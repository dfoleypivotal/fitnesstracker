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
    workout_name = raw_input("Enter session name: ")
    workout_description = raw_input("Enter session Description: ")
    start_time_str = raw_input("Enter Session Start Date/Time (default=Jul 24 2018 5:33PM): ")
    if start_time_str == '':
        start_time_str = 'Jul 24 2018 5:33PM'

    min_str = raw_input("Enter Session Minutes (default 60): ")
    if min_str == '':
        min_str = '60'

    startTime = datetime.strptime(start_time_str,'%b %d %Y %I:%M%p')

    startnano = date_to_nano(startTime)
    endnano = date_to_nano(startTime + timedelta(seconds=(int(min_str) * 60)))

    header = ['Content-type: application/json',
              'Authorization: Bearer {}'.format(access_token)]


    current_nano =  date_to_nano(datetime.now())
    session_id = 'RandallId{}'.format(current_nano)


    file = open("sessionData2.json","w")

    post_data = {
        "id": "{}".format(session_id),
        "name": "{}".format(workout_name),
        "description": "{}".format(workout_description),
        "startTimeMillis": startnano,
        "endTimeMillis":   endnano,
        "application": {
            "packageName": "com.google.android.apps.fitness",
            "version": "web"
        },
        "activityType": 108}

    file.write(json.dumps(post_data))

    file.close()

    buf = cStringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, 'https://www.googleapis.com/fitness/v1/users/me/sessions/{}'.format(session_id))
    c.setopt(c.HTTPHEADER, header)

    c.setopt(c.UPLOAD, 1)
    file = open('sessionData2.json')
    c.setopt(c.READDATA, file)

    c.perform()
    print "status code: %s" % c.getinfo(pycurl.HTTP_CODE)

    c.close()

    # File must be kept open while Curl object is using it
    file.close()

    body = buf.getvalue()

    print(body)
