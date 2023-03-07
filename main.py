import extractor.scraping as scraping
import data_processing

def main():
    # 20230206 기준 영화 최대 10페이지까지의 리뷰를 스크래핑해서 csv 파일로 저장
    scraping.movie_reviews(kind='all_time', page=10, date='20230206')
    scraping.movie_reviews(kind='now', page=1, date='20230206')
    # 20230206 기준 영화 최대 10페이지까지의 짧은 평점과 점수를 스크래핑해서 csv 파일로 저장
    scraping.movie_short_comments(kind='all_time', page=10, date='20230206')
    scraping.movie_short_comments(kind='now', page=1, date='20230206')



if __name__ == '__main__':
    main()