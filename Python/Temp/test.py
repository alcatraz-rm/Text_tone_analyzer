import datetime
from pprint import pprint
import time


def _last_report_find():
    dates = list()

    for i in range(5):
        tmp = str(datetime.datetime.now()).split('.')[0]

        print(tmp)
        tmp = datetime.datetime.strptime(tmp, '%y-%m-%d %H:%M:%S')
        print(tmp)

        dates.append(tmp)
        time.sleep(2)

    dates[2], dates[3] = dates[3], dates[2]

    pprint(dates)

    pprint(sorted(dates))


_last_report_find()
