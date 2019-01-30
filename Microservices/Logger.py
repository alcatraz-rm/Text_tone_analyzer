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

import inspect
import os
import platform
import sys
from datetime import datetime

from Python.Services.Singleton import Singleton


# TODO: fix bug with method name detecting (using inspect)

class Logger(metaclass=Singleton):
    def __init__(self):
        # Data
        self._wd = os.getcwd()
        self._platform = platform.system().lower()
        self._start_time = None
        self._path_to_current_log = None
        self._path_to_logs = None

        self._configure()

    def _find_main_directory(self):
        max_nesting_level = 5
        nesting_level = 0

        while 'Data' not in os.listdir(os.getcwd()):
            os.chdir('..')

            nesting_level += 1

            if nesting_level > max_nesting_level:
                exit(-1)

        path_to_data = os.path.abspath(os.path.join(os.getcwd(), 'Data'))
        self._path_to_logs = os.path.join(path_to_data, 'Logs')

        os.chdir(self._wd)

    def _configure(self):
        self._find_main_directory()

        if not os.path.exists(self._path_to_logs):
            os.mkdir(self._path_to_logs)

        self._start_time = str(datetime.now()).replace(':', '-')

        with open(os.path.join(self._path_to_logs, f'log_{self._start_time}.log'), 'w', encoding='utf-8') as log:
            log.write(f'Platform: {self._platform}\n')
            log.write(f'WD: {self._wd}\n')
            log.write(f'Start time: {self._start_time}\n')

        self._path_to_current_log = os.path.join(self._path_to_logs, f'log_{self._start_time}.log')

    def page_break(self):
        with open(self._path_to_current_log, 'a', encoding='utf-8') as log:
            log.write('\n' * 3)

    def debug(self, message: str, module_name: str):
        with open(self._path_to_current_log, 'a', encoding='utf-8') as log:
            try:
                debug_message = f'\n{str(datetime.now())} | DEBUG | {module_name}.{inspect.stack()[2][3]} | {message}\n'
            except:
                debug_message = f'\n{str(datetime.now())} | DEBUG | {module_name}.unknown | {message}\n'

            log.write(debug_message)
            print(debug_message)

    def info(self, message: str, module_name: str):
        with open(self._path_to_current_log, 'a', encoding='utf-8') as log:
            try:
                log.write(f'\n{str(datetime.now())} | INFO | {module_name}.{inspect.stack()[2][3]} | {message}\n')
            except:
                log.write(f'\n{str(datetime.now())} | INFO | {module_name}.unknown | {message}\n')

    def warning(self, message: str, module_name: str):
        with open(self._path_to_current_log, 'a', encoding='utf-8') as log:
            try:
                warning_message = f'\n{str(datetime.now())} | WARNING | {module_name}.{inspect.stack()[2][3]}' \
                                  f' | {message}\n'
            except:
                warning_message = f'\n{str(datetime.now())} | WARNING | {module_name}.unknown | {message}\n'

            log.write(warning_message)
            print(warning_message, file=sys.stderr)

    def error(self, message: str, module_name: str):
        with open(self._path_to_current_log, 'a', encoding='utf-8') as log:
            try:
                error_message = f'\n{str(datetime.now())} | ERROR | {module_name}.{inspect.stack()[2][3]} | {message}\n'
            except:
                error_message = f'\n{str(datetime.now())} | ERROR | {module_name}.unknown | {message}\n'

            log.write(error_message)
            print(error_message, file=sys.stderr)

    def fatal(self, message: str, module_name: str):
        with open(self._path_to_current_log, 'a', encoding='utf-8') as log:
            try:
                fatal_message = f'\n{str(datetime.now())} | FATAL | {module_name}.{inspect.stack()[2][3]} | {message}\n'
            except:  # catch this bug
                fatal_message = f'\n{str(datetime.now())} | FATAL | {module_name}.unknown | {message}\n'
            log.write(fatal_message)
            print(fatal_message, file=sys.stderr)

    def __del__(self):
        del self._wd
        del self._platform
        del self._start_time
        del self._path_to_current_log
        del self._path_to_logs
