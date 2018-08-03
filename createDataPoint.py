#!/usr/bin/env python

import pycurl
import os
import configparser
import calendar
from datetime import datetime, timedelta
import json
import cStringIO

def date_to_nano(ts):
    """
    Takes a datetime object and returns POSIX UTC in nanoseconds
    """
    return calendar.timegm(ts.utctimetuple()) * int(1e3)

if __name__ == '__main__':

    cwd = os.path.dirname(os.path.realpath(__file__))
    inputfile = "{}/settings.ini".format(cwd)
    settings = configparser.ConfigParser()
    settings.read(inputfile)
    access_token = settings.get('FIT', 'api.accesstoken')
    start_time_str = raw_input("Enter Start Date/Time (default=Aug 01 2018 5:00PM): ")
    if start_time_str == '':
        start_time_str = 'Aug 01 2018 5:00PM'

    min_str = raw_input("Enter Duration (default 60): ")
    if min_str == '':
        min_str = '60'

    startTime = datetime.strptime(start_time_str,'%b %d %Y %I:%M%p')

    startnano = date_to_nano(startTime)
    endnano = date_to_nano(startTime + timedelta(seconds=(int(min_str) * 60)))

    steps = raw_input("Enter Step Count: ")

    header = ['Content-type: application/json',
              'Authorization: Bearer {}'.format(access_token)]


    current_nano =  date_to_nano(datetime.now())
    session_id = 'RandallId{}'.format(current_nano)

    file = open("dataPointsData.json","w")

    post_data = {
        "dataSourceId":
            "derived:com.google.step_count.delta:MyStepDataSource",
        "maxEndTimeNs": endnano,
        "minStartTimeNs": startnano,
        "point": [
            {
                "dataTypeName": "com.google.step_count.delta",
                "endTimeNanos": endnano,
                "originDataSourceId": "",
                "startTimeNanos": startnano,
                "value": [
                    {
                        "intVal": steps
                    }
                ]
            }
        ]}

    file.write(json.dumps(post_data))

    file.close()

    buf = cStringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, 'https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.step_count.delta:MyStepDataSource/datasets/{}-{}'.format(startnano, endnano))
    c.setopt(c.HTTPHEADER, header)

    c.setopt(c.UPLOAD, 1)
    file = open('dataPointsData.json')
    c.setopt(c.READDATA, file)

    c.perform()
    print "status code: %s" % c.getinfo(pycurl.HTTP_CODE)

    c.close()

    # File must be kept open while Curl object is using it
    file.close()

    body = buf.getvalue()

    print(body)
