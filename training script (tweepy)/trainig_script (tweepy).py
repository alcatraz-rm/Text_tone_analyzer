import tweepy
from pprint import pprint
import json
import copy
import chardet
import pymorphy2
import datetime


def twitter_auth():
    consumer_key = '7jK49ES2ZDv0DL6Jsxm9wIdDx'
    consumer_secret = 'yOLMq677FX0n2MEMarOKaqYEqTXAVaAFRiqIntiRSUyu6fauwT'
    access_token = '2361221932-dsYEXSV10UFUTkKqt2oS0PpUek5o7FaGO4Od1s0'
    access_token_secret = 'mQFmIODWdurpz4oVBkdUSi6K8LascxvvTiHa5JZDwlA6a'
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    return tweepy.API(auth)


def lemmatization(string):
    morph = pymorphy2.MorphAnalyzer()

    punctuations_list = ['.', ',', '?', '!', ':', ';', '/', '&', '*', '%', '@', '#', '+', '=', '>', '<', '{', '}', '[',
                         ']', '"', "'", '`',
                         '$', '№', '^', '(', ')']

    interjections_list = [' а ', ' а как же ', ' алло ', ' алле ', ' аминь ', ' ах ', ' ах ах ах ', ' бля ', ' блин ',
                          ' боже ', ' браво ', ' бах ', ' бац ',
                          ' вау ', ' все ', ' го ', ' господи ', ' да ', ' е ', ' ё ', ' е мае ', ' ё мае ',
                          ' ей богу ', ' елки палки ', ' елы палы ',
                          ' ёлки палки ', ' ёлы палки ', ' епт ', ' ёпт ', ' епть', ' ёпть ', ' естественно ',
                          ' здравствуйте ', ' здравствуй ', ' здрасьте ',
                          ' извините ', ' кыш ', 'ко ко ко', ' м ', ' мда ', ' ну ка ', ' ну ', ' ну ну ', ' о ',
                          ' окей ', ' ой ', ' опа ', ' опаньки ',
                          ' ох ', ' поди ', ' подожди ', ' привет ', ' простите ', ' прощайте ', ' пока ', ' стоп ',
                          ' то то ', ' тик так ', ' тсс ', ' ух ',
                          ' фух ', ' фуух ', ' фууух ', ' ха ', ' хлобысь ', ' черт ', ' эй ', ' эх ']

    prepositions_list = [' а ля ', ' без ', ' без ведома ', ' безо ', ' благодаря ', ' близ ', ' близко от ', ' в ',
                         ' в виде ', ' в зависимости от ',
                         ' в интересах ', ' в качестве ', ' в лице ', ' в отличие от ', ' в отношении ', ' в пользу ',
                         ' в преддверии ', ' в продолжение ',
                         ' в результате ', ' в роли ', ' в связи с ', ' в силу ', ' в случае ', ' в соответствии с ',
                         ' в течение ', ' в целях ',
                         ' вблизи ', ' ввиду ', ' вглубь ', ' вдогон ', ' вдоль ', ' взамен ', ' включая ', ' вокруг ',
                         ' вместо ', ' вне ', ' внизу ',
                         ' внутри ', ' внутрь ', ' во ', ' во имя ', ' вовнутрь ', ' возле ', ' вопреки ', ' впереди ',
                         ' вплоть до ', ' впредь до ',
                         ' вразрез ', ' вроде ', ' вслед ', ' вследствие ', ' для ', ' до ', ' за ', ' за вычетом ',
                         ' за исключением ', ' за счет ',
                         ' из ', ' из за ', ' из под ', ' изнутри ', ' изо ', ' исключая ', ' исходя из ', ' к ',
                         ' касаемо ', ' касательно ', ' ко ',
                         ' кроме ', ' кругом ', ' лицом к лицу с ', ' на ', ' на благо ', ' на виду у ',
                         ' на глазах у ', ' на предмет ', ' наверху ',
                         ' наверху ', ' навстречу ', ' над ', ' надо ', ' назад ', ' накануне ', ' наместо ',
                         ' наперекор ', ' наперерез ', ' наперехват ',
                         ' наподобие ', ' напротив ', ' наряду с ', ' насчет ', ' начиная с ', ' насчёт ', ' не без ',
                         ' не считая ', ' невзирая на ',
                         ' недалеко от ', ' независимо от ', ' несмотря на ', ' ниже ', ' о ', ' об ', ' обо ',
                         ' около ', ' окромя ', ' от ',
                         ' от имени ', ' от лица ', ' относительно ', ' ото ', ' перед ', ' передо ', ' по ',
                         ' по линии ', ' по мере ',
                         ' по направлению к ', ' по поводу ', ' по причине ', ' по случаю ', ' по сравнению с ',
                         ' поблизости от ', ' поверх ', ' под ',
                         ' под видом ', ' под эгидой ', ' подле ', ' подо ', ' подобно ', ' позади ', ' позднее ',
                         ' помимо ', ' поперек ', ' поперёк ',
                         ' порядка ', ' посередине ', ' посерёдке ', ' посередке ', ' посередь ', ' после ',
                         ' посреди ', ' посредине ', ' посредством ',
                         ' пред ', ' предо ', ' прежде ', ' при ', ' при помощи ', ' применительно к ', ' про ',
                         ' промеж ', ' против ', ' противно ',
                         ' путем ', ' путём ', ' ради ', ' рядом с ', ' с ', ' с ведома ', ' с помощью ',
                         ' с прицелом на ', ' с точки зрения ',
                         ' с целью ', ' сверх ', ' сверху ', ' свыше ', ' сзади ', ' следом за ', ' смотря по ',
                         ' снизу ', ' со ', ' согласно ',
                         ' спустя ', ' среди ', ' сродни ', ' судя по ', ' у ', ' через ']

    particles_list = [' а вот ', ' авось ', ' ага ', ' бишь ', ' будто ', ' буквально ', ' бы ', ' ведь ', ' вероятно ',
                      ' вон ', ' вот ', ' вот вот ',
                      ' вроде ', ' вряд ли ', ' все ', ' таки ', ' всего ', ' да ', ' да уж ', ' ка ', ' давай ',
                      ' даже ', ' дескать ', ' едва ли ',
                      ' едва ли не ', ' если ', ' еще ', 'ещё ', ' же ', ' ка ', ' как ', ' ладно ', ' навряд ли ',
                      ' наоборот ', ' неа ', ' неужто ',
                      ' ну ', ' ну ну ', ' ну с ', ' откуда ', ' очевидно ', ' по видимому ', ' поди ', ' пожалуй ',
                      ' пожалуйста ', ' походу ', ' прямо ',
                      ' пусть ', ' разве ', ' ровно ', ' с ', ' словно ', ' собственно ', ' спасибо ', ' так ',
                      ' таки ', ' типа ', ' то то ', ' тоже ',
                      ' уж ', ' уже ', ' хотя ', ' хоть ', ' якобы ']

    numbers_list = [' восемнадцать ', ' восемь ', ' восемьдесят ', ' восьмеро ', ' два ', ' двадцать ', ' двенадцать ',
                    ' две ', ' двое ', ' девять ',
                    ' девяносто ', ' девятеро ', ' девятнадцать ', ' десять ', ' десятеро ', ' дофига ', ' много ',
                    ' немного ', ' немножно ',
                    ' несколько ', ' оба ', ' один ', ' одиннадцать ', ' полтора ', ' пятеро ', ' пятнадцать ',
                    ' пять ', ' пятьдесят ', ' раз ',
                    ' семь ', ' семеро ', ' семнадцать ', ' семьдесят ', ' сорок ', ' сто ', ' двести ', ' триста ',
                    ' четыреста ', ' пятьсот ',
                    ' шестьсот ', ' семьсот ', ' восемьсот ', ' девятьсот ', ' тысяча ', ' три ', ' тридцать ',
                    ' трое ', ' четыре ', ' четверо ',
                    ' четырнадцать ', ' шесть ', ' шестеро ', ' шестнадцать ', ' шестьдесят ']

    conjuctions_list = [' а ', ' и ', ' а ведь ', ' а именно ', ' а не то ', ' а то ', ' аки ', ' благодаря тому что ',
                        ' благодаря чему ', ' будто ',
                        ' в результате чего ', ' ведь ', ' впрочем ', ' вследствие чего ', ' где ', ' где то ',
                        ' дабы ', ' даже ', ' до тех пор пока ',
                        ' до тех пор пока не ', ' до того как ', ' докуда ', ' едва ', ' если ', ' ежели ', ' же ',
                        ' зато ', ' зачем ', ' и ', ' или ',
                        ' ибо ', ' из за того что ', ' из за этого ', ' иль ', ' именно ', ' иначе ', ' итак ',
                        ' кабы ', ' как ', ' как бы не ',
                        ' как то ', ' каков ', ' какой ', ' когда ', ' коли ', ' который ', ' куда ', ' либо ',
                        ' лишь ', ' лишь только ', ' настолько ',
                        ' нежели ', ' но ', ' однако ', ' однако же ', ' окуда ', ' оттого ', ' отчего ',
                        ' перед тем как ', ' по мере того как ',
                        ' пока не ', ' поскольку ', ' потому как ', ' потому что ', ' притом ', ' причем ', ' причём ',
                        ' просто ', ' пусть ', ' равно ',
                        ' разве ', ' с тем чтобы ', ' сколько ', ' следовательно ', ' словно ', ' столько ',
                        ' так как ', ' также ', ' то ', ' то есть  ',
                        ' то ли ', ' тоже ', ' только ', ' хоть ', ' хотя ', ' чем ', ' что ', ' чтоб ', ' чтобы ',
                        ' чуть ']

    pronouns_list = ['все все ', ' какой либо ', ' кое кто ', ' кое что ', ' кто ', ' кто либо ', ' многий ', ' никто ',
                     ' ничто ', ' сий ', ' такой то ', ' тот то ', ' чей либо ', ' чей нибудь ', ' чей то ', ' мы ',
                     ' вы ', ' он ', ' она ', ' оно ', ' они ', ' ты ', ' я ', ' некто ', ' нечто ', ' каждый ',
                     ' любой ', ' ваш ', ' их ', ' мой ', ' мое ', ' мое ', ' моя ', ' наш ', ' свой ', ' твой ',
                     ' чей ', ' тот ', ' этот ', ' эта', ' эти ', ' это ', ' друг друга ', ' друг с другом ',
                     ' между собой ']

    part_of_speech_dictionary = {'interjection':interjections_list, 'preposition':prepositions_list,
    'particles':particles_list, 'number':numbers_list, 'conjuction':conjuctions_list, 'pronouns':pronouns_list}

    string = string.lower()
    string = ' ' + string + ' '

    for word in punctuations_list:
        string = string.replace(word, '')

    for part_of_speech in part_of_speech_dictionary:
        for word in part_of_speech_dictionary[part_of_speech]:
            string = string.replace(word, ' ')

    string = string[2:len(string) - 1]

    string = string.split()
    for num, word in enumerate(string):
        string[num] = morph.parse(word)[0].normal_form

    string = [word + ' ' for word in string]

    return ''.join(string).strip().lower()


