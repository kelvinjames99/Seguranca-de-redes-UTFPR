import time
import datetime

d = datetime.datetime.now()
print(d)
d = d + datetime.timedelta(minutes=15)
dateString = d.strftime("%m/%d/%Y, %H:%M:%S")
print(dateString)
date_time_obj = datetime.datetime.strptime(dateString, "%m/%d/%Y, %H:%M:%S")
print(date_time_obj)
if datetime.datetime.now() > date_time_obj:
    print("oi")
