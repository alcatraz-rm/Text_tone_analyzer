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

from Python.Services.ExceptionsHandler import ExceptionsHandler
from Python.Services.Logger import Logger


# NOTE: This module doesn't work, because there is a problem with module PyAudio

class SpeechRecognizer:
    def __init__(self):
        # Services
        self.__recognizer = sr.Recognizer()
        self.__logger = Logger()
        self._exceptions_handler = ExceptionsHandler()

        self.__logger.info('SpeechRecognizer was successfully initialized.', __name__)

    def recognize_speech(self):
        while True:
            try:
                with sr.Microphone() as source:
                    speech = self.__recognizer.listen(source)

            except BaseException as exception:
                error_message = self._exceptions_handler.get_error_message(exception)

                self.__logger.error(error_message, __name__)
                return error_message

            try:
                text = self.__recognizer.recognize_google(speech, language="ru-RU").lower().strip()
                return text

            except BaseException as exception:
                error_message = self._exceptions_handler.get_error_message(exception)

                if isinstance(exception, sr.WaitTimeoutError):
                    self.__logger.warning(self._exceptions_handler.get_error_message(exception), __name__)
                else:
                    self.__logger.error(error_message, __name__)
                    return error_message
