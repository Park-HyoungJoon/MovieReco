import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from sklearn.metrics.pairwise import cosine_similarity
from konlpy.tag import Okt
import re

df = pd.read_csv('movie2.csv', encoding='utf-8')
# print(df.shape)
# print(df)

df = df.dropna()

"""한글, 숫자, 영어 빼고 전부 제거"""


def sub_special(s):
    return re.sub(r'[^ㄱ-ㅎㅏ-ㅣ가-힣0-9a-zA-Z ]', '', s)


STOP_WORDS = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']
df.loc[:, "stoty"] = df.loc[:, "stoty"].apply(sub_special)


def morph_and_stopword(s):
    token_ls = []
    # 형태소 분석
    okt = Okt()
    tmp = okt.morphs(s, stem=True)

    # 불용어 처리
    for token in tmp:
        if token not in STOP_WORDS:
            token_ls.append(token)


"""TF-IDF로 만들기"""
tfidf = TfidfVectorizer()
tfidf_matrix = tfidf.fit_transform(df.stoty)
# 줄거리에 대해서 tf-idf 수행
print(tfidf_matrix.shape)

"""코사인 유사도 구하기"""
cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)

"""인덱스 테이블 만들기"""
indices = pd.Series(df.index, index=df.name).drop_duplicates()
# print(indices)


"""추천 해주기"""


def movie_REC(name, cosine_sim=cosine_sim):
    # 입력한 영화로 부터 인덱스 가져오기
    idx = indices[name]

    # 모든 영화에 대해서 해당 영화와의 유사도를 구하기
    sim_scores = list(enumerate(cosine_sim[idx]))

    # 유사도에 따라 영화들을 정렬
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)

    # 가장 유사한 10개의 영화를 받아옴
    sim_scores = sim_scores[1:11]
    # print(sim_scores)

    # 가장 유사한 10개 영화의 인덱스 받아옴
    movie_indices = [i[0] for i in sim_scores]
    # print(movie_indices)

    # 기존에 읽어들인 데이터에서 해당 인덱스의 값들을 가져온다. 그리고 스코어 열을 추가하여 코사인 유사도도 확인할 수 있게 한다.
    result_df = df.iloc[movie_indices].copy()
    result_df['score'] = [i[1] for i in sim_scores]

    # 읽어들인 데이터에서 줄거리 부분만 제거, 제목과 스코어만 보이게 함
    del result_df['stoty']

    # 가장 유사한 10개의 영화의 제목을 리턴
    return result_df


# 예시
print(movie_REC("어벤져스"))