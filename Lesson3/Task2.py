def desired_salary(salary):

    for vacancy in vacancies.find({'$or': [{'max_salary': None, 'min_salary': {'$gt': salary}},
                                           {'min_salary': None, 'max_salary': {'$gt': salary}},
                                           {'max_salary': {'$gt': salary}}]}):
        pprint(vacancy)

desired_salary(int(input('Введите нижний порог зарплаты: ')))