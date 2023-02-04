import extractor.scraping as scraping
import data_processing

def main():
    reviews = scraping.movie_review(kind='all_time')
    
    for review in reviews:
        data_processing.save_to_csv(f"C:/Users/parkdongkyu/Desktop/codestates_data_anal/final_project/data{review['title']}.csv", review['info'], ['content', 'view_count', 'date', 'user_id'])

if __name__ == '__main__':
    main()