def parse(result):
    tmp_positive = []
    tmp_negative = []
    # tmp = {'text': text}
    tmp = dict()
    for tweet in result:
        if len(tweet.text) < 139:
            tmp_text = tweet.text
            print(tmp_text)
            tmp['text'] = lemmatization(tmp_text)
            print(tmp['text'])
            tonal = input('Tonal: ')  # 'p'/'n'/'s'

            if tonal.strip().lower() == 'p':
                tmp_positive.append(tmp)
                tmp_positive = copy.deepcopy(tmp_positive)
            elif tonal.strip().lower() == 'n':
                tmp_negative.append(tmp)
                tmp_negative = copy.deepcopy(tmp_negative)
            elif tonal.strip().lower() == 'stop':
                break

    return tmp_positive, tmp_negative


date = input('Enter the date: ').split('.')
day = int(date[0])
month = int(date[1])
year = int(date[2])

date = datetime.date(year, month, day)
api = twitter_auth()
tmp_positive = []
tmp_negative = []
search_text = '1'
search_text_prev = ''

while search_text:
    search_text = input('Query: ')

    if search_text.strip().lower() == 'stop':
        break

    while not search_text:
        search_text = input('Query: ')

    if 'prev' in search_text.strip().lower():
        search_text = search_text_prev

    result = api.search(q=search_text, lang='ru')
    tmp = parse(result)
    tmp_positive.extend(tmp[0])
    tmp_negative.extend(tmp[1])
    search_text_prev = search_text


positive = {'results': tmp_positive}
negative = {'results': tmp_negative}
with open('positive_%s.json' % date, 'w') as file:
    json.dump(positive, file, indent=4)

with open('negative_%s.json' % date, 'w') as file:
    json.dump(negative, file, indent=4)

with open('positive_%s.txt' % date, 'w', encoding='utf-8') as file:
    file.write(json.dumps(positive, indent=4))

with open('negative_%s.txt' % date, 'w', encoding='utf-8') as file:
    file.write(json.dumps(negative, indent=4))

with open('negative_%s.txt' % date, 'rb') as file:
    encoding = chardet.detect(file.read())['encoding']
    print(encoding)

with open('positive_%s.txt' % date, 'r', encoding='utf-8') as file:
    positive_read = json.loads(file.read())

with open('negative_%s.txt' % date, 'r', encoding='utf-8') as file:
    negative_read = json.loads(file.read())

pprint(positive_read)
pprint(negative_read)
