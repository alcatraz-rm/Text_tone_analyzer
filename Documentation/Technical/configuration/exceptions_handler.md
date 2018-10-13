# ExceptionsHandler

Класс, как не трудно догадаться по названию, предназначен для обработки ошибок
и исключений, возникающих во время работы программы. На данный момент реализована
обработка следующих видов ошибок и исключений.

#### System:
    1. KeyError
    2. AttributeError
    3. IndexError
    4. ZeroDivisionError
    5. ValueError
    6. AssertionError
    7. SystemError

#### Requests
    1. requests.ConnectionError
    2. requests.HTTPError
    3. requests.TooManyRedirects
    4. requests.Timeout
    5. requests.TooManyRedirects
    6. requests.RequestException
    7. requests.ConnectTimeout
    8. requests.ReadTimeout

#### Files
    1. FileExistsError
    2. FileNotFoundError
