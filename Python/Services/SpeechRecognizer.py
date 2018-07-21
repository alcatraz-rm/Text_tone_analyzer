# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import sys
import os
import speech_recognition as sr
sys.path.append(os.path.join('..', '..'))

from Python.Services.Logger import Logger


class SpeechRecognizer:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.logger = Logger()

        if not self.logger.configured:
            self.logger.configure()

    def recognize_speech(self):
        while True:
            try:
                with sr.Microphone() as source:
                    audio = self.recognizer.listen(source)

            except sr.RequestError:
                return 'No microphone'

            try:
                string = self.recognizer.recognize_google(audio, language="ru-RU")\
                                                                        .lower().strip()
                return string

            except sr.UnknownValueError:
                return 'Unknown value'

            except sr.RequestError:
                return 'Internet connection lost'

            except sr.WaitTimeoutError:
                pass
