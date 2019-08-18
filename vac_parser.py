import requests
from bs4 import BeautifulSoup
import time
import re
import pandas as pd
from vacancy_db import save_to_db



def input_params():
    vacancy_text = input('Введите название вакансии или ключевые навыки: ')
    return vacancy_text


def count_pages(html_doc):
    soup = BeautifulSoup(html_doc, 'html.parser')
    pages_block = soup.findAll('a', {'class': 'bloko-button HH-Pager-Control'})
    return int(pages_block[-1].string)


def request_to_hh(vacancy, page=6):
    header = {
        'accept': '*/*',
        'user-agent': 'User-Agent: Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36'
    }
    params = {
        'area': '1',
        'text': vacancy,
        'page': page
    }
    all_pages = []  # Собираем все страницы с данными параметрами запроса
    try:
        response = requests.get('https://hh.ru/search/vacancy', headers=header, params=params)
        print(response.status_code)
        number_of_pages = count_pages(response.text)  # парсим количество страниц с данными параметрами

        if page == 0:
            all_pages.append(response.text)
            for doc in range(1, number_of_pages):
                params['page'] = doc
                response = requests.get('https://hh.ru/search/vacancy', headers=header, params=params)
                if response.status_code == 200:
                    all_pages.append(response.text)
                    time.sleep(1)  # Время на прогрузку страницы
                else:
                    continue
            return all_pages
        else:  # для теста возвращаем только одну заданную страницу
            if page <= number_of_pages:
                params['page'] = page
                response = requests.get('https://hh.ru/search/vacancy', headers=header, params=params)
                all_pages.append(response.text)
                return all_pages
            else:
                print(f'Всего страниц с заданными параметрами: {number_of_pages}, вы указали: {page}')

    except requests.exceptions.ConnectionError:
        print('Please check your internet connection!')
        exit(1)


def page_parser(html_docs):

    # структура для записи в бд
    columns = ['position_name', 'salary', 'company', 'responsibilities', 'requirements', 'link', 'responded']
    position_name = []
    salary = []
    company = []
    responsib = []
    requir = []
    link = []
    responded = []

    for doc in html_docs:  # Обходим все переданные страницы и парсим нужные данные
        soup = BeautifulSoup(doc, 'html.parser')
        vacancies = soup.findAll('div', {'data-qa': 'vacancy-serp__vacancy'})

        for vac in vacancies:
            position_name.append(vac.find('div', {'class': 'resume-search-item__name'}).span.a.string)
            try:
                r_salary = vac.find('div', {'class': 'vacancy-serp-item__compensation'}).string
                match_salary = re.search(r'\d{2,4}\s{1,2}\d{1,4}', r_salary).group()
                salary.append(int("".join(match_salary.split())))
            except AttributeError:
                salary.append(None)
            company.append(vac.find('div', {'class': 'vacancy-serp-item__meta-info'}).a.string)
            requir.append(vac.find('div', {'data-qa': 'vacancy-serp__vacancy_snippet_responsibility'}).string)
            responsib.append(vac.find('div', {'data-qa':'vacancy-serp__vacancy_snippet_requirement'}).string)
            link.append(vac.find('div', {'class': 'resume-search-item__name'}).span.a['href'])
            responded.append(False)

    df = pd.DataFrame({'position_name': position_name,
                       'salary': salary,
                       'company': company,
                       'responsibilities': responsib,
                       'requirements': requir,
                       'link': link,
                       'responded': responded
                       }, columns=columns)
    save_to_db(df)





