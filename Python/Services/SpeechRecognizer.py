# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import speech_recognition as sr
# import logging


class SpeechRecognizer():
    def __init__(self):
        self.recognizer = sr.Recognizer()

    def check_microphone(self):
        try:
            if sr.Microphone():
                return True

        except sr.RequestError:
            return False

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
                # logging.info('\nrecognised speech: %s\n' % string)
                return string

            except sr.UnknownValueError as error:
                # logging.error('\n{0}\n'.format(e))
                return 'Unknown value'

            except sr.RequestError as error:
                # logging.error('\nspeech recognition: {0}\n'.format(e))
                return 'Internet connection lost'

            except sr.WaitTimeoutError as error:
                # logging.error('\n{0}\n'.format(e))
                pass
