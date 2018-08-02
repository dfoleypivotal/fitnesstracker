import pycurl
from StringIO import StringIO
import os
import configparser
import cStringIO
import json
import calendar
from datetime import datetime, timedelta
import pytz


cwd = os.path.dirname(os.path.realpath(__file__))
inputfile = "{}/settings.ini".format(cwd)
settings = configparser.ConfigParser()
settings.read(inputfile)
access_token = settings.get('FIT', 'api.accesstoken')

header = ['Content-type: application/json;encoding=utf-8',
          'Authorization: Bearer {}'.format(access_token)]

buf = cStringIO.StringIO()

c = pycurl.Curl()
c.setopt(c.URL, 'https://www.googleapis.com/fitness/v1/users/me/sessions')
c.setopt(c.HTTPHEADER, header)

c.setopt(c.WRITEFUNCTION, buf.write)

c.perform()
c.close()

body = buf.getvalue()

# Body is a string in some encoding.
# In Python 2, we can print it without knowing what the encoding is.
# print(body)

result = json.loads(body)

timezone = pytz.timezone("America/Denver")

print("\nGetting Session Data...\n")
sessions = result['session']
for session in sessions:
    # print("{}".format(session))
    dt = datetime.fromtimestamp(int('{}000000'.format(session['startTimeMillis']))/1e9)
    startTimeStr = "{}".format(dt.strftime('%Y-%m-%d %H:%M:%S'))
    dt = datetime.fromtimestamp(int('{}000000'.format(session['endTimeMillis']))/1e9)
    endTimeStr = "{}".format(dt.strftime('%Y-%m-%d %H:%M:%S'))
    print("id: {}, name: {}, Start {}:, End {}:".format(session['id'], session['name'], startTimeStr, endTimeStr))
else:
    print("\nNo data found....")






