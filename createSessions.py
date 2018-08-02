import pycurl
from StringIO import StringIO
import os
import configparser
import calendar
from datetime import datetime
from urllib import urlencode
import json
import cStringIO
from io import BytesIO


def date_to_nano(ts):
    """
    Takes a datetime object and returns POSIX UTC in nanoseconds
    """
    return calendar.timegm(ts.utctimetuple()) * int(1e2)

if __name__ == '__main__':

    cwd = os.path.dirname(os.path.realpath(__file__))
    inputfile = "{}/settings.ini".format(cwd)
    settings = configparser.ConfigParser()
    settings.read(inputfile)
    access_token = settings.get('FIT', 'api.accesstoken')

    header = ['Content-type: application/json',
              'Authorization: Bearer {}'.format(access_token)]

    tnum =  date_to_nano(datetime.now())
    session_id = 'RandallId{}'.format(tnum)

    file = open("sessionData2.json","w")

    post_data = {
        "id": "{}".format(session_id),
        "name": "Randalls example workout {}".format(str(tnum)),
        "description": "A very intense workout by Randall",
        "startTimeMillis": 1532539980000,
        "endTimeMillis":   1532547180000,
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
