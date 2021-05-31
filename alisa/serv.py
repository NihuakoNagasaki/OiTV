# -*- coding: utf-8 -*-

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
iter = 0
lst = list(records.find({}))








def text_search(text, lst, current_Lst):
    word = morph.parse(text)[0].normal_form
    if text:
        if text.lower() == 'новый заказ' or text.lower() == 'новый запрос':
            
            return {
            'response' : {
                'text' : 'Слушаю новый заказ',
                'end_session': False
                },
                "application_state": {
                "value": {}
                },
                'version': '1.0'
            }   
        if text.lower() == 'выход':
            
            return {
            'response' : {
                'text' : 'Бывай',
                'end_session': True
                },
                "application_state": {
                "value": {}
                },
                'version': '1.0'
            }      
        if text.lower() == 'покажи что есть' or text.lower() == 'покажи, что есть':
            if len('\n'.join(current_Lst)) >= 1024:
                return {
                'response' : {
                'text' : 'Слишком много вариантов, сначала уточните заказ',
                'end_session': False
                },                
                'version': '1.0'
            }
            else:
                return {
                'response' : {
                    'text' : '\n'.join(current_Lst),
                    'end_session': False
                    },                
                    'version': '1.0'
                }    
        if text.lower() == 'доступные варианты':
            if current_Lst:
                result = []
                for i in current_Lst:
                    i = i.split(" ")
                    for j in i:
                        if len(j) > 4:
                            result.append(j)
                result = set(result)
                response_text = {
                'response' : {
                    'text' : "Доступные варианты: \n" + ', '.join(result),
                    'end_session': False
                    },
                    "application_state": {
                    "value": current_Lst
                    },
                    'version': '1.0'
                }
                return response_text
            else:
                return {
                'response' : {
                    'text' : "Сначала осуществите поиск",
                    'end_session': False
                    },
                    "application_state": {
                    "value": current_Lst
                    },
                    'version': '1.0'
                }
        if text.lower() == 'расскажи подробнее' or text.lower() == 'расскажи поподробнее':
            if len(current_Lst) == 1:
                for row in lst:
                    print(current_Lst[0])
                    print(row["title"])
                    if current_Lst[0].lower() in row["title"].lower():
                        print(row)
                        return {
                        'response' : {
                        'text' : 'Категория: ' + row['category'] + '\n' + '\nНазвание: ' + row['title'] + '\n' + '\nОписание: ' + row['desc'] + '\n' + '\nЦена: ' + row['price']+ '\n',
                        'end_session': False,
                        "buttons": [
                        {
                            "title": "Перейти к товару",
                            "payload": {},
                            "url": row['link'],
                            "hide": True
                        }
                        ],     
                        },   
                                
                        'version': '1.0'
                }
            else:
                return {
                'response' : {
                    'text' : 'Сначала сократите поиск до одного варианта',
                    'end_session': False
                    },                
                    'version': '1.0'
                }    
        text = text.split(" ")
        print(text)         
        for i in text:
            print('Ход')
            if not current_Lst: 
                
                lst_2 = []            
                for row in lst:
                    if i in row["title"].lower():
                        lst_2.append(row["title"])
                         
                if lst_2: 
                    print('done')                        
                    
                    current_Lst = lst_2 
                
                                            
                
            else: 
                lst_2 = []
                print(current_Lst)
                print(len(current_Lst))
                for row in current_Lst:
                    if i in row.lower():
                        print(row)                        
                        lst_2.append(row) 
                    if lst_2: 
                        
                        current_Lst = lst_2  
                       
                                    
        if len(current_Lst) > 14 and len(current_Lst) != 0:     
            print('123')             
            result = []
            for i in current_Lst:
                i = i.split(" ")
                for j in i:
                    if len(j) > 4:
                        result.append(j)
            result = set(result)
            response_text = {
            'response' : {
                'text' : "Найдено " + str(len(current_Lst)) + " позиций , уточните запрос \n " + "Доступные варианты: \n" + ', '.join(result),
                'end_session': False
                },
                "application_state": {
                "value": current_Lst
                },
                'version': '1.0'
            }
            return response_text
        if len(current_Lst) < 14 and len(current_Lst) != 0:
            lst = lst_2            
            response_text = {
            'response' : {
                'text' : '\n'.join(current_Lst),
                'end_session': False
                },
                "application_state": {
                "value": current_Lst
                },
                'version': '1.0'
            }
            return response_text
        if len(current_Lst) == 0:                       
            response_text = {
            'response' : {
                'text' : 'Ничего не найдено',
                'end_session': False
                },                
                'version': '1.0'
            }
            return response_text
        



@app.route('/alice', methods=['POST'])
def resp():    
    text = request.json.get('request', {}).get('command')
    current_Lst = request.json.get('state').get('application').get('value')
    print(current_Lst)
    
    if current_Lst:

        response = {
                'response' : {
                    'text' : 'Привет. Чтобы что то заказать, просто скажите что, например "Закажи штукатурка". Позиция для заказа должна быть в именительном падеже. \n Чтобы выбрать новый заказ, скажите "Новый заказ". \n Доступные команды: \n Закажи, для заказов \n Расскажи поподробнее, для получения ссылки на заказ (Для работы команды, должна остаться одна позиция в поиске.) \n \n В последнем запросе ' + str(len((current_Lst))) + ' позиций \n Чтобы отобразить список, скажите "Покажи, что есть"',
                    'end_session': False
                    },
                    
                    'version': '1.0'
                }
    else:
        response = {
                'response' : {
                    'text' : 'Привет. Чтобы что то заказать, просто скажите что, например "Закажи штукатурка". Позиция для заказа должна быть в именительном падеже. \n Чтобы выбрать новый заказ, скажите "Новый заказ". \n Доступные команды: \n Закажи, для заказов \n Расскажи поподробнее, для получения ссылки на заказ (Для работы команды, должна остаться одна позиция в поиске.)',
                    'end_session': False
                    },
                    
                    'version': '1.0'
                }
    if text:       
        response = text_search(text, lst, current_Lst)


    
    
    return response

app.run('0.0.0.0', port=5000, debug=True)