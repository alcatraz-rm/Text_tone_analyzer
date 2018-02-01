# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import speech_recognition as sr

r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        audio = r.listen(source)

    try:
        string = r.recognize_google(audio, language="ru-RU").lower()
        if string == 'стоп':
            break
        else:
            print(string)
    except sr.UnknownValueError:
        print("Робот не расслышал фразу")
    except sr.RequestError as e:
        print("Ошибка сервиса; {0}".format(e))
