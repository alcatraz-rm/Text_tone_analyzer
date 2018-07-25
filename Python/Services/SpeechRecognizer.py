# Copyright © 2018. All rights reserved.
# Author: German Yakimov

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

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
