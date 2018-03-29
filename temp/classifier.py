import csv
from pprint import pprint
import pandas


def read_dataset_as_dataframe():
    dataframe_list = list()

    with open('dataset.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data = ''.join(row).split(';')
            dataframe_list.append([data[2], data[1]])  # temp, for one feature (unigrams weight)
            # dataframe_list.append([data[2], data[3], data[4], data[1]])

    dataframe = pandas.DataFrame(data=dataframe_list, columns=['unigrams_weight', 'label'])  # temp, for one feature (unigrams weight)
    # dataframe = pandas.DataFrame(data=dataframe_list, columns=['unigrams_weight', 'bigrams_weight', 'trigrams_weight',
    #                                                           'label'])

    return dataframe


def read_dataset():
    x = list()  # features
    y = list()  # labels

    with open('dataset.csv', 'r', encoding='utf-8') as file:
        reader = csv.reader(file)
        for row in reader:
            data = ''.join(row).split(';')
            y.append(data[1])  # appending label
            x.append([data[2]])  # temp, for one feature (unigrams weight)
            # x.append([data[2], data[3], data[4]])

    return x, y


x, y = read_dataset()

