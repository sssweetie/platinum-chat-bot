## -*- coding: utf-8 -*-
import requests
import pytz
import re
from datetime import datetime
from time import sleep

# Адрес нашего бота (без указания запроса)
url = 'https://api.telegram.org/bot5767584645:AAEeqnAucht38zYfYc0R4LtaZFvYLS9a5uk/'

# Получаем JSON-строку ответа на запрос getUpdates
def get_updates_json():
    params = {'timeout': 100, 'offset': None}     # Ждём ответа на протяжении заданного в параметре timeout числа секунд
    response = requests.get(url + 'getUpdates', data=params)  # Выполняем Get-запрос, возвращается объект ответа
    return response.json()                        # Из объекта ответа берём JSON                    # Из объекта ответа берём JSON

# Получить последнее событие от бота


def last_update(response_json):
    # Обращаемся к словарю по ключу result
    results = response_json['result']
    # Последнее событие - последнее по порядку минус 1, т.к. нумерация с нуля
    last_update_index = len(results) - 1
    return results[last_update_index]       # Возвращаем последнее событие

# Получаем идентификатор чата, от которого пришло сообщение


def get_chat_id(result_json):
    # Смотрим по JSON строке: message -> chat -> id
    return result_json['message']['chat']['id']

# Отправляем пришедшее событие назад

def get_update_id(updates_json):
    return (updates_json["update_id"]), (updates_json["message"]["text"])

def send_message(chat_id, text):
    # Формируем параметры запроса: куда и что отправяем
    params = {'chat_id': chat_id, 'text': text}
    # Отправляем Post-запрос, возвращаем объект ответа
    return requests.post(url + 'sendMessage', data=params)
# Функция - точка входа в программу
def main():
  # Бот работает в вечном цикле, нужно будет принудительно останавливать свою программу
  last_update_id, _ = get_update_id(last_update(get_updates_json())) # Получаем идентификатор самого последнего события
  while True:
    _, message = get_update_id(last_update(get_updates_json()))
    updates_json = last_update(get_updates_json())    # Получаем последнее событие на текущий момент
    current_update_id = get_update_id(updates_json)   # Получаем его идентификатор
    date_message = (message.split(",",1))
    date_message = date_message[0][5:]
    output = ""

    if (last_update_id != current_update_id[0]) and  re.search("/add " + '\d\d.\d\d.\d{4}, ' + "\w{3,}?, "  + "\d{1,}, \d{1,}, \d{1,}", message) and date_message == datetime.now(pytz.timezone("Europe/Moscow")).strftime("%d.%m.%Y"):
      text_file = open("sample.txt", "a")
      text_file.write(message + "\n")
      text_file.close()
      send_message(get_chat_id(updates_json), "Запись успешно сохранена!")
      last_update_id = current_update_id[0]
      _, message = get_update_id(last_update(get_updates_json()))
      
    elif (last_update_id != current_update_id[0]) and  (message == "/help"):
      send_message(get_chat_id(updates_json), "/add - add new record to file. Follow the syntax: /add 20.20.2020, Жим_Лежа, 4, 12, 60\n/del - delete the file.\n/show - show all records from current date. Follow the syntax: /show 20.20.2020\n/help - list of commands")
      last_update_id = current_update_id[0]
      _, message = get_update_id(last_update(get_updates_json()))
    elif (last_update_id != current_update_id[0]) and  (message == "/del"):
      text_file = open("sample.txt", "w")
      text_file.close()
      send_message(get_chat_id(updates_json), "Записи удалены")
      last_update_id = current_update_id[0]
      _, message = get_update_id(last_update(get_updates_json()))

    elif (last_update_id != current_update_id[0]) and (re.search("/show " + "\d\d.\d\d.\d{4}", message)):
      message = message.split(" ")[1]
      text_file = open("sample.txt", "r")
      lines = text_file.readlines()
      text_file.close()
      for line in lines:
        line_modify = (line[4:].replace(" ", "").split(","))
        line_date = line_modify[0]
        line_modify = ",".join(line_modify)
        if(line_date == message):
          output = output + line_modify
        elif(line_date != message):
          message = line_date
          send_message(get_chat_id(updates_json), output)
          output = line_modify
      send_message(get_chat_id(updates_json), output)
      last_update_id = current_update_id[0]
      _, message = get_update_id(last_update(get_updates_json()))

    elif (last_update_id != current_update_id[0]):
      send_message(get_chat_id(updates_json), "Запись не сохранена! Проверьте правильность написания введённых данных.")
      last_update_id = current_update_id[0]
      _, message = get_update_id(last_update(get_updates_json()))
    
    sleep(1)    # Ждём одну секунду, не забудьте про эту функцию, чтобы наш код не слал постоянно большое количество запросов на сервер Telegram
 
if __name__ == '__main__':  
    main()

