# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import speech_recognition as sr
from Python.Services.Logger import Logger


class SpeechRecognizer:
    def __init__(self):
        self.__recognizer = sr.Recognizer()
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self.__logger.info('SpeechRecognizer was successfully initialized.', 'SpeechRecognizer.__init__()')

    def recognize_speech(self):
        while True:
            try:
                with sr.Microphone() as source:
                    audio = self.__recognizer.listen(source)

            except sr.RequestError:
                self.__logger.error('No microphone.', 'SpeechRecognizer.recognize_speech()')
                return 'No microphone'

            try:
                string = self.__recognizer.recognize_google(audio, language="ru-RU").lower().strip()
                return string

            except sr.UnknownValueError:
                self.__logger.error('Unknown value.', 'SpeechRecognizer.recognize_speech()')
                return 'Unknown value'

            except sr.RequestError:
                self.__logger.error('Internet connection lost.', 'SpeechRecognizer.recognize_speech()')
                return 'Internet connection lost'

            except sr.WaitTimeoutError:
                self.__logger.warning('wait timeout.', 'SpeechRecognizer.recognize_speech()')
