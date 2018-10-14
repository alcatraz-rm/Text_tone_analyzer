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
    
#### Database
    1. sqlite3.Error
    2. sqlite3.DataError
    3. sqlite3.ProgrammingError
    4. sqlite3.DatabaseError
    5. sqlite3.NotSupportedError
    6. sqlite3.IntegrityError
    7. sqlite3.InterfaceError
    8. sqlite3.InternalError
    9. sqlite3.OperationalError
    
#### Speech Recognition
    1. SpeechRecognition.RequestError
    2. SpeechRecognition.UnknownValueError
    3. SpeechRecognition.WaitTimeoutError
    4. SpeechRecognition.RequestError
