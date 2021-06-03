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

word = 'Шпиль'
word2 = '4,8'
diameter = []
lenght = []
count = []
material = []

# for row in lst:
#     if word in row['title'].lower():              
#         diameter.append(row['table2'][5])
#         lenght.append(row['table2'][7])
#         slot.append(row['table2'][13])

# diameter = set(diameter)
# lenght = set(lenght)
# slot = set(slot)
# print('Найдены следующие варианты: \n''Диаметр: ' + ', '.join(diameter) + '\n' + 'Длина: ' + ', '.join(lenght) + '\n' + 'Тип шлица: ' + ', '.join(slot) + '\n' + 'Назначение: ' + ', '.join(appointment))

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
    
    if 'Диаметр резьбы:' in current_Lst[title]:
        diameter.append(current_Lst[title][current_Lst[title].index('Диаметр резьбы:')+1])
    if 'Длина:' in current_Lst[title]:
        lenght.append(current_Lst[title][current_Lst[title].index('Длина:')+1])
    if 'Количество в упаковке:' in current_Lst[title]:
        count.append(current_Lst[title][current_Lst[title].index('Количество в упаковке:')+1])     
    if 'Материал:' in current_Lst[title]:
        material.append(current_Lst[title][current_Lst[title].index('Материал:')+1])     
        

diameter = set(diameter)
lenght = set(lenght)
count = set(count)
material = set(material)

print('Найдены следующие варианты: \n''Диаметр: ' + ', '.join(diameter) + '\n' + 'Длина: ' + ', '.join(lenght) + '\n' + 'Материал: ' + ', '.join(material) + '\n' + 'Количество в упаковке: ' + ', '.join(count))

