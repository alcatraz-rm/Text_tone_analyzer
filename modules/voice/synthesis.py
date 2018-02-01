# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import requests
from pygame import mixer
import time
import os

mixer.init()

text = input('Введите текст: ')

url = 'https://tts.voicetech.yandex.net/generate'
key = 'd5ef89bb-c6fb-4376-83bd-b5980e0b443e'

with open('speech.mp3', 'wb') as file:
    response = requests.get(url, params={
        'text': text,
        'format': 'mp3',
        'lang': 'ru-RU',
        'speaker': 'zahar',
        'emotion': 'good',
        'key': key
    })

    file.write(response.content)

mixer.music.load('speech.mp3')
mixer.music.play()
while mixer.music.get_busy():
    time.sleep(0.1)

mixer.stop()
mixer.quit()

os.remove('speech.mp3')
