#!/usr/bin/env python

import pycurl
import os
import configparser
import json
import cStringIO

if __name__ == '__main__':

    cwd = os.path.dirname(os.path.realpath(__file__))
    inputfile = "{}/settings.ini".format(cwd)
    settings = configparser.ConfigParser()
    settings.read(inputfile)
    access_token = settings.get('FIT', 'api.accesstoken')

    header = ['Content-type: application/json',
              'Authorization: Bearer {}'.format(access_token)]

    buf = cStringIO.StringIO()

    c = pycurl.Curl()
    c.setopt(c.URL, 'https://www.googleapis.com/fitness/v1/users/me/dataSources')
    c.setopt(c.HTTPHEADER, header)

    c.setopt(c.UPLOAD, 1)
    file = open('stepDataSource.json')
    c.setopt(c.READDATA, file)

    c.perform()
    print "status code: %s" % c.getinfo(pycurl.HTTP_CODE)

    c.close()

    # File must be kept open while Curl object is using it
    file.close()

    body = buf.getvalue()

    print(body)
