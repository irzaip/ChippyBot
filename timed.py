
import datetime
import time


dir(time)
print(datetime.datetime.now().minute)

alarm = (8,6)

def check_time(input: tuple):
    while (datetime.datetime.now().hour != input[0]) or (datetime.datetime.now().minute != input[1]):
        time.sleep(10)
        print('sleep')

check_time(alarm)
print("EXECUTED")



