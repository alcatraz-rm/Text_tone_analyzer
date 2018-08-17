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

import os
import sys
import platform
import datetime
from Python.Services.Singleton.Singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self):
        self._cwd = os.getcwd()
        self._platform = platform.system().lower()
        self._start_time = None
        self.configured = False
        self._path_to_log = None

    def configure(self):
        if self.configured:
            return

        if not os.path.exists('Logs'):
            os.mkdir('Logs')

        self._start_time = str(datetime.datetime.now()).replace(':', '-')

        with open(os.path.join('Logs', 'log_%s.log' % self._start_time), 'w', encoding='utf-8') as log:
            log.write('Platform: %s\n' % self._platform)
            log.write('CWD: %s\n' % self._cwd)
            log.write('Start time: %s\n' % self._start_time)

        self._path_to_log = os.path.join('Logs', 'log_%s.log' % self._start_time)
        self.configured = True

    def page_break(self):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            log.write('\n\n\n')

    def debug(self, message, method_name):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            log.write('\n%s | DEBUG | %s | %s\n' % (str(datetime.datetime.now()), method_name, message))

    def info(self, message, method_name):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            log.write('\n%s | INFO | %s | %s\n' % (str(datetime.datetime.now()), method_name, message))

    def warning(self, message, method_name):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            warning_message = '\n%s | WARNING | %s | %s\n' % (str(datetime.datetime.now()), method_name, message)
            log.write(warning_message)
            print(warning_message, file=sys.stderr)

    def error(self, message, method_name):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            error_message = '\n%s | ERROR | %s | %s\n' % (str(datetime.datetime.now()), method_name, message)
            log.write(error_message)
            print(error_message, file=sys.stderr)

    def fatal(self, message, method_name):
        with open(self._path_to_log, 'a', encoding='utf-8') as log:
            fatal_message = '\n%s | FATAL | %s | %s\n' % (str(datetime.datetime.now()), method_name, message)
            log.write(fatal_message)
            print(fatal_message, file=sys.stderr)
