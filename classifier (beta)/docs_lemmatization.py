import lemmatization


with open('negative (beta).txt', 'r') as file:
    negative = file.read().split('\n')

negative = [lemmatization.lemmatization(doc) for doc in negative]

with open('negative (beta).txt', 'w') as file:
    for doc in negative:
        file.write(doc + '\n')

with open('positive (beta).txt', 'r') as file:
    positive = file.read().split('\n')

positive = [lemmatization.lemmatization(doc) for doc in positive]

with open('positive (beta).txt', 'w') as file:
    for doc in positive:
        file.write(doc + '\n')
