import csv

def save_to_csv(file_name: str, reviews:dict, columns:list):
    try:
        with open(f"C:/Users/parkdongkyu/Desktop/codestates_data_anal/final_project/data/{file_name}.csv", 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns) # ['user_id', 'star_score', 'recommend_count', 'main_text']
            for review in reviews:
                writer.writerow([review[column] for column in columns])
                
    except Exception as e:
        print(f'Error: Can\'t save to csv file: {e}')

