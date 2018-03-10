import random
import time
import sqlite3
import datetime
import json
from datetime import datetime, timedelta
import aiohttp
import async as async
import vk_api
import urllib.request

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



def messageReply(users, userId, messageUser):
    now = datetime.now()
    londonTimeNow = datetime.utcnow()
    hour = datetime.time(now)
    if users.get(userId, '666') == '666':  # Загрузка пользователя из бд или создание нового
        cursor.execute("SELECT * from usersid WHERE userid=  '%s'" % userId)
        # print(cursor.fetchall())
        newUsers = cursor.fetchall()
        if newUsers == []:
            users[userId] = dict(Hello=0, Game=0, liveGame=0, word='', encryptedWord='',
                                 listLetter=[], wordAnswer='', UserName=0, numberAnswer=0, name=None, Greenwich=0,
                                 gameWord=0, gameWordWin=0, gameNumber=0, gameNumberWin=0,
                                 differenceFromGreenwich=0)
        else:
            newUser = newUsers[0]
            users[userId] = dict(Hello=0, Game=0, liveGame=0, word=None, encryptedWord=None,
                                 listLetter=[], wordAnswer=None, UserName=0, numberAnswer=0, Greenwich=0,
                                 name=newUser[1],
                                 gameWord=newUser[2], gameWordWin=newUser[3], gameNumber=newUser[4],
                                 gameNumberWin=newUser[5], differenceFromGreenwich=newUser[6])

    if users[userId]['Greenwich'] == 1:
        if response['items'][0]['body'].isdigit():
            cursor.execute(
                "UPDATE usersid SET differenceFromGreenwich = '%s' WHERE userid = '%s'" % (int(messageUser), userId))
            con.commit()
            return (
                         'Время успешно установлено. Настройка завереша. Теперь тебе доступен весь функционал бота')
            users[userId]['Greenwich'] = 0

    if users[userId]['UserName'] == 1:
        addUser(userId, response['items'][0]['body'])
        users[userId]['name'] = response['items'][0]['body']
        users[userId]['UserName'] = 0
        return ( 'Окей, теперь тебя зовут - ' + response['items'][0]['body'])
        return ( '''И последнее. Это для найстройки времени! Какая у тебя разница 
                                во времени от нулевого меридиана (Гринвича UTC +0). Например, в UTC +0 входит Лондон.
                                Сейчас там: ''' + nowLondon.strftime("%H:%M:%S"))
        users[userId]['Greenwich'] = 1

    if users.get(userId, dict(Hello=1, UserName=0))['UserName'] == 2:
        updateUser(userId, response['items'][0]['body'])
        users[userId]['UserName'] = 0
        users[userId]['name'] = response['items'][0]['body']
        return ( 'Окей, теперь тебя зовут - ' + response['items'][0]['body'])

    cursor.execute("SELECT name FROM usersid WHERE userid = '%s'" % userId)
    nameUser = cursor.fetchall()
    if nameUser != []:
        if messageUser in setHello:
            users[userId]['Hello'] = 1
            if 4 < hour.hour < 12:
                return ( random.choice(sayRandomGoodMorning))
                return ( sayInfo)
            elif 12 <= hour.hour < 18:
                return (
                             random.choice(sayRandomHelloKnowUser) + users[userId]['name'] + '! '
                             + random.choice(sayRandomHelloEmojiKnowUser))
                return ( sayInfo)
            elif 00 <= hour.hour < 4 & 21 < hour.hour <= 00:
                return ( random.choice(sayRandomHelloGoodNight) + users[userId]['name'])
                return ( sayInfo)
            else:
                return ( random.choice(sayRandomGoodEveningKnowUser) + users[userId]['name'] + '! '
                             + random.choice(sayRandomGoodbyeEmojiKnowUser))
                return ( sayInfo)
    else:
        if messageUser in setHello:
            users[userId]['Hello'] = 1
            users[userId]['UserName'] = 1
            if 4 < hour.hour < 12:
                return ( random.choice(sayRandomGoodMorning))
                return ( sayInfo)
                return (
                             'Похоже, я тебя не знаю :C\nСейчас я проведу для себя небольшу настроечку, чтобы нам было приятней общаться \nКак ты хочешь, чтобы я тебя называл?')
            elif 12 <= hour.hour < 18:
                return ( random.choice(sayRandomHello))
                return ( sayInfo)
                return (
                             'Похоже, я тебя не знаю :C\nСейчас я проведу для себя небольшу настроечку, чтобы нам было приятней общаться\nКак ты хочешь, чтобы я тебя называл?')
            elif 00 <= hour.hour < 4 & 21 < hour.hour <= 00:
                return ( random.choice(sayRandomHelloGoodNight))
                return ( sayInfo)
                return (
                             'Похоже, я тебя не знаю :C\nСейчас я проведу для себя небольшу настроечку, чтобы нам было приятней общаться \nКак ты хочешь, чтобы я тебя называл?')
            else:
                return ( random.choice(sayRandomGoodEvening))
                return ( sayInfo)
                return (
                             'Похоже, я тебя не знаю :C\nСейчас я проведу для себя небольшу настроечку, чтобы нам было приятней общаться \nКак ты хочешь, чтобы я тебя называл?')

    if messageUser == 'изменить имя':
        users[userId]['UserName'] = 2
        return ( 'Выбери себе новое имя')

    if users[userId]['Hello'] == 1:
        if users.get(userId, dict(Game=0))['Game'] != 0:
            if messageUser == '!выход':
                users[userId]['Game'] = 0
                return ( 'Вы вышли из игры')

    if users.get(userId, dict(Game=0))['Game'] == 2:
        if messageUser.isdigit():
            if int(messageUser) == users[userId]['numberAnswer']:
                users[userId]['Game'] = 0
                users[userId]['gameNumberWin'] = (users[userId]['gameNumberWin'] * users[userId]['gameNumber']
                                                  + users[userId]['liveGame']) / (users[userId]['gameNumber'] + 1)
                users[userId]['gameNumber'] += 1
                cursor.execute("UPDATE usersid SET gameNumber = '%s', gameNumberWin = '%s' WHERE userid = '%s'" % (
                    users[userId]['gameNumber'], users[userId]['gameNumberWin'], userId))
                con.commit()
                return (
                             'Молодец!!! Ты угадал(-а) число, количество попыток: ' + str(users[userId]['liveGame']))
            else:
                if int(messageUser) < users[userId]['numberAnswer']:
                    users[userId]['liveGame'] += 1
                    return ( 'Число больше чем ' + messageUser)
                else:
                    users[userId]['liveGame'] += 1
                    return ( 'Число меньше чем ' + messageUser)

    if users.get(userId, dict(Game=0))['Game'] == 1:
        if messageUser == users[userId]['wordAnswer']:
            users[userId]['Game'] = 0
            users[userId]['gameWordWin'] += 1
            cursor.execute("UPDATE usersid SET gameWordWin = '%s' WHERE userid = '%s'"
                           % (users[userId]['gameWordWin'], userId))
            con.commit()
            return ( 'Ураааа!!!! Молодец ты угадал(-а) слово - '
                         + users[userId]['wordAnswer'].upper())
        elif len(messageUser) == 1 & messageUser.isalpha():
            setResult = checkLetter(users[userId], messageUser)
            stringLetters = ''
            for i in users[userId]['listLetter']:
                if i == users[userId]['listLetter'][-1]:
                    stringLetters += i + '.'
                else:
                    stringLetters += i + ', '
            if setResult == 2:
                return ( '[ ' + users[userId]['encryptedWord'] + ' ]\n'
                             + '❤' * users[userId]['liveGame']
                             + '💔' * (10 - users[userId]['liveGame'])
                             + '\nСписок использованных букв: ' + stringLetters
                             )
                if users[userId]['encryptedWord'].find('*') == -1:
                    users[userId]['Game'] = 0
                    users[userId]['gameWordWin'] += 1
                    cursor.execute("UPDATE usersid SET gameWordWin = '%s' WHERE userid = '%s'"
                                   % (users[userId]['gameWordWin'], userId))
                    con.commit()
                    return ( 'Ураааа!!!! Молодец ты угадал(-а) слово - '
                                 + users[userId]['encryptedWord'].upper())
            elif setResult == 1:
                return (
                             '[ ' + users[userId]['encryptedWord'] + ' ]' + '\nЭта буква была названа \n'
                             + '❤' * users[userId]['liveGame']
                             + '💔' * (10 - users[userId]['liveGame'])
                             + '\nСписок использованных букв: ' + stringLetters)
            else:
                users[userId]['liveGame'] -= 1
                if users[userId]['liveGame'] == 0:
                    return ( 'Game over! &#128546; \nЗагаданное слово было: '
                                 + users[userId]['wordAnswer'].upper()
                                 + '\nПовезет в другой раз &#128521;')
                    users[userId]['Game'] = 0
                else:
                    return ( '[ ' + users[userId]['encryptedWord'] + ' ]\n'
                                 + '\nТакой буквы нет'
                                 + '❤' * users[userId]['liveGame'] + '💔' * (10 - users[userId]['liveGame'])
                                 + '\nСписок использованных букв: ' + stringLetters)

    if messageUser == 'число':
        users[userId]['Game'] = 2
        users[userId]['liveGame'] = 1
        users[userId]['numberAnswer'] = random.randint(0, 1000)
        return (
                     'Я загадал число в диапазоне [0:1000], попробуй угадать\n Чтобы выйти из игры, напиши "!выход')

    if messageUser == 'слова':
        word = random.choice(Words)
        word = word[0: len(word) - 1]
        encryptedWord = ''
        for i in word:
            i = '*'
            encryptedWord += i
        users[userId]['Game'] = 1
        users[userId]['liveGame'] = 10
        users[userId]['word'] = word
        users[userId]['encryptedWord'] = encryptedWord
        users[userId]['listLetter'] = []
        users[userId]['wordAnswer'] = word
        firstLetter = checkLetter(users[userId], word[0])
        if len(word) > 5:
            lastLetter = checkLetter(users[userId], word[-1])
        if users[userId]['word'].find('-') != -1:
            defisLetter = checkLetter(users[userId], '-')
        users[userId]['gameWord'] += 1
        cursor.execute("UPDATE usersid SET gameWord = '%s' WHERE userid = '%s'"
                       % (users[userId]['gameWord'], userId))
        con.commit()
        return ( 'Я загадал слово [ ' + users[userId][
            'encryptedWord'] + ' ]\n' + 'У тебя' + '❤' * 10 + ' попыток.\n' + 'Чтобы выйти напиши "!выход"\nВыходя из игры, Вы признаете свое поражение')

    if messageUser == 'статистика':
        try:
            return ( 'В ИГРЕ СЛОВА:\nКоличество игр: ' + str(users[userId]['gameWord'])
                         + '\nКоличество угаданных слов: ' + str(users[userId]['gameWordWin'])
                         + '\nПроцент побед: ' + str((users[userId]['gameWordWin'] / users[userId]['gameWord']) * 100)[
                                                 0:6]
                         + '\nВ ИГРЕ ЧИСЛО:\nКоличество игр: ' + str(users[userId]['gameNumber'])
                         + '\nСреднее число попыток: ' + str(users[userId]['gameNumberWin']))
        except ZeroDivisionError:
            return ( 'В ИГРЕ СЛОВА:\nКоличество игр: ' + str(users[userId]['gameWord'])
                         + '\nКоличество угаданных слов: ' + str(users[userId]['gameWordWin'])
                         + '\nПроцент побед: сыграй хотя бы одну игру'
                         + '\nВ ИГРЕ ЧИСЛО:\nКоличество игр: ' + str(users[userId]['gameNumber'])
                         + '\nСреднее число попыток: ' + str(users[userId]['gameNumberWin']))
    # Сказать пока
    if users.get(userId, dict(Hello=0))['Hello'] != 0:
        if 1 <= hour.hour < 4 & 21 < hour.hour <= 24:
            for i in setGoodNight:
                if messageUser.find(i) != -1:
                    return ( random.choice(sayRandomGoodNight))
                    users.pop(userId)
        else:
            if messageUser in setGoodbye:
                return ( random.choice(sayRandomGoodbyeKnowUser) + users[userId]['name'] + '! '
                             + random.choice(sayRandomGoodbyeEmojiKnowUser))
                users.pop(userId)

    if messageUser == 'справка':
        return ( sayNote)

    # Узнать сколько сейчас времени
    if messageUser == 'время':
        cursor.execute("SELECT differenceFromGreenwich FROM usersid WHERE userid = '%s'" % userId)
        userTime = cursor.fetchall()
        timeDifference = timedelta(hours=userTime[0][0])
        userTimeNow = londonTimeNow + timeDifference
        return ( 'Сегодня: ' + userTimeNow.strftime("%d-%m-%Y") + '. Сейчас: '
                     + userTimeNow.strftime("%H:%M:%S"))

        # if messageUser == 'шутка':
        #         with aiohttp.ClientSession() as sess:
        #             with sess.get(URL) as resp:
        #                 text = resp.text()
        #                 joke = "".join(text.replace('\r\n', '\n').split("\"")[3:-1])
        #         return (  str(joke))

        #     #      with aiohttp.ClientSession() as sess:
        #     #          with sess.get(URL) as resp:
        #     #              text = await resp.text()
        #     res = urllib.request.urlopen(URL).read()
        #     soup = BeautifulSoup(res)
        #     res1 = soup.html.body.p.string
        #     parsed_string = json.loads(res1)
        #     print(parsed_string['content'])
        # return ( parsed_string['content'])
        # return ( text)
        # joke = "".join(text.replace('\r\n', '\n').split("\"")[3:-1])
        # msg.answer(random.choice(answers) + '\n' + str(joke))
