import csv
from modules.count_text_weight.count_text_weight import count_text_weight
from modules.lemmatization.lemmatization import lemmatization

# with open('neutral (base).csv', 'w') as f:
#     pass
#
#
# def dump_to_neutral(s):
#     s[0] = lemmatization(s[0])
#     # s[1] = str(count_text_weight(s[0]))
#     with open('neutral (base).csv', 'a', encoding='utf-8') as file:
#         file.write(s[0] + '\n')
#
#
# def dump_to_negative(s):
#     s[0] = lemmatization(s[0])
#     # s[1] = str(count_text_weight(s[0]))
#     with open('negative (base)_extended.csv', 'a', encoding='utf-8') as file:
#         file.write(s[0] + '\n')
#
#
# def dump_to_positive(s):
#     s[0] = lemmatization(s[0])
#     # s[1] = str(count_text_weight(s[0]))
#     with open('positive (base)_extended.csv', 'a', encoding='utf-8') as file:
#         file.write(s[0] + '\n')
#
#
# with open('text_rating_final_exported_fixed.csv', 'r') as file:
#     reader = csv.reader(file)
#     for row in reader:
#         s = ''.join(row).split(';')
#         print(s)
#         try:
#             if int(s[1]) == 0:
#                 dump_to_neutral(s)
#             elif int(s[1]) < 0:
#                 dump_to_negative(s)
#             elif int(s[1]) > 0:
#                 dump_to_positive(s)
#         except:
#             pass


with open('negative (base).csv', 'r', encoding='utf-8') as file:
    reader = csv.reader(file)
    with open('negative.csv', 'w', encoding='utf-8') as ff:
        for f in reader:
            data = ''.join(f)
            print(data)
            try:
                data = data.split(';')
                ff.write(data[0] + '\n')
            except:
                ff.write(data + '\n')
