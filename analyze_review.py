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
okt = Okt()

from data_processing import generating_dataframe

def get_comments(type='review'):
    if type == 'review':
        for movie_name, df in generating_dataframe(type):
            review_data = df['main_text'].dropna().values
            
