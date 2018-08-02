import pycurl
from StringIO import StringIO
import os
import configparser

cwd = os.path.dirname(os.path.realpath(__file__))
inputfile = "{}/settings.ini".format(cwd)
settings = configparser.ConfigParser()
settings.read(inputfile)
access_token = settings.get('FIT', 'api.accesstoken')

header = ['Content-type: application/json;encoding=utf-8',
          'Authorization: Bearer {}'.format(access_token)]


buffer = StringIO()
c = pycurl.Curl()
c.setopt(c.URL, 'https://www.googleapis.com/fitness/v1/users/me/sessions')
c.setopt(c.HTTPHEADER, header)

#c.setopt(c.WRITEDATA, buffer)

c.perform()
c.close()

body = buffer.getvalue()

# Body is a string in some encoding.
# In Python 2, we can print it without knowing what the encoding is.
print(body)


'''
#!/bin/bash
# Get the refreshed access token "Bearer" from the https://developers.google.com/oauthplayground
if [[ -z "${ACCESS_TOKEN}" ]]; then
  echo "ACCESS_TOKEN has not been set or is invalid. Go to https://developers.google.com/oauthplayground to generate a new token"
  exit
fi
curl \
  -H "Content-Type: application/json;encoding=utf-8" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -X GET https://www.googleapis.com/fitness/v1/users/me/sessions
'''