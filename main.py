import extractor.scraping as scraping
import data_processing

def main():
    scraping.movie_reviews(page=10)

if __name__ == '__main__':
    main()