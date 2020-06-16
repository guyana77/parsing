from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
import re
from pymongo import MongoClient

client = MongoClient('localhost', 27017)

db = client['vacancies']

vacancies = db.vacancies

# Код из прошлого урока

vacancy_name = input('Введите название вакансии для поиска по всей России: ')

main_link = 'https://hh.ru/search/vacancy'

params = {'area': '113',
          'st': 'searchVacancy',
          'text': vacancy_name}
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.138 Safari/537.36 OPR/68.0.3618.125',
    'Accept': '*/*'}

response = requests.get(main_link, params=params, headers=headers)

soup = bs(response.text, 'lxml')

total_pages = soup.findAll('a', {'class': "bloko-button HH-Pager-Control"})

pages = int(total_pages[-1].text)

parsed_vacancies = []

for i in range(pages):

    params_for_pages = {'area': '113',
                        'st': 'searchVacancy',
                        'text': vacancy_name,
                        'page': i}
    response_for_pages = requests.get(main_link, params=params_for_pages, headers=headers)

    soup_for_pages = bs(response_for_pages.text, 'lxml')

    vacancy_block = soup_for_pages.find('div', {'class': 'vacancy-serp'})

    vacancy_list = vacancy_block.findAll('div', {'data-qa': 'vacancy-serp__vacancy'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        name = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'}).text
        link = vacancy.find('a', {'class': 'bloko-link HH-LinkModifier'})['href']
        salary = vacancy.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
        if not salary:
            min_salary = None
            max_salary = None
        else:
            salary = salary.getText().replace(u'\xa0', u'')
            salaries = salary.split('-')
            salaries[0] = re.sub(r'[^0-9]', '', salaries[0])
            min_salary = int(salaries[0])
            if len(salaries) > 1:
                salaries[1] = re.sub(r'[^0-9]', '', salaries[1])
                max_salary = int(salaries[1])
            else:
                max_salary = None

        vacancy_data['name'] = name
        vacancy_data['link'] = link
        vacancy_data['source'] = 'hh.ru'
        vacancy_data['min_salary'] = min_salary
        vacancy_data['max_salary'] = max_salary
        parsed_vacancies.append(vacancy_data)

# Код к данному уроку

for v in parsed_vacancies:
    vacancies.update_one({}, {'$set': v}, upsert=True)

