import requests
from bs4 import BeautifulSoup
import re

# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.chrome.service import Service
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.common.by import By


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36'}


# def webdriver():
#     options = Options()
#     options.add_argument("disable-infobars")
#     options.add_argument("disable-extensions")
#     options.add_argument("start-maximized")
#     options.add_argument('disable-gpu')
#     options.add_argument('headless')
#     options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/109.0.0.0 Safari/537.36")

#     # Selenium 4.0 - load webdriver
#     try:
#         s = Service(ChromeDriverManager().install())
#         browser = webdriver.Chrome(service=s, options=options)
#         return browser
#     except Exception as e:
#         print(e)
#     return

def movie_info(kind='all_time'):
    # movie_name_code_info = get_movie_list_now_in_theathers()
    reviews = []
    if kind == 'all_time':
        movie_name_code_info = get_movie_list_all_time()
    elif kind == 'now':
        movie_name_code_info = get_movie_list_now_in_theathers()

    for movie_name, movie_code in movie_name_code_info.items():
        reviews.append(get_comments_star(movie_name, movie_code))
        
    return reviews

def movie_review(kind='all_time'):
    reviews = []

    if kind == 'all_time':
        movie_name_code_info = get_movie_list_all_time()
    elif kind == 'now':
        movie_name_code_info = get_movie_list_now_in_theathers()


    for movie_name, movie_code in movie_name_code_info.items():
        reviews.append(get_movie_reviews(movie_name, movie_code))

    return reviews

def get_movie_list_all_time():
    try:
        MOVIE_LAST_PAGE = 2
        # {영화이름: 영화코드}
        movie_name_code_info = {}

        for page in range(1, MOVIE_LAST_PAGE):
            url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=pnt&date=20230202&page={page}'
            soup = get_soup(url)
            for movie in soup.select('td.title div.tit5 a'):
                movie_name = movie['title']
                movie_code = movie['href'].split('=')[1]
                movie_name_code_info[movie_name] = movie_code
    
        return movie_name_code_info

    except:
        print('Error: Can\'t get movie list of all time')
        return None


def get_movie_list_now_in_theathers():
    try:
        # 평점순 영화 리스트
        url = 'https://movie.naver.com/movie/running/current.naver?view=list&tab=normal&order=point'

        soup = get_soup(url)
        movie_list = soup.select('div.lst_wrap > ul.lst_detail_t1 li')
        
        # {영화이름: 영화코드}
        movie_name_code_info = {}
        
        for movie in movie_list:
            movie_name = movie.select_one('dl.lst_dsc > dt.tit > a').get_text()
            movie_code = movie.select_one('dl.lst_dsc > dt.tit > a')['href'].split('=')[1]
            movie_name_code_info[movie_name] = movie_code

        return movie_name_code_info

    except:
        print('Error: Can\'t get movie list')
        return None


def get_comments_star(movie_name, movie_code):
    try:
        COMMENTS_LAST_PAGE = 301
        # 겹치는 리뷰 페이지는 더이상 스크래핑 하지 않게 하기 위한 변수
        before_page = None

        reviews = []

        for page in range(1, COMMENTS_LAST_PAGE):
            url = f'https://movie.naver.com/movie/bi/mi/pointWriteFormList.naver?code={movie_code}&type=after&isActualPointWriteExecute=false&isMileageSubscriptionAlready=false&isMileageSubscriptionReject=false&page={page}'
            soup = get_soup(url)

            if same_page(before_page, soup):
                break

            for review in soup.select('div.score_result ul li'):
                score = review.select_one('div.star_score > em').get_text().strip()
                comment = review.select_one('div.score_reple > p > span:last-child').get_text().strip()
                user_id = review.select_one('div.score_reple > dl > dt > em').get_text().strip()
                date = review.select_one('div.score_reple > dl > dt > em:last-child').get_text().strip()

                # {점수, 댓글}
                reviews.append({'title': movie_name, 'score': score, 'comment': comment, 'user_id': user_id, 'date': date})
        
            before_page = soup.get_text()
            
        return reviews
    
    except:
        print('Error: Can\'t get comments and stars')


def get_movie_reviews(movie_name, movie_code):
    try:

        before_page = None
        reviews = {'title': movie_name, 'info': []}
        # 영화 평점순 리스트
        for page in range(1, 11):
            url = f'https://movie.naver.com/movie/bi/mi/review.naver?code={movie_code}&page={page}'
            print(url, movie_name, movie_code)
            soup = get_soup(url)

            if same_page(before_page, soup):
                break
        # 영화 리뷰 리스트
            review_list = soup.select('div.review ul.rvw_list_area li')

            for review in review_list:
                p = re.compile(r'\d+') # 숫자만 추출
                review_nid = p.findall(review.a.get('onclick'))[0]
                print(review_nid)
                review_url = f'https://movie.naver.com/movie/bi/mi/reviewread.naver?nid={review_nid}&code={movie_code}&order=#tab'

                review_soup = get_soup(review_url)

                content = review_soup.select_one('div.review div.user_tx_area').get_text().strip()
                user_id = review_soup.select_one('div.review div.board_title ul li:last-child a em').get_text().strip()
                view_count = review_soup.select_one('div.review div.board_title div.user_tx_info span > em').get_text().strip()
                date = review_soup.select_one('div.review div.top_behavior span.wrt_date').get_text().strip()
                reviews['info'].append({'content': content, 'view_count': view_count, 'date': date, 'user_id': user_id})

            before_page = soup.get_text()

        return reviews

    except TypeError as e:
        print(f'Error: Can\'t get movie reviews: {e}')
        return None

def get_soup(url):
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'lxml')
        return soup
    except:
        print('Error: Can\'t get soup')
        return None


def same_page(before_page, soup):
    if before_page == soup.get_text():
        return True
    else:
        return False