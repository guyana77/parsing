# 1. Посмотреть документацию к API GitHub, разобраться как вывести список репозиториев для
# конкретного пользователя, сохранить JSON-вывод в файле *.json.

import  requests
import json
main_link = 'https://api.github.com/users/guyana77/repos'
response = requests.get(main_link).json()
with open('repos.json', 'w')as f:
    json.dump(response, f)