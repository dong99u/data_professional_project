import extractor.scraping as scraping
import data_processing

def main():
    reviews = scraping.get_movie_reviews(kind='now')

    data_processing.save_to_csv(reviews, 'final_project/movie_reviews_now.csv')

if __name__ == '__main__':
    main()