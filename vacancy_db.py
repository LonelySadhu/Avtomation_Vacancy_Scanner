import pandas as pd
from datetime import datetime, timedelta


def save_to_db(df):
    try:
        data = pd.read_csv('vacancies.csv')
        df = df.loc[~df['link'].isin(data.link.values)]  # Проверка на оригинальность
        data = pd.concat([data, df], ignore_index=True)  # Добавление новых записей
        data.to_csv('vacancies.csv', index=False)
    except FileNotFoundError:
        df.to_csv('vacancies.csv', index=False)


def clear_db():
    import os

    try:
        os.remove('vacancies.csv')
    except FileNotFoundError:
        pass


def show_db():
    try:
        data = pd.read_csv('vacancies.csv')
        print(data.info())
        print(data.shape)
    except FileNotFoundError:
        print('Для начала запустите парсер, файла не существует!')


def show_fresh(days=3):
    """Выбираем из датасета только свежие вакансии"""
    import warnings
    warnings.filterwarnings("ignore", category=FutureWarning)
    try:
        data = pd.read_csv('vacancies.csv')
        data['date'] = pd.to_datetime(data['date'])
        print(data.loc[data['date'].between(datetime.now().date() - timedelta(days=days), datetime.now().date()), :])
    except FileNotFoundError:
        print('Для начала запустите парсер, файла не существует!')

