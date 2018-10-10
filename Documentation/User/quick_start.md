# Быстрый старт
Для запуска программы необходимо:
1. Скачать [здесь](https://github.com/GermanYakimov/Text_tone_analyzer/releases) последний релиз программы (не рекомендуется
устанавливать pre-alpha (pa) и alpha (a) релизы, так как они являются начальными и могут содержать большое
количество ошибок)
или склонировать репозиторий, выполнив команду

`git clone https://github.com/GermanYakimov/Text_tone_analyzer`

Запускать необходимо ту версию проекта, которая находится в ветке master. Чтобы переключиться на ветку master,
необходимо выполнить команду:

`git checkout master`

2. Установить интерпретатор [Python 3.7](https://www.python.org/downloads/release/python-370/) на компьютер.
3. Установить необходимые библиотеки ([инструкция по установке](./install_packages.md)):
    1. [PyQt5](https://pypi.python.org/pypi/PyQt5)
    2. [sklearn](https://pypi.python.org/pypi/sklearn)
    3. [pandas](https://pypi.python.org/pypi/pandas)
    4. [pymorphy2](https://pypi.python.org/pypi/pymorphy2)
    5. [requests](https://pypi.python.org/pypi/requests)
    6. [speech_recognition](https://pypi.python.org/pypi/SpeechRecognition)
    7. [gensim](https://pypi.org/project/gensim/)
    8. [chardet](https://pypi.org/project/chardet/)
4. В консоли перейти в Text_tone_analyzer/Python
5. Запустить файл Demo.py

    `python Demo.py`
6. Ввести текст в поле ввода (с помощью клавиатуры, файлового диалога или голосового ввода)
7. Нажать клавишу "Enter" или кнопку "Start"

Нормальным результатом работы программы является тональность и вероятность принадлежности текста к ней.

[Интерфейс →](./interface.md)
