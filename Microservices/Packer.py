import json


def pack(data):
    return ','.join([str(ord(char)) for char in list(json.dumps(data, ensure_ascii=True))])


def unpack(data):
    return json.loads(''.join([str(chr(int(code))) for code in data.split(',')]), encoding='utf-8')
