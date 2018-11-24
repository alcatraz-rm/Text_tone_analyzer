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

from Microservices import Packer

data = Packer.pack({'text': input('text: ')})
default_port = 5002

response = requests.get(f'http://localhost:{default_port}/api/spellChecker/checkText',
                        params={'content': data}).content.decode('utf-8')

checked_text = Packer.unpack(response)['response']['text']

print(checked_text)
