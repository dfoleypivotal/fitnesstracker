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

    startTimeStr = 'Jul 24 2018 5:33PM'
    duration_seconds = 10
    records = 10

    startTime = datetime.strptime(startTimeStr,'%b %d %Y %I:%M%p')

    startnano = date_to_nano(startTime)
    print "Start Date = ", startnano

    endnano = date_to_nano(datetime.now())
    print "End Date = ", endnano

