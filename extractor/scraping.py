import requests
from bs4 import BeautifulSoup
import re
import data_processing 

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

def movie_info(kind='all_time', page=1):
    # movie_name_code_info = get_movie_list_now_in_theathers()
    reviews = []
    if kind == 'all_time':
        movie_name_code_info = get_movie_list(kind, page, date='20230206')
    elif kind == 'now':
        movie_name_code_info = get_movie_list(kind, 1, date='20230206')

    for movie_name, movie_code in movie_name_code_info.items():
        reviews.append(get_comments_star(movie_name, movie_code))
        
    return reviews

def movie_reviews(kind='all_time', page=1):
    p = re.compile(r'[\/:*?:"<>|]')

    if kind == 'all_time':
        movie_name_code_info = get_movie_list(kind, page, date='20230206')
    elif kind == 'now':
        movie_name_code_info = get_movie_list(kind, 1, date='20230206')

    for movie_name, movie_code in movie_name_code_info.items():
        review = get_movie_reviews(movie_name, movie_code)
        if review:
            movie_name = p.sub('', movie_name)
            data_processing.save_to_csv(movie_name, review['reviews'], ['user_id', 'star_score', 'view_count', 'recommend_count', 'main_text'])
        else:
            print(movie_name, movie_code, 'No review - None')

    

def get_movie_list(type='all_time', MOVIE_LAST_PAGE = 1, date='20230206'):
    try:
        # {영화이름: 영화코드}
        movie_name_code_info = {}
        if type == 'all_time':
            type = 'pnt'
        elif type == 'now':
            type = 'cur'

        for page in range(1, MOVIE_LAST_PAGE + 1):
            url = f'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel={type}&date={date}&page={page}'
            soup = get_soup(url)
            for movie in soup.select('td.title div.tit5 a'):
                movie_name = movie['title']
                movie_code = movie['href'].split('=')[1]
                movie_name_code_info[movie_name] = movie_code
    
    # {'탑건: 매버릭': '81888', '클라우스': '191613', '가버나움': '174830', '그린 북': '171539'
        return movie_name_code_info

    except:
        print('Error: Can\'t get movie list of all time')
        return None


# def get_movie_list_now_in_theathers():
#     try:
#         # 평점순 영화 리스트
#         url = 'https://movie.naver.com/movie/sdb/rank/rmovie.naver?sel=cur&date=20230206'

#         soup = get_soup(url)
#         movie_list = soup.select('div.lst_wrap > ul.lst_detail_t1 li')
        
#         # {영화이름: 영화코드}
#         movie_name_code_info = {}
        
#         for movie in movie_list:
#             movie_name = movie.select_one('dl.lst_dsc > dt.tit > a').get_text()
#             movie_code = movie.select_one('dl.lst_dsc > dt.tit > a')['href'].split('=')[1]
#             movie_name_code_info[movie_name] = movie_code

#         return movie_name_code_info

#     except:
#         print('Error: Can\'t get movie list')
#         return None


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

# 한 영화에 대한 리뷰를 최대 10페이지까지 스크래핑
def get_movie_reviews(movie_name, movie_code):
    try:
        url = f'https://movie.naver.com/movie/bi/mi/review.naver?code={movie_code}'
        last_page = paging(url)

        if not last_page:
            return None


        info = {'title': movie_name, 'reviews': []}
        for page in range(1, last_page + 1):
            nid_list = get_nid(url, page)
            for nid in nid_list:
                info['reviews'].append(review_content(movie_code, nid))

        return info


    except Exception as e:
        print(f'Error: Can\'t get movie reviews: {e}')

# 영화 리뷰의 한 페이지의 코드들을 리턴함
def get_nid(url, page):
    try:
        url = f'{url}&page={page}'
        soup = get_soup(url)
        review_list = soup.select('div.review > ul.rvw_list_area li > a')
        p = re.compile(r'\d{5,7}')

        nid_list = []
        for review in review_list:
            m = p.search(str(review))
            if m:
                nid_list.append(m.group())

        return nid_list

    except Exception as e:
        print(f'Error: Can\'t get review code: {e}')
        return None

def review_content(movie_code, nid):
    try:
        url = f'https://movie.naver.com/movie/bi/mi/reviewread.naver?nid={nid}&code={movie_code}&order=#tab'
        soup = get_soup(url)

        main_text = soup.find('div', class_='user_tx_area').get_text().strip()
        main_text = re.sub(r'\s', " ", main_text)
        user_id = soup.select_one('div.board_title ul li:last-child em').get_text().strip()
        view_count = soup.select_one('div.user_tx_info span:first-child em').get_text().strip()
        recommend_count = soup.select_one('div.user_tx_info span:nth-child(2) em').get_text().strip()
        star_score = soup.select_one('div.star_score em')
        if star_score:
            star_score = star_score.get_text().strip()

        return {'user_id': user_id, 'star_score': star_score, 'view_count': view_count, 'recommend_count': recommend_count,  'main_text': main_text}


    except Exception as e:
        print(f'Error: Can\'t get review content: {e}')
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


def paging(url):
    try:
        soup = get_soup(url)
        pages = soup.select('div.paging a > span')
        if pages:
            last_page = pages[-1].get_text()
            return int(last_page)
        return None
        
    
    except Exception as e:
        print(f'Error: Can\'t get last page: {e}')
        return None