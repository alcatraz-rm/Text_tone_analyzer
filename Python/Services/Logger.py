# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

import os
import sys
import platform
import datetime
sys.path.append(os.path.join('..', '..'))

from Python.Services.Singleton.Singleton import Singleton


class Logger(metaclass=Singleton):
    def __init__(self):
        self.cwd = os.getcwd()
        self.platform = platform.system().lower()
        self.start_time = None
        self.configured = False

    def configure(self):
        if not os.path.exists(os.path.join('..', 'Logs')):
            os.mkdir(os.path.join('..', 'Logs'))

        self.start_time = str(datetime.datetime.now()).replace(':', '-')

        with open(os.path.join('logs', 'log_%s.log' % self.start_time), 'w', encoding='utf-8') as log:
            log.write('Platform: %s\n' % self.platform)
            log.write('CWD: %s\n' % self.cwd)
            log.write('Start time: %s\n' % self.start_time)

        self.configured = True

    def debug(self, message, method_name):
        with open(os.path.join('logs', 'log_%s.log' % self.start_time), 'a', encoding='utf-8') as log:
            log.write('\n%s | DEBUG | %s | %s\n' % (str(datetime.datetime.now()), method_name, message))

    def info(self, message, method_name):
        with open(os.path.join('logs', 'log_%s.log' % self.start_time), 'a', encoding='utf-8') as log:
            log.write('\n%s | INFO | %s | %s\n' % (str(datetime.datetime.now()), method_name, message))

    def warning(self, message, method_name):
        with open(os.path.join('logs', 'log_%s.log' % self.start_time), 'a', encoding='utf-8') as log:
            warning_message = '\n%s | WARNING | %s | %s\n' % (str(datetime.datetime.now()), method_name, message)
            log.write(warning_message)
            print(warning_message)

    def error(self, message, method_name):
        with open(os.path.join('logs', 'log_%s.log' % self.start_time), 'a', encoding='utf-8') as log:
            error_message = '\n%s | ERROR | %s | %s\n' % (str(datetime.datetime.now()), method_name, message)
            log.write(error_message)
            print(error_message)

    def fatal(self, message, method_name):
        with open(os.path.join('logs', 'log_%s.log' % self.start_time), 'a', encoding='utf-8') as log:
            fatal_message = '\n%s | FATAL | %s | %s\n' % (str(datetime.datetime.now()), method_name, message)
            log.write(fatal_message)
            print(fatal_message)
