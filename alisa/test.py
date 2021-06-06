# -*- coding: utf-8 -*-

from operator import le
from flask import Flask, request
from pymongo import MongoClient
import time
import threading
import pymorphy2
import json
app = Flask(__name__)

morph = pymorphy2.MorphAnalyzer()
server_uri = "mongodb+srv://user1:4X5j6rXjVRyX7Nq@clusterone.zewh9.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
client = MongoClient(server_uri)
db = client.Obi_Products
records = db.products

lst = list(records.find({}))
lst_2 = {}
current_Lst = None

word = 'шпаклев'
word2 = '4,8'
weight = []
base = []
ready = []



for row in lst:
    if word.lower() in row['title'].lower():
        # lst_2['title'].append(row['title'])
        # lst_2['table2'].append(row['table2'])
        lst_2[row['title']] = row['table2']
        current_Lst = lst_2

# for title in current_Lst:
#     print(str(title) + str(current_Lst[title]) + '\n')
#     print(current_Lst[title][current_Lst[title].index('Назначение:')])


for title in current_Lst:  
    # print(str(title) + str(current_Lst[title]) + '\n')
    # print(current_Lst[title][current_Lst[title].index('Количество в упаковке:')])
    
    # if 'Диаметр резьбы:' in current_Lst[title]:
    #     diameter.append(current_Lst[title][current_Lst[title].index('Диаметр резьбы:')+1])
    if 'Основа:' in current_Lst[title]:
        base.append(current_Lst[title][current_Lst[title].index('Основа:')+1])
    if 'Готовность:' in current_Lst[title]:        
        ready.append(current_Lst[title][current_Lst[title].index('Готовность:')+1])     
    if 'Вес:' in current_Lst[title]:
        weight.append(current_Lst[title][current_Lst[title].index('Вес:')+1])     
        

base = set(base)
ready = set(ready)
weight = set(weight)


print('Найдены следующие варианты: \n''Основа: ' + ', '.join(base) + '\n' + 'Готовность: ' + ', '.join(ready) + '\n' + 'Вес: ' + ', '.join(weight))

