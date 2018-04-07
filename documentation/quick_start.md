# Быстрый старт
Для запуска программы необходимо:
1. Скачать [здесь](https://github.com/GermanYakimov/Text_tone_analyzer/releases) последний релиз программы
или склонировать репозиторий с помощью `git clone` (в данном варианте необходимо будет вручную скачать файл `trigrams.db`
из директории `databases` и заменить его в одноименной директории локально)
2. Установить интерпретатор [Python 3.X](https://www.python.org/downloads/) на компьютер
3. Установить необходимые библиотеки:
    1. [PyQt5](https://pypi.python.org/pypi/PyQt5)
    2. [sklearn](https://pypi.python.org/pypi/sklearn)
    3. [pandas](https://pypi.python.org/pypi/pandas)
    4. [pymorphy2](https://pypi.python.org/pypi/pymorphy2)
    5. [requests](https://pypi.python.org/pypi/requests)
    6. [speech_recognition](https://pypi.python.org/pypi/SpeechRecognition)
4. В консоли перейти в Text_tone_analyzer/master
5. Запустить файл main.py

    `python main.py`
6. Ввести текст в поле ввода (либо воспользоваться голосовым вводом)
7. Нажать клавишу "Enter" или кнопку "Start"

Нормальным результатом работы программы является тональность и вероятность принадлежности текста к ней.

[Интерфейс →](./interface.md)
