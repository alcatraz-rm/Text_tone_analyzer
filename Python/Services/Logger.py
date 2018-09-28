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

import datetime
import os
import platform
import sys

from Python.Services.Singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self):
        self._wd = os.getcwd()
        self._platform = platform.system().lower()
        self._start_time = None
        self._path_to_log = None

        self._configure()

    def _configure(self):
        if not os.path.exists('Logs'):
            os.mkdir('Logs')

        self._start_time = str(datetime.datetime.now()).replace(':', '-')

        with open(os.path.join('Logs', f'log_{self._start_time}.log'), 'w', encoding='utf-8') as log:
            log.write(f'Platform: {self._platform}\n')
            log.write(f'WD: {self._wd}\n')
            log.write(f'Start time: {self._start_time}\n')

        self._path_to_log = os.path.join('Logs', f'log_{self._start_time}.log')

    def page_break(self):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            log.write('\n' * 3)

    def debug(self, message, method_name):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            debug_message = f'\n{str(datetime.datetime.now())} | DEBUG | {method_name} | {message}\n'
            log.write(debug_message)
            print(debug_message)

    def info(self, message, method_name):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            log.write(f'\n{str(datetime.datetime.now())} | INFO | {method_name} | {message}\n')

    def warning(self, message, method_name):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            warning_message = f'\n{str(datetime.datetime.now())} | WARNING | {method_name} | {message}\n'
            log.write(warning_message)
            print(warning_message, file=sys.stderr)

    def error(self, message, method_name):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            error_message = f'\n{str(datetime.datetime.now())} | ERROR | {method_name} | {message}\n'
            log.write(error_message)
            print(error_message, file=sys.stderr)

    def fatal(self, message, method_name):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            fatal_message = f'\n{str(datetime.datetime.now())} | FATAL | {method_name} | {message}\n'
            log.write(fatal_message)
            print(fatal_message, file=sys.stderr)
