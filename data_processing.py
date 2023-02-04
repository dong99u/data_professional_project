import csv

def save_to_csv(file_name, reviews:dict, columns:list):
    try:
        with open(file_name, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns) # ['title', 'score', 'comment', 'user_id', 'date']
            for review in reviews['info']:
                writer.writerow([review[column] for column in columns])
                
    except Exception as e:
        print(f'Error: Can\'t save to csv file: {e}')
