import pycurl
from StringIO import StringIO
import os
import configparser
import cStringIO


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
print(body)
