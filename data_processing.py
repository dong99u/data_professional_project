import csv

def save_to_csv(review_list, file_name):
    try:
        with open(file_name, 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(['title', 'score', 'comment', 'user_id', 'date'])
            for review in review_list:
                for elem in review:
                    writer.writerow([elem['title'], elem['score'], elem['comment'], elem['user_id'], elem['date']])
                
    except Exception as e:
        print(f'Error: Can\'t save to csv file: {e}')