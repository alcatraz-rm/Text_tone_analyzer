from modules.count_text_tonal.count_text_tonal import Document


text = input('Enter the text: ')
doc = Document(text)
doc.count_tonal()
print(doc.unigrams_weight)
print(doc.trigrams_weight)
