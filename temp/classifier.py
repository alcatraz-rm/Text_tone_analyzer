# Copyright © 2017-2018. All rights reserved.
# Authors: German Yakimov, Aleksey Sheboltasov
# License: https://github.com/GermanYakimov/Text_tone_analyzer/blob/master/LICENSE
# Contacts: german@yakimov.su, alekseysheboltasov@gmail.com


from pprint import pprint
import pandas
from sklearn.linear_model import LogisticRegression
from modules.count_text_tonal.count_text_tonal import Document


# def read_dataset_as_dataframe():
#     dataframe_list = list()
#
#     with open('dataset.csv', 'r', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             data = ''.join(row).split(';')
#             dataframe_list.append([data[2], data[1]])  # temp, for one feature (unigrams weight)
#             # dataframe_list.append([data[2], data[3], data[4], data[1]])
#
#     dataframe = pandas.DataFrame(data=dataframe_list, columns=['unigrams_weight', 'label'])  # temp, for one feature (unigrams weight)
#     # dataframe = pandas.DataFrame(data=dataframe_list, columns=['unigrams_weight', 'bigrams_weight', 'trigrams_weight',
#     #                                                           'label'])
#
#     return dataframe
#
#
# def read_dataset():
#     x = list()  # features
#     y = list()  # labels
#
#     with open('dataset.csv', 'r', encoding='utf-8') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             data = ''.join(row).split(';')
#             y.append(data[1])  # appending label
#             x.append([data[2]])  # temp, for one feature (unigrams weight)
#             # x.append([data[2], data[3], data[4]])
#
#     return x, y
#
#
# x, y = read_dataset()


def read_data():
    data = pandas.read_csv('dataset.csv', sep=';', encoding='utf-8')
    x = data.loc()[:, ['unigrams_weight']]
    y = data['tonal']

    return x, y


def classification(text):
    doc = Document(text)
    doc.count_weight_by_unigrams()

    x, y = read_data()
    classifier = LogisticRegression()
    classifier.fit(x, y)
    prediction = classifier.predict(doc.unigrams_weight)

    return prediction, doc.unigrams_weight


print(classification(input('text: ')))
