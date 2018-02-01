import speech_recognition as sr

r = sr.Recognizer()

while True:
    with sr.Microphone() as source:
        print("Скажите что-нибудь")
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
