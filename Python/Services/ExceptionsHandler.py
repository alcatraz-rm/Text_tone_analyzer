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

import requests
from Python.Services.Logger import Logger


class ExceptionsHandler:
    def __init__(self):
        self.__logger = Logger()

        if not self.__logger.configured:
            self.__logger.configure()

        self._request_exceptions = [type(item) for item in [requests.ConnectionError(), requests.HTTPError(),
                                    requests.TooManyRedirects(), requests.Timeout(), requests.TooManyRedirects(),
                                    requests.RequestException(), requests.ConnectTimeout(), requests.ReadTimeout()]]

        self.__logger.info('ExceptionsHandler was successfully initialized.', 'ExceptionsHandler.__init__()')

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

        if type(exception) in self._request_exceptions:
            error_message = ExceptionsHandler._handle_request_exception(exception)

        return error_message
