import extractor.scraping as scraping
import data_processing

if __name__ == '__main__':
    reviews = scraping.get_movie_reviews(kind='all_time')

    data_processing.save_to_csv(reviews)