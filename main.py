import random
import time
import sqlite3
import datetime
import json
import asyncio
from datetime import datetime, timedelta
import aiohttp
#import async as async
import vk_api
import urllib.request
#from bs4 import BeautifulSoup
#from lxml import html
#from games import Games
import messageProcessing as MP
import noAccess
# vk = vk_api.VkApi(login="", password="")
vk = vk_api.VkApi(token=noAccess.getToken())
# vk.auth()

values = {'out': 0, 'count': 20, 'time_offset': 90}

# Получить и сказать привет
setHello = ['привет', 'хай', 'алоха', 'ку', 'здарова', 'салют', 'здрям', 'дарова', 'добрый день',
            'добрый вечер', 'доброе утро', 'hello', 'good morning', 'good evening', 'здаров', 'доброй ночи']
sayRandomHello = ['И тебе привет! &#129412;', 'Ку-ку &#9786;', 'Hello my friend &#128075;',
                  'Алоха&#128074;', 'Дратути&#128515;']
sayRandomGoodMorning = ['Доброе утро &#9728;&#9728;&#9728;', 'Доброго утречка &#9728;',
                        'Смотрите, кто проснулся &#128527; Доброе утро &#9728;']
sayRandomHelloStickers = [5129, 4663, 4639, 4501, 4431, 4380, 4275, 3871, 3574, 3462]
sayRandomGoodMorningStickers = [3087, 4343, 3957, 3571]
sayRandomHelloGoodNight = ['Hello my friend! Good Night &#128075;', 'Доброй ночки &#129412;', 'Доброй ночи &#128406;']

# Получить и сказать привет/пока если бот знает юзера
sayRandomHelloKnowUser = ['И тебе привет, ', 'Ку-ку, ', 'Hello, ', 'Алоха, ', 'Дратути, ']
sayRandomHelloEmojiKnowUser = ['&#129412;', '&#9786;', '&#128075;', '&#128074;', '&#128515;']
sayRandomGoodbyeKnowUser = ['До скорой встречи, ', 'Бай бай, ', 'Пока, еще увидимся, ', 'Покусики, ', 'Goodbye, ']
sayRandomGoodbyeEmojiKnowUser = ['&#128075;', '&#9995;', '&#128060;']
sayRandomGoodEveningKnowUser = ['Добрый вечер, ', 'Доброго вечерка, ', 'Good evening, ',
                        'Добрейший вечерочек, ']
sayRandomGoodEveningEmojuKnowUser = ['&#9786;', '&#128075;', '&#128585;',
                        '&#128400;']

#  Получить и сказать пока
setGoodbye = ['пока', 'до свидания', 'покеда', 'покасики', 'пок', 'пока)', 'до встречи']
setGoodNight = ['спокойной ночи', 'сладких снов', 'приятных сновидений', 'добрых снов']
sayRandomGoodbye = ['До скорой встречи &#128075;', 'Бай бай', 'Пока, еще увидимся &#9995;', 'Покусики &#128060;',
                    'Goodbye my friend']
sayRandomGoodNight = ['Спокойной ночи &#10024;&#10024;&#10024;', 'Сладких снов <3&#129412;<3',
                      'Приятных сновидений &#128049;', 'Добрых снов :з']
sayRandomGoodEvening = ['Добрый вечер &#9786;', 'Доброго вечерка &#128075;', 'Good evening my friend &#128585;',
                        'Добрейший вечерочек &#128400;']

# справка
sayNote = ['''Мой создатель решил, что я много знаю и порезал меня :'(
            Но в будущем мой функционал станет больше\n
            Теперь я отвечаю на следующие команды:\n
           1. Приветствие (привет, хай, алоха, ку, салют).\n
           2. Изменить имя (изменить имя).\n
           3. Узнать дату и время ('время').\n
           4. Игры [число (угадать случайное число), слова(угадать загаданное слово)].\n
           5. Узнать свою статистику в играх (статистика).\n
           6. Попращаться (пока, до свидания, покеда, покасики, пок).\n
           Чтобы начать общение с ботом - поздаровайся ;-)''']
sayInfo = ['Если хочешь узнать побольше обо мне, напиши "справка"']


users = dict(dict())

con = sqlite3.connect('username.db')
cursor = con.cursor()



URL = "http://rzhunemogu.ru/RandJSON.aspx?CType=1"



answers = '''А вот и шуточки подъехали!!!
Сейчас будет смешно, зуб даю!
Шуточки заказывали?
Петросян в душе прям бушует :)
'''.splitlines()

# Cловарь для игры слова
Words = []

file = open('word_rus.txt')
for line in file:
    Words.append(line.lower())

def checkLetter(user, letter):
    if not letter in user['listLetter']:
        user['listLetter'].append(letter)
        user['listLetter'].sort()
        if user['word'].find(letter) != -1:
            for i in user['word']:
                if i == letter:
                    s = user['word'].find(letter)
                    user['encryptedWord'] = user['encryptedWord'][:s] + user['word'][s] + user['encryptedWord'][s + 1:]
                    user['word'] = user['word'][:s] + '*' + user['word'][s + 1:]
            return 2
        else:
            return 0
    else:
        return 1


def writeMessage(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message})


def writeMessageChat(user_id, message):
    vk.method('messages.send', {'chat_id': user_id, 'message': message})


def writeMessageSticker(user_id, sticker):
    vk.method('messages.send', {'user_id': user_id, 'sticker_id': sticker})



def addUser(userid, username):
    cursor.execute("INSERT INTO usersid (userid, name) VALUES ('%s','%s')" % (userid, username))
    con.commit()


def updateUser(userid, username):
    cursor.execute("UPDATE usersid SET name = '%s' WHERE userid = '%s'" % (username, userid))
    con.commit()


while True:
    response = vk.method('messages.get', values)
    if response['items']:
        values['last_message_id'] = response['items'][0]['id']
    for item in response['items']:
        if item.get('chat_id', 0) == 0:
            userId = item['user_id']
            messageUser = response['items'][0]['body'].lower()
            try:
                writeMessage(userId, MP.messageReply(users, userId, messageUser))
            except:
                writeMessage(userId,'Это сообщение сломало мне мозг (')
    time.sleep(1)
con.close()
