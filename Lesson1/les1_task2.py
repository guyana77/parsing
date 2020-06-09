# 2. Изучить список открытых API. Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.

import  requests
import json
import vk

access_token = '182c6a65c2b327398080df76f918c339f5b6bd97c6ed22e1fefb92724acb763a9e0b81da4bb870217063c'
v = '5.107'
session = vk.Session(access_token=access_token)
api = vk.API(session, v=v)

info = api.account.getProfileInfo()

with open('vk_info.json', 'w')as f:
    json.dump(info, f)
