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

users = dict(dict())

def writeMessage(user_id, message):
    vk.method('messages.send', {'user_id': user_id, 'message': message})


def writeMessageChat(user_id, message):
    vk.method('messages.send', {'chat_id': user_id, 'message': message})


def writeMessageSticker(user_id, sticker):
    vk.method('messages.send', {'user_id': user_id, 'sticker_id': sticker})

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
            except Exception as e:
                writeMessage(userId, e)
    time.sleep(1)
con.close()