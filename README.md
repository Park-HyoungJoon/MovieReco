# MovieReco

python과 Django를 사용하여 제작한 영화추천 프로그램



# 개발동기
넷플릭스, 왓챠 등과 같은 OTT 서비스가 급증하고 있는 요즘, 사용자의 편리하고 폭넓은 문화생활을 돕는 데에 목적성을 둔 "영화추천시스템"을 구현하려고 한다.

사용자 맞춤 알고리즘은 사용자의 시청 기록을 기반으로 유사성 높은 새로운 컨텐츠를 제공하는 형태를 가지고 있다. 그러나 이러한 알고리즘들은 많은 시간과 데이터가 필요했으며, 영화의 제목과 간단한 내용만을 보여줄 뿐이기 때문에, 기본적인 추천만으로는 사용자의 적극적 선택까지 이어지기 어렵다고 생각했다. 

많은 시간과 데이터 없이도 줄거리 간의 유사도만으로도 영화를 추천해줄 수 있는 보다 간단한 시스템을 만들어보고자 했으며, 두번째로 언급했던 아쉬운 부분에 대해, 트위터 API를 사용해 긍정 또는 부정적 견해에 대한 비율을 시각화하여 보여주는 기능을 추가하고자 했다.

# 사용 기능
한국영화 진흥원에서 1990년부터 2022년 까지의 데이터를 가져와 영화제목으로 네이버 영화에서 
줄거리를 크롤링하여 데이터셋을 제작

TF-IDF 기법과 코사인 유사도 기법으로 줄거리 간의 유사도를 측정

python의 tweets를 사용.
트위터에서 keyword(영화이름)을 noOfTweets(검색 수 제한)만큼 댓글들을 크롤링해 가져온다.
자연어 처리 기능 중 하나인 ‘vader_lexicon’(vader 사전)을 다운로드 받는다.
tweets(크롤링하여 가져온 댓글들)을 foreach를 통해 tweet(하나의 댓글)로 나눈다.
SentimentIntensityAnalyzer().polarity_scores를 사용해 각 트위터 댓글의 감정분석을 실시한다.
감정 분석을 실시하게 되면 100%를 기준으로 neg(부정), neu(중립), pos(긍정)에 각각 감정점수를 부여한다. 




# 동작 시나리오
![image](https://github.com/Park-HyoungJoon/MovieReco/assets/83392856/8e50b897-f2f5-43e8-a536-cf894961ca5d)

# 결과 화면
![image](https://github.com/Park-HyoungJoon/MovieReco/assets/83392856/e9b98e63-d41b-4b83-855e-fd22295adc2a)
![image](https://github.com/Park-HyoungJoon/MovieReco/assets/83392856/0ddce1d5-d6a2-42ba-b8b5-2a621430a19a)
![image](https://github.com/Park-HyoungJoon/MovieReco/assets/83392856/28e2adec-0c95-4200-af91-cf3d7c32a975)

