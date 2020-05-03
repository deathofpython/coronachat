import datetime


def make_date():
    if len(str(datetime.datetime.now().hour)) == 2:
        h = str(datetime.datetime.now().hour)
    else:
        h = '0' + str(datetime.datetime.now().hour)
    if len(str(datetime.datetime.now().minute)) == 2:
        m = str(datetime.datetime.now().minute)
    else:
        m = '0' + str(datetime.datetime.now().minute)
    return str(datetime.datetime.now().date()) + " " + h + ':' + m