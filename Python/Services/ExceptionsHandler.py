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

import sqlite3

import requests

from Python.Services.Logger import Logger


class ExceptionsHandler:
    def __init__(self):
        self.__logger = Logger()

        self._request_exceptions = [type(item) for item in [requests.ConnectionError(), requests.HTTPError(),
                                    requests.TooManyRedirects(), requests.Timeout(), requests.TooManyRedirects(),
                                    requests.RequestException(), requests.ConnectTimeout(), requests.ReadTimeout()]]

        self._system_errors = [type(item) for item in [KeyError(), AttributeError(), IndexError(),
                                                       ZeroDivisionError(), SystemError(), ValueError(),
                                                       AssertionError()]]

        self._file_errors = [type(item) for item in [FileExistsError(), FileNotFoundError()]]
        self._database_errors = [type(item) for item in [sqlite3.Error(), sqlite3.DataError(),
                                                         sqlite3.ProgrammingError(), sqlite3.DatabaseError(),
                                                         sqlite3.NotSupportedError(), sqlite3.IntegrityError(),
                                                         sqlite3.InterfaceError(), sqlite3.InternalError(),
                                                         sqlite3.OperationalError()]]

        self.__logger.info('ExceptionsHandler was successfully initialized.', 'ExceptionsHandler.__init__()')

    @staticmethod
    def _handle_system_exception(exception):
        if isinstance(exception, KeyError):
            return 'Key error occurred.'
        elif isinstance(exception, AttributeError):
            return 'AttributeError occurred.'
        elif isinstance(exception, IndexError):
            return 'Index error occurred.'
        elif isinstance(exception, ZeroDivisionError):
            return 'ZeroDivisionError occurred.'
        elif isinstance(exception, SystemError):
            return 'SystemError occurred.'
        elif isinstance(exception, ValueError):
            return 'ValueError occurred.'
        elif isinstance(exception, AssertionError):
            return 'Assertion error occurred.'

    @staticmethod
    def _handle_file_exception(exception):
        if isinstance(exception, FileNotFoundError):
            return 'FileNotFoundError occurred.'
        elif isinstance(exception, FileExistsError):
            return 'FileExistsError occurred.'

    @staticmethod
    def _handle_database_exception(exception):
        if isinstance(exception, sqlite3.OperationalError):
            return 'sqlite3.Operational occurred.'
        elif isinstance(exception, sqlite3.ProgrammingError):
            return 'sqlite3.ProgrammingError occurred.'
        elif isinstance(exception, sqlite3.InternalError):
            return 'sqlite3.InternalError occurred.'
        elif isinstance(exception, sqlite3.InterfaceError):
            return 'sqlite3.InterfaceError occurred.'
        elif isinstance(exception, sqlite3.IntegrityError):
            return 'sqlite3.IntegrityError occurred.'
        elif isinstance(exception, sqlite3.NotSupportedError):
            return 'sqlite3.NotSupportedError occurred.'
        elif isinstance(exception, sqlite3.DatabaseError):
            return 'sqlite3.DatabaseError occurred.'
        elif isinstance(exception, sqlite3.DataError):
            return 'sqlite3.DataError occurred.'
        elif isinstance(exception, sqlite3.Error):
            return 'sqlite3.Error occurred.'

    @staticmethod
    def _handle_request_exception(exception):
        if isinstance(exception, requests.ConnectionError):
            return 'Problems with connection (requests.ConnectionError).'
        elif isinstance(exception, requests.HTTPError):
            return 'HHTP request return unsuccessful status code (requests.HTTPError).'
        elif isinstance(exception, requests.Timeout):
            return 'Request times out (requests.Timeout).'
        elif isinstance(exception, requests.TooManyRedirects):
            return 'Request exceeds the configured number of maximum redirections (requests.TooManyRedirects).'
        elif isinstance(exception, requests.ConnectTimeout):
            return 'ConnectTimeout (requests.ConnectTimeout).'
        elif isinstance(exception, requests.ReadTimeout):
            return 'ReadTimeout (requests.ReadTimeout).'
        else:
            return 'Request exception (requests.RequestException).'

    def get_error_message(self, exception):
        error_message = 'Base exception occurred.'

        if type(exception) in self._system_errors:
            error_message = self._handle_system_exception(exception)

        elif type(exception) in self._file_errors:
            error_message = self._handle_file_exception(exception)

        elif type(exception) in self._request_exceptions:
            error_message = ExceptionsHandler._handle_request_exception(exception)

        return error_message
