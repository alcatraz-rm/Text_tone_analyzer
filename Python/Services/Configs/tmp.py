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

import json


data = {
    'windows': {'size': (500, 300),

                'background-color': 'rgb(255, 222, 200)',

                'line-edit': {
                    'size': (375, 30),
                    'background-color': 'rgb(255, 255, 255)',
                    'coordinates': (32.5, 40),
                    'font': ('Times', 14)
                                },

                'answer_button': {
                    'size': (190, 60),
                    'coordinates': (155, 100),
                    'font': ('Times', 17),
                    'background-color': {
                        'hover': 'rgb(144, 235, 235)',
                        '!hover': 'rgb(134, 227, 227)',
                        'pressed': 'rgb(124, 218, 217)'
                                            }
                                    },

                'voice_button': {
                    'size': (30, 30),
                    'coordinates': (415, 40),
                    'font': ('Times', 17),
                    'background-color': {
                        'hover': 'rgb(177, 137, 255)',
                        '!hover': 'rgb(172, 132, 250)',
                        'pressed': 'rgb(155, 118, 245)'
                                            }
                                    },

                'delete_button': {
                    'size': (30, 30),
                    'coordinates': (452, 40),
                    'font': ('Times', 17),
                    'background-color': {
                        'hover': 'rgb(200, 200, 200)',
                        '!hover': 'rgb(180, 180, 180)',
                        'pressed': 'rgb(160, 160, 160)'
                                            }
                                    },

                'file_dialog_button': {
                    'size': (67, 30),
                    'coordinates': (415, 77),
                    'font': ('Times', 17),
                    'background-color': {
                        'hover': 'rgb(207, 236, 207)',
                        '!hover': 'rgb(181, 225, 174)',
                        'pressed': 'rgb(145, 210, 144)'
                    }
                                    },

                'answer_label': {
                    'size': (300, 100),
                    'coordinates': (180, 180),
                    'font': ('Times', 24)
                                }
                },

    'darwin': {'size': (600, 350),

               'background-color': 'rgb(255, 230, 210)',

               'line-edit': {
                   'size': (460, 40),
                   'background-color': 'rgb(255, 255, 255)',
                   'coordinates': (30, 40),
                   'font': ('Times', 24)
                                },

               'answer_button': {
                   'size': (190, 60),
                   'coordinates': (205, 100),
                   'font': ('Times', 30),
                   'background-color': {
                       'hover': 'rgb(144, 235, 235)',
                       '!hover': 'rgb(134, 227, 227)',
                       'pressed': 'rgb(124, 218, 217)'
                                        }
                                    },

               'voice_button': {
                    'size': (40, 40),
                    'coordinates': (500, 40),
                    'font': ('Times', 28),
                    'background-color': {
                        'hover': 'rgb(177, 137, 255)',
                        '!hover': 'rgb(172, 132, 250)',
                        'pressed': 'rgb(155, 118, 245)'
                                            }
                                    },

               'delete_button': {
                   'size': (40, 40),
                   'coordinates': (545, 40),
                   'font': ('Times', 28),
                   'background-color': {
                       'hover': 'rgb(200, 200, 200)',
                       '!hover': 'rgb(180, 180, 180)',
                       'pressed': 'rgb(160, 160, 160)'
                                    },

               'file_dialog_button': {
                   'size': (85, 40),
                   'coordinates': (500, 85),
                   'font': ('Times', 17),
                   'background-color': {
                       'hover': 'rgb(207, 236, 207)',
                       '!hover': 'rgb(181, 225, 174)',
                       'pressed': 'rgb(145, 210, 144)'
                   }
                                    },

               'answer_label': {
                   'size': (300, 100),
                   'coordinates': (180, 180),
                   'font': ('Times', 40)
                                }
                                    }
               }
    }

with open('demo.json', 'w', encoding='utf-8') as file:
    json.dump(data, file, indent=4)
