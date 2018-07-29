#!/usr/bin/env python

from datetime import datetime, timedelta
import calendar
import random

def date_to_nano(ts):
    """
    Takes a datetime object and returns POSIX UTC in nanoseconds
    """
    return calendar.timegm(ts.utctimetuple()) * int(1e9)

if __name__ == '__main__':

    file = open("stepData.txt","w")


    startTimeStr = 'Jul 24 2018 5:33PM'
    duration_seconds = 10
    records = 10


    startTime = datetime.strptime(startTimeStr,'%b %d %Y %I:%M%p')

    startnano = date_to_nano(startTime)
    endnano = date_to_nano(startTime + timedelta(seconds=(duration_seconds * records + duration_seconds)))


    #startStr = "{}".format(date_to_nano(datetime_obj) + timedelta(seconds=(records * duration_seconds + duration_seconds)))
    # print("{0}".format((datetime.strptime(startTime,'%b %d %Y %I:%M%p') + timedelta(seconds=5))))

    head = "{{\"dataSourceId\": " \
           "\n\t\"derived:com.google.step_count.delta:Example Manufacturer:ExampleTablet:1000001:MyStepDataSource\", " \
           "\n\t\"maxEndTimeNs\": {0}, \"minStartTimeNs\": {1}," \
           "\n\t\"point\": [".format(startnano, endnano)


    file.write(head)

    for i in range(0, duration_seconds * records, records):

        print(i)

        if i > 0:
            file.write("\n\t\t,\n")
        else:
            file.write("\n")

        startnano = date_to_nano(startTime + timedelta(seconds=(i)))
        endnano = date_to_nano(startTime + timedelta(seconds=(i + duration_seconds - 1)))
        # print("{} {} {} {}".format(i*duration_seconds, startnano,(i + 1), (i+1) * duration_seconds - 1))
        body = "\t\t{{\n\t\t\t\"dataTypeName\": \"com.google.step_count.delta\", " \
               "\n\t\t\t\"endTimeNanos\":   {0}," \
               "\n\t\t\t\"originDataSourceId\": \"\"," \
               "\n\t\t\t\"startTimeNanos\": {1}," \
               "\n\t\t\t\"value\": [" \
               "\n\t\t\t\t{{\"intVal\": {2}}}\n\t\t\t]\n\t\t}}".format(endnano, startnano, random.randint(1,20))
        file.write(body)
    file.write("\n\t]\n}")





