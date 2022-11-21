#!/usr/bin/env python
# -*- coding: utf-8 -*-
from vk_api.longpoll import VkLongPoll, VkEventType
import vk_api
from googletrans import Translator, constants
import json
from raskladka import LayoutChanger
from datetime import datetime
import random
import time
import wikipedia

token = "token"
vk_session = vk_api.VkApi(token=token)
session_api = vk_session.get_api()
longpoll = VkLongPoll(vk_session)
upload = vk_api.VkUpload(session_api)
message_from_chat = False
wikipedia.set_lang("ru")

translator = Translator()

#func to fast read and write json
def write_file(_path, _value):
    _f = open(_path, 'w')
    _f.write(_value)
    _f.close()

def read_file(_path):
    _f = open(_path, 'r')
    _value = _f.read()
    _f.close()
    return _value

whitelist = json.loads(read_file('whitelist.json'))

#main bot func
def remove_from_whitelist(uid):
    whitelist.remove(uid)
    write_file('whitelist.json', json.dumps(whitelist))
    send("успешно")
def add_to_whitelist(uid):
    whitelist.append(uid)
    write_file('whitelist.json', json.dumps(whitelist))
    send("успешно")

def change_layout(text):
    return LayoutChanger.change(text)
def translate(mytext, lang = "ru"):
    translation = translator.translate(mytext, lang)
    return translation.text
def wiki(text):
    try:
        send(wikipedia.summary(text))
    except Exception as e:
        send(e)
def send_photo(path):
    if message_from_chat:
        vk_session.method('messages.send', {'chat_id': event.chat_id, 'attachment': path, 'random_id': 0})
    else:
        vk_session.method('messages.send', {'user_id': event.user_id, 'attachment': path, 'random_id': 0})

def send(text):
    if token in text:
        text = "токен типа не дам)"
    if message_from_chat:
        vk_session.method('messages.send', {'chat_id': event.chat_id, 'message': text, 'random_id': 0})
    else:
        vk_session.method('messages.send', {'user_id': event.user_id, 'message': text, 'random_id': 0})

print("успех")
while True:
    try:
        for event in longpoll.listen():
            if event.type == VkEventType.MESSAGE_NEW:
                msg = event.text
                message_from_chat = event.from_chat
                reply_message = None
                try:
                    reply_message = session_api.messages.get_by_id(message_ids = [event.message_id])["items"][0]["reply_message"]
                except Exception:
                    pass
                if msg.startswith("/") and (event.user_id in whitelist or event.from_me):
                    try:
                        final_msg = msg[1 : len(msg)].replace("&quot;", "'")
                        final_msg = final_msg.replace("[tab]","\t")
                        if "token" not in final_msg and "vk_session.method" not in final_msg and "messages.send" not in final_msg:
                            if "import os" in final_msg:
                                send("чел ты мне диск не форматируй")
                            else:
                                if "eval" in final_msg or "exec" in final_msg:
                                    send("юзать евал и ексес, зачем если твое сообщение я и так ексекаю? сдаётся мне это чтобы обойти систему защиты, но я и это предусмотрел")
                                else:
                                    exec(final_msg)
                        else:
                            send("токен не получишь. и методы от вк_апи вызвать не дам")
                    except Exception as e:
                        try:
                            send("Error: " + str(e))
                        except Exception:
                            print("серьёзная еррор")
                if reply_message and (event.user_id in whitelist or event.from_me):
                    if msg.startswith("translate "):
                        try:
                            send(translate(reply_message["text"], msg[len("translate ") : len(msg)]))
                        except Exception as e:
                            send("Error: " + str(e))
                    elif msg == "change layout":
                        try:
                            send(change_layout(reply_message["text"]))
                        except Exception as e:
                            send("Error: " + str(e))
    except Exception:
        pass
