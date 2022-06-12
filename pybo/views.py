import json
import os
import sys
from datetime import time

import requests
from django.shortcuts import render
from django.http import HttpResponse, response
from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from nltk.sentiment import SentimentIntensityAnalyzer
from googletrans import Translator
from .models import Question
import nltk
import pandas as pd
import numpy as np
import tweepy
from textblob import TextBlob
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Okt
import re


# Create your views here.
def index(request):

    return render(request, 'pybo/search_main.html')

def detail(request,question_id):
    """
    pybo 내여ㅛㅇ 출력
    """
    if request.method == 'POST':
        data = json.loads(request.body)
        print(data)

        context = {
            'result':data,
        }
        return JsonResponse(context)
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request,'pybo/question_detail.html',context)


def modal(request,question_id):
    """
    pybo 내여ㅛㅇ 출력
    """
    question = get_object_or_404(Question, pk=question_id)
    context = {'question': question}
    return render(request,'pybo/my_modal.html',context)

@csrf_exempt
def main(request):
    translator = Translator()
    question_list = Question.objects.order_by('-create_date')
    image = []
    subtitle = []
    title = []
    date = []
    director = []
    actors = []
    rating = []
    posi = []
    nega = []

    for question in question_list:
        ### 영화 상세정보
        client_id = "Lto6_bod66oF06JX0cym"
        client_secret = "e0FM1WU2z0"

        movie = question.subject
        header_parms = {"X-Naver-Client-Id": client_id, "X-Naver-Client-Secret": client_secret}
        url = f"https://openapi.naver.com/v1/search/movie.json?query={movie}"
        res = requests.get(url, headers=header_parms)
        data = res.json()
        image.append(data['items'][0]['image'])
        subtitle.append(data['items'][0]['subtitle'])
        title.append(data['items'][0]['title'])
        date.append(data['items'][0]['pubDate'])
        director.append(data['items'][0]['director'].split('|')[0])
        actors.append(data['items'][0]['actor'].split('|')[:-1])
        rating.append(float(data['items'][0]['userRating']))

        ### 사람심리조사
        consumerKey = "swlbPpEoXrl6cb44UohWViEn4"
        consumersecret = "OGwcPDpOffiQCg4U0Oh9QpoYuvfGYq7atWpFy3TrwKKb7sLB3B"
        token = "1124707533510152192-Tnk8k0OzVPbyhSojsNVZ6zdsdyuu0u"
        token_secret = "1YXNGTb0OXvPiZuGKc0iDj2zXeUf8mmaoAXBiIzj8Na8M"
        auth = tweepy.OAuthHandler(consumerKey, consumersecret)
        auth.set_access_token(token, token_secret)
        api = tweepy.API(auth)
        def percentage(part, whole):
            return 100 * float(part) / float(whole)

        keyword = data['items'][0]['subtitle']
        noOfTweet = 100
        tweets = tweepy.Cursor(api.search_tweets, q=keyword).items(noOfTweet)
        positive = 0
        negative = 0
        # neutral = 0
        polarity = 0
        tweet_list = []
        # neutral_list = []
        negative_list = []
        positive_list = []
        nltk.download('vader_lexicon')
        for tweet in tweets:

            # print(tweet.text)
            tweet_list.append(tweet.text)
            analysis = TextBlob(tweet.text)
            score = SentimentIntensityAnalyzer().polarity_scores(tweet.text)
            neg = score['neg']
            neu = score['neu']
            pos = score['pos']
            comp = score['compound']
            polarity += analysis.sentiment.polarity

            if neg > pos:
                negative_list.append(tweet.text)
                negative += 1
            elif pos > neg:
                positive_list.append(tweet.text)
                positive += 1

    # elif pos == neg:
    #   neutral_list.append(tweet.text)
    #  neutral += 1
        positive = percentage(positive, noOfTweet)
        negative = percentage(negative, noOfTweet)
    # eutral = percentage(neutral, noOfTweet)
        polarity = percentage(polarity, noOfTweet)
        positive = format(positive, '.1f')
        negative = format(negative, '.1f')
    # neutral = format(neutral, '.1f')
        c={}
    # neutral_list = pd.DataFrame(neutral_list)
        negative_list = pd.DataFrame(negative_list)
        positive_list = pd.DataFrame(positive_list)
        total = len(positive_list) + len(negative_list)
        posi.append(len(positive_list) / total)
        nega.append(len(negative_list) / total)
        schedule_list = zip(title,date,director,actors,rating,image,subtitle,posi,nega)
    return render(request, 'pybo/question_list.html', {'question_list':question_list,'title':title,'date':date,'director':director,
                                                       'actors':actors,'rating':rating,'image':image,'subtitle':subtitle,'positive':posi,'negative':nega,'s_l':schedule_list})