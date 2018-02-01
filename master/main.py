# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


from modules.count_text_weight.count_text_weight import count_text_weight
from modules.lemmatization.lemmatization import lemmatization
from modules.classifier.classifier import classifier

while True:
    text = input('Enter the text: ')
    text = lemmatization(text)
    weight = count_text_weight(text)
    if weight == 0:
        print('Unknown Tonal')
        continue
    tonal = classifier(weight)

    print('Text Weight: %f' % weight)
    print('Tonal: %s' % tonal)
