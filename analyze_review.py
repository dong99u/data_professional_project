import pandas as pd
import numpy as np

import os, re
from tqdm import tqdm

# 경고문구 미표시
import warnings
warnings.filterwarnings('ignore')

# 한글 폰트 지정
import matplotlib.pyplot as plt
plt.rc('font', family='NanumBarunGothic')


from konlpy.utils import pprint
from konlpy.tag import Okt
import torchtext 
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.linear_model import LogisticRegression

# 시각화
import pyLDAvis.sklearn

from data_processing import generating_dataframe

def get_comments(type='review'):
    if type == 'review':
        for movie_name, df in generating_dataframe(type):
            review_data = df['main_text'].dropna().values
            

def predict_model():
    # 데이터 다운로드 
    # 다운로드 받을 폴더를 준비
    DATA_DIR = "./data"
    os.makedirs(DATA_DIR, exist_ok=True)
    
    train_data = torchtext.utils.download_from_url(url='https://raw.githubusercontent.com/e9t/nsmc/master/ratings_train.txt', 
                                    path=os.path.join(DATA_DIR, 'train.txt'))
    test_data = torchtext.utils.download_from_url(url='https://raw.githubusercontent.com/e9t/nsmc/master/ratings_test.txt', 
                                    path=os.path.join(DATA_DIR, 'test.txt'))

    train_data = pd.read_csv('data/train.txt', sep='\t')
    test_data = pd.read_csv('data/train.txt', sep='\t')
    data = pd.concat([train_data, test_data])
    data.drop_duplicates(subset = ['document'], inplace=True) # document 열에서 중복인 내용이 있다면 중복 제거
    data['document'] = data['document'].str.replace("[^ㄱ-ㅎㅏ-ㅣ가-힣 ]","") # 정규 표현식 수행
    data['document'] = data['document'].str.replace('^ +', "") # 공백은 empty 값으로 변경
    data['document'].replace('', np.nan, inplace=True) # 공백은 Null 값으로 변경
    data = data.dropna(how='any') # Null 값 제거
    data.reset_index(inplace=True)
    
    okt = Okt()
    review_data = data['document'].dropna().values
    cleaned_review_data = []

    for review in tqdm(review_data):
        tokens = okt.nouns(review)
        cleaned_tokens = []
        for word in tokens:
            if len(word) > 2:
                cleaned_tokens.append(word)
            else:
                pass
        cleaned_review = " ".join(cleaned_tokens)
        cleaned_review_data.append(cleaned_review)

    # TF-IDF 변환기 객체를 생성
    tfid = TfidfVectorizer()

    review_tfid = tfid.fit_transform(cleaned_review_data)
    # 단어 사전 확인 (딕셔너리 형태)
    vocab = tfid.vocabulary_
    index_to_word = { v:k for k, v in vocab.items() } 

    labels = data['label'].values
    lr = LogisticRegression()

# TF-IDF 벡터를 입력하여 모델 학습 
    lr.fit(review_tfid, labels)
    return lr