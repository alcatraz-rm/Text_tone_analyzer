# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


import pymorphy2
from string import ascii_letters
import re
# import logging
import json
import os
from Python.Services.SpellChecker import SpellChecker


class Lemmatizer:
    def __init__(self):
        self.spell_checker = SpellChecker()
        if os.getcwd().endswith('Master'):
            self.parts_of_speech_path = os.path.join('..' 'Modules', 'Lemmatizer', 'parts_of_speech.json')
        else:
            self.parts_of_speech_path = os.path.join(os.getcwd(), 'parts_of_speech.json')

        self.parts_of_speech = self.read_parts_of_speech()
        self.morph_analyzer = pymorphy2.MorphAnalyzer()


    def contains_latin_letter(self, word):
        return all(map(lambda c: c in ascii_letters, word))

    def read_parts_of_speech(self):
        with open(self.parts_of_speech_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def lead_to_initial_form(self, text):
        words = re.findall(r'\w+', self.spell_checker.check(text.lower()))

        words = [word for word in words if not word.isalpha()
                 and not self.contains_latin_letter(word)]

        words = [self.morph_analyzer.parse(word)[0].normal_form + ' '
                  for word in words]

        text = ' ' + ''.join(words) + ' '

        for part_of_speech in self.parts_of_speech.values():
            for word in part_of_speech:
                text = text.replace(word, ' ')

        return text.strip()
