import csv
import pandas as pd
import os

def save_to_csv(file_name: str, reviews:dict, columns:list):
    try:
        with open(f"C:/Users/parkdongkyu/Desktop/codestates_data_anal/final_project/data/{file_name}.csv", 'w', encoding='utf-8', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(columns) # ['user_id', 'star_score', 'recommend_count', 'main_text']
            for review in reviews:
                writer.writerow([review[column] for column in columns])
                
    except Exception as e:
        print(f'Error: Can\'t save to csv file: {e}')


def load_csv_files(type='review'):

    dir_path = f"data/{type}"
    file_list = os.listdir(dir_path) # unpacking

    yield from file_list


def generating_dataframe(type='review'):
    try:
        dir_path = f"data/{type}"
        for file_name in os.listdir(dir_path):
            df = pd.read_csv(os.path.join(dir_path, file_name))
            yield file_name, df

        

    except Exception as e:
        print(f'Error: Can\'t transform to dataframe: {e}')
