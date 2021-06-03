# -*- coding: utf-8 -*-

from operator import le
from typing import Counter
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
            result = []
            for title in current_Lst:
                result.append(title)

            if len('\n'.join(result)) >= 1024:
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
                    'text' : '\n'.join(result),
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
                    for title in current_Lst:
                        if title.lower() in row["title"].lower():
                            
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
        counter = 1         
        for i in text:
            print('Ход')            
            if not current_Lst: 
                if len(i) > 6:
                    imod = i[0:-2]
                elif 3 < len(i) <= 6:
                    imod = i[0:-1]
                else:
                    imod = i
                lst_2 = {}    
                result = []        
                for row in lst:
                    if imod in row["title"].lower() or i in row["table2"]:                         
                        result.append(row["title"])
                        # lst_2.append([row['title'], row['table2']])
                        lst_2[row['title']] = row['table2']
                        # lst_2['table2'] = row['table2']                        
                        # lst_2.append(row['table2'])

                         
                if lst_2: 
                    print('done')            
                    
                    current_Lst = lst_2
                    # for row in current_Lst:
                    #     print(row['title'])
                    
                    
                        
                    diameter = []
                    lenght = []
                    slot = []
                    appointment = []
                    count = []
                    base = []
                    weight = []
                    ready = []
                    material = []

                    done1 = 0
                    done2 = 0
                    done3 = 0
                    for title in current_Lst:  
                        if imod.lower() in 'саморезы' or 'саморез' in title.lower():
                            if current_Lst[title][1].lower() == 'кровельный':
                                if 'Количество в упаковке:' in current_Lst[title]:
                                    count.append(current_Lst[title][current_Lst[title].index('Количество в упаковке:')+1])
                                diameter.append(current_Lst[title][current_Lst[title].index('Диаметр:') + 1])
                                lenght.append(current_Lst[title][current_Lst[title].index('Длина:')+1])     
                                appointment.append(current_Lst[title][current_Lst[title].index('Тип:')+1]) 
                                
                            else: 
                                if 'Количество в упаковке:' in current_Lst[title]:
                                    count.append(current_Lst[title][current_Lst[title].index('Количество в упаковке:')+1])
                                diameter.append(current_Lst[title][current_Lst[title].index('Диаметр:') + 1])
                                lenght.append(current_Lst[title][current_Lst[title].index('Длина:')+1])        
                                appointment.append(current_Lst[title][current_Lst[title].index('Назначение:')+1])
                                slot.append(current_Lst[title][current_Lst[title].index('Тип шлица:')+1])
                            done1 = 1
                        
                        elif imod.lower() in 'штукатурка' or 'штукатур' in title.lower():
                            if 'Основа:' in current_Lst[title]:
                                base.append(current_Lst[title][current_Lst[title].index('Основа:')+1])
                            if 'Вес:' in current_Lst[title]:
                                weight.append(current_Lst[title][current_Lst[title].index('Вес:')+1])
                            if 'Готовность:' in current_Lst[title]:
                                ready.append(current_Lst[title][current_Lst[title].index('Готовность:')+1])
                            done2 = 1
                        
                        elif imod.lower() in 'шпилька' or 'шпиль' in title.lower():
                            print("Зашел")
                            if 'Диаметр резьбы:' in current_Lst[title]:
                                diameter.append(current_Lst[title][current_Lst[title].index('Диаметр резьбы:')+1])
                            if 'Длина:' in current_Lst[title]:
                                lenght.append(current_Lst[title][current_Lst[title].index('Длина:')+1])
                            if 'Количество в упаковке:' in current_Lst[title]:
                                count.append(current_Lst[title][current_Lst[title].index('Количество в упаковке:')+1])     
                            if 'Материал:' in current_Lst[title]:
                                material.append(current_Lst[title][current_Lst[title].index('Материал:')+1])    
                            done3 = 1
                    if counter == len(text) and done1:
                        diameter = set(diameter)
                        lenght = set(lenght)
                        slot = set(slot)
                        appointment = set(appointment)
                        count = set(count)
                        if len('\n'.join(result)) >= 1024:                               
                            return {
                            'response' : {
                                'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Диаметр: ' + ', '.join(diameter) + '\n' + 'Длина: ' + ', '.join(lenght) + '\n' + 'Тип шлица: ' + ', '.join(slot) + '\n' + 'Назначение: ' + ', '.join(appointment)+ '\n' + 'Количество в упаковке: ' + ', '.join(count),
                                'end_session': False
                                },    
                                "application_state": {
                                "value": current_Lst
                                },            
                                'version': '1.0'
                            }   
                        else:
                            return {
                            'response' : {
                                'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Диаметр: ' + ', '.join(diameter) + '\n' + 'Длина: ' + ', '.join(lenght) + '\n' + 'Тип шлица: ' + ', '.join(slot) + '\n' + 'Назначение: ' + ', '.join(appointment)+ '\n' + 'Количество в упаковке: ' + ', '.join(count)+ '\n' + 'Вот что удалось найти: ' + ', '.join(result),
                                'end_session': False
                                },    
                                "application_state": {
                                "value": current_Lst
                                },            
                                'version': '1.0'
                            } 
                    if counter == len(text) and done2:
                        base = set(base)
                        weight = set(weight)
                        ready = set(ready)
                        if len('\n'.join(result)) >= 1024:                               
                            return {
                            'response' : {
                                'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Основа: ' + ', '.join(base) + '\n' + 'Вес: ' + ', '.join(weight) + '\n' + 'Готовность: ' + ', '.join(ready),
                                'end_session': False
                                },    
                                "application_state": {
                                "value": current_Lst
                                },            
                                'version': '1.0'
                            }   
                        else:
                            return {
                            'response' : {
                                'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Основа: ' + ', '.join(base) + '\n' + 'Вес: ' + ', '.join(weight) + '\n' + 'Готовность: ' + ', '.join(ready)+ '\n' + 'Вот что удалось найти: \n' + '\n '.join(result),
                                'end_session': False
                                },    
                                "application_state": {
                                "value": current_Lst
                                },            
                                'version': '1.0'
                            }   
                    if counter == len(text) and done3:
                        diameter = set(diameter)
                        lenght = set(lenght)
                        count = set(count)
                        material = set(material)
                        if len('\n'.join(result)) >= 1024:                               
                            return {
                            'response' : {
                                'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Диаметр: ' + ', '.join(diameter) + '\n' + 'Длина: ' + ', '.join(lenght) + '\n' + 'Материал: ' + ', '.join(material) + '\n' + 'Количество в упаковке: ' + ', '.join(count),
                                'end_session': False
                                },    
                                "application_state": {
                                "value": current_Lst
                                },            
                                'version': '1.0'
                            }   
                        else:
                            return {
                            'response' : {
                                'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Диаметр: ' + ', '.join(diameter) + '\n' + 'Длина: ' + ', '.join(lenght) + '\n' + 'Материал: ' + ', '.join(material) + '\n' + 'Количество в упаковке: ' + ', '.join(count)+ '\n' + 'Вот что удалось найти: \n' + '\n '.join(result),
                                'end_session': False
                                },    
                                "application_state": {
                                "value": current_Lst
                                },            
                                'version': '1.0'
                            }  
                           
            else: 
                if len(i) > 6:
                    imod = i[0:-2]
                elif 3 < len(i) <= 6:
                    imod = i[0:-1]
                else:
                    imod = i
                lst_2 = {}
                result = []
                print(i)
                for title in current_Lst:
                    
                    if imod in title.lower() or i.capitalize() in current_Lst[title]:
                        lst_2[title] = current_Lst[title]
                        result.append(title)
                        # lst_2.append(row[1])
                if lst_2: 
                    diameter = []
                    lenght = []
                    slot = []
                    appointment = []
                    count = []
                    base = []
                    weight = []
                    ready = []
                    material = []

                    done1 = 0
                    done2 = 0
                    done3 = 0
                    current_Lst = lst_2  
                    for title in current_Lst: 
                        if imod.lower() in 'саморезы' or 'саморез' in title.lower():
                            print("тут")                           
                            
                            
                            if current_Lst[title][1].lower() == 'кровельный':
                                if 'Количество в упаковке:' in current_Lst[title]:
                                    count.append(current_Lst[title][current_Lst[title].index('Количество в упаковке:')+1])
                                diameter.append(current_Lst[title][current_Lst[title].index('Диаметр:') + 1])
                                lenght.append(current_Lst[title][current_Lst[title].index('Длина:')+1])     
                                appointment.append(current_Lst[title][current_Lst[title].index('Тип:')+1]) 
                                
                            else: 
                                if 'Количество в упаковке:' in current_Lst[title]:
                                    count.append(current_Lst[title][current_Lst[title].index('Количество в упаковке:')+1])
                                diameter.append(current_Lst[title][current_Lst[title].index('Диаметр:') + 1])
                                lenght.append(current_Lst[title][current_Lst[title].index('Длина:')+1])        
                                appointment.append(current_Lst[title][current_Lst[title].index('Назначение:')+1])
                                slot.append(current_Lst[title][current_Lst[title].index('Тип шлица:')+1])
                            done1 = 1

                        elif imod.lower() in 'штукатурка' or 'штукатур' in title.lower():
                            if 'Основа:' in current_Lst[title]:
                                base.append(current_Lst[title][current_Lst[title].index('Основа:')+1])
                            if 'Вес:' in current_Lst[title]:
                                weight.append(current_Lst[title][current_Lst[title].index('Вес:')+1])
                            if 'Готовность:' in current_Lst[title]:
                                ready.append(current_Lst[title][current_Lst[title].index('Готовность:')+1])
                            done2 = 1
                        
                        elif imod.lower() in 'шпилька' or 'шпиль' in title.lower():
                            if 'Диаметр резьбы:' in current_Lst[title]:
                                diameter.append(current_Lst[title][current_Lst[title].index('Диаметр резьбы:')+1])
                            if 'Длина:' in current_Lst[title]:
                                lenght.append(current_Lst[title][current_Lst[title].index('Длина:')+1])
                            if 'Количество в упаковке:' in current_Lst[title]:
                                count.append(current_Lst[title][current_Lst[title].index('Количество в упаковке:')+1])     
                            if 'Материал:' in current_Lst[title]:
                                material.append(current_Lst[title][current_Lst[title].index('Материал:')+1])    
                            done3 = 1
            
                    if counter == len(text) and done1:
                        diameter = set(diameter)
                        lenght = set(lenght)
                        slot = set(slot)
                        appointment = set(appointment)
                        count = set(count)
                        if len('\n'.join(result)) >= 1024:                               
                            return {
                            'response' : {
                                'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Диаметр: ' + ', '.join(diameter) + '\n' + 'Длина: ' + ', '.join(lenght) + '\n' + 'Тип шлица: ' + ', '.join(slot) + '\n' + 'Назначение: ' + ', '.join(appointment)+ '\n' + 'Количество в упаковке: ' + ', '.join(count),
                                'end_session': False
                                },    
                                "application_state": {
                                "value": current_Lst
                                },            
                                'version': '1.0'
                            }   
                        else:
                            return {
                            'response' : {
                                'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Диаметр: ' + ', '.join(diameter) + '\n' + 'Длина: ' + ', '.join(lenght) + '\n' + 'Тип шлица: ' + ', '.join(slot) + '\n' + 'Назначение: ' + ', '.join(appointment)+ '\n' + 'Количество в упаковке: ' + ', '.join(count)+ '\n' + 'Вот что удалось найти: \n' + '\n '.join(result),
                                'end_session': False
                                },    
                                "application_state": {
                                "value": current_Lst
                                },            
                                'version': '1.0'
                            } 

                    if counter == len(text) and done2:
                        base = set(base)
                        weight = set(weight)
                        ready = set(ready)
                        if len('\n'.join(result)) >= 1024:                               
                            return {
                            'response' : {
                                'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Основа: ' + ', '.join(base) + '\n' + 'Вес: ' + ', '.join(weight) + '\n' + 'Готовность: ' + ', '.join(ready),
                                'end_session': False
                                },    
                                "application_state": {
                                "value": current_Lst
                                },            
                                'version': '1.0'
                            }   
                        else:
                            return {
                            'response' : {
                                'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Основа: ' + ', '.join(base) + '\n' + 'Вес: ' + ', '.join(weight) + '\n' + 'Готовность: ' + ', '.join(ready)+ '\n' + 'Вот что удалось найти: \n' + '\n '.join(result),
                                'end_session': False
                                },    
                                "application_state": {
                                "value": current_Lst
                                },            
                                'version': '1.0'
                            }     
                    if counter == len(text) and done3:
                            diameter = set(diameter)
                            lenght = set(lenght)
                            count = set(count)
                            material = set(material)
                            if len('\n'.join(result)) >= 1024:                               
                                return {
                                'response' : {
                                    'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Диаметр: ' + ', '.join(diameter) + '\n' + 'Длина: ' + ', '.join(lenght) + '\n' + 'Материал: ' + ', '.join(material) + '\n' + 'Количество в упаковке: ' + ', '.join(count),
                                    'end_session': False
                                    },    
                                    "application_state": {
                                    "value": current_Lst
                                    },            
                                    'version': '1.0'
                                }   
                            else:
                                return {
                                'response' : {
                                    'text' : 'Найдено ' + str(len(current_Lst)) + ' позиций со следующиим вариантами: \n''Диаметр: ' + ', '.join(diameter) + '\n' + 'Длина: ' + ', '.join(lenght) + '\n' + 'Материал: ' + ', '.join(material) + '\n' + 'Количество в упаковке: ' + ', '.join(count)+ '\n' + 'Вот что удалось найти: \n' + '\n '.join(result),
                                    'end_session': False
                                    },    
                                    "application_state": {
                                    "value": current_Lst
                                    },            
                                    'version': '1.0'
                                }  
            counter += 1  
                       
                                    
        if len(current_Lst) > 14 and len(current_Lst) != 0:     
                        
            result = []            
            for i in current_Lst:
                print(i)                
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
            result = []
            for title in current_Lst:
                result.append(title)
            response_text = {
            'response' : {
                'text' : 'Вот что удалось найти: \n' + '\n'.join(result),
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
    
    
    if current_Lst:

        response = {
                'response' : {
                    'text' : 'Привет. Чтобы что то заказать, просто скажите что, например "Закажи штукатурка". \n Чтобы выбрать новый заказ, скажите "Новый заказ". \n Доступные команды: \n Закажи, для заказов \n Расскажи поподробнее, для получения ссылки на заказ (Для работы команды, должна остаться одна позиция в поиске.) \n \n В последнем запросе ' + str(len((current_Lst))) + ' позиций \n Чтобы отобразить список, скажите "Покажи, что есть"',
                    'end_session': False
                    },
                    
                    'version': '1.0'
                }
    else:
        response = {
                'response' : {
                    'text' : 'Привет. Чтобы что то заказать, просто скажите что, например "Закажи штукатурка".  \n Чтобы выбрать новый заказ, скажите "Новый заказ". \n Доступные команды: \n Закажи, для заказов \n Расскажи поподробнее, для получения ссылки на заказ (Для работы команды, должна остаться одна позиция в поиске.)',
                    'end_session': False
                    },
                    
                    'version': '1.0'
                }
    if text:       
        response = text_search(text, lst, current_Lst)


    
    
    return response

app.run('0.0.0.0', port=5000, debug=True)