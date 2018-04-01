# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


from modules.count_text_tonal.count_text_tonal import Document


text = input('Enter the text: ')
doc = Document(text)
doc.count_weight_by_unigrams()
doc.count_weight_by_unigrams_tf_idf()

print('weight: %f' % doc.unigrams_weight)
print('tf idf weight: %f' % doc.unigrams_weight_tf_idf)
