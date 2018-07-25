# Copyright © 2018. All rights reserved.
# Author: German Yakimov
# Licensed under the Apache License, Version 2.0
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
