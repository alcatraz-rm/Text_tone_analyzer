import csv


with open('negative.csv', 'r', encoding='utf-8') as file:
    with open('negative-tmp.csv', 'w', encoding='utf-8') as csv_file:
        reader = csv.reader(file)
        data = dict()

        try:
            for row in reader:
                try:
                    data['text'] = ''.join(row).replace('"', '').replace('\n', ' ').replace('RT', '').split(';')[3]
                    if data['text'].isdigit():
                        continue
                    else:
                        csv_file.write(data['text'] + '\n')
                        print(data)
                except:
                    print('error')
        except:
            print('error')
