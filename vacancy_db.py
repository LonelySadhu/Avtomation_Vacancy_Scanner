import pandas as pd


def create_csv_db():
    try:
        data = pd.read_csv('vacancies.csv')
    except FileNotFoundError:
        df = pd.DataFrame({'position_name': [],
                           'salary': [],
                           'company': [],
                           'responsibilities': [],
                           'requirements': [],
                           'link': [],
                           'responded': []},
                           columns=['position_name', 'salary', 'company', 'responsibilities',
                                    'requirements', 'link', 'responded'])
        df.to_csv('vacancies.csv')


def save_to_db(df):
    try:
        data = pd.read_csv('vacancies.csv')
        data = pd.concat([data, df], ignore_index=True, axis=1)
        data.to_csv('vacancies.csv')
    except FileNotFoundError:
        df.to_csv('vacancies.csv')


def show_db():
    data = pd.read_csv('vacancies.csv')
    print(data.columns)
    print(data.head())




