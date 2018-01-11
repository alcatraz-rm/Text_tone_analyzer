from pprint import pprint


with open('dictionary.txt', 'r', encoding='windows-1251') as file:
    data = file.read().split('\n')

pprint(data)
