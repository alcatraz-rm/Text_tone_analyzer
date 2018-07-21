# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com

from string import ascii_letters
import re
import json
import os
import sys
import pymorphy2
sys.path.append(os.path.join('..', '..'))

from Python.Services.SpellChecker import SpellChecker
from Python.Services.Logger import Logger


class Lemmatizer:
    def __init__(self):
        self.spell_checker = SpellChecker()
        self.logger = Logger()

        if not self.logger.configured:
            self.logger.configure()

        self.parts_of_speech = self.read_parts_of_speech()
        self.morph_analyzer = pymorphy2.MorphAnalyzer()

        self.logger.info('Lemmatizer was successfully initialized.', 'Lemmatizer.__init__()')

    @staticmethod
    def contains_latin_letter(word):
        return all(map(lambda c: c in ascii_letters, word))

    @staticmethod
    def read_parts_of_speech():
        if os.getcwd().endswith('Master') or os.getcwd().endswith('Tests'):
            parts_of_speech_path = os.path.join('..', 'Services', 'Lemmatizer', 'parts_of_speech.json')
        else:
            parts_of_speech_path = 'parts_of_speech.json'

        with open(parts_of_speech_path, 'r', encoding='utf-8') as file:
            return json.load(file)

    def lead_to_initial_form(self, text):
        self.logger.info('Start text: %s' % text, 'Lemmatizer.lead_to_initial_form()')

        words = re.findall(r'\w+', self.spell_checker.check(text.lower()))

        words = [word for word in words if word.isalpha()
                 and not self.contains_latin_letter(word)]

        words = [self.morph_analyzer.parse(word)[0].normal_form + ' ' for word in words]

        text = ' ' + ''.join(words) + ' '

        for part_of_speech in self.parts_of_speech.values():
            for word in part_of_speech:
                text = text.replace(word, ' ')

        text = text.strip()
        self.logger.info('Lemmatized text: %s' % text, 'Lemmatizer.lead_to_initial_form()')

        return text
