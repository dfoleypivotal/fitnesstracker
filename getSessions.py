import pycurl
from StringIO import StringIO
import os
import configparser
import cStringIO
import json
import calendar
from datetime import datetime, timedelta
import pytz

class FitDataset:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_dataset_points(self, datasourceId, datasetId):
        ds_header = ['Content-type: application/json;encoding=utf-8',
                     'Authorization: Bearer {}'.format(self.access_token)]

        buf = cStringIO.StringIO()

        c = pycurl.Curl()
        c.setopt(c.URL, 'https://www.googleapis.com/fitness/v1/users/me/dataSources/{}/datasets/{}'.format(datasourceId, datasetId))
        c.setopt(c.HTTPHEADER, ds_header)

        c.setopt(c.WRITEFUNCTION, buf.write)

        c.perform()
        c.close()

        body = buf.getvalue()

        # Body is a string in some encoding.
        # In Python 2, we can print it without knowing what the encoding is.
        # print(body)
        if body == 'Not Found':
            return None

        try:
            result = json.loads(body)
        except:
            return None

        point = result['point']
        return point


class FitDatasources:
    def __init__(self, access_token):
        self.access_token = access_token

    def get_datasources(self):
        ds_header = ['Content-type: application/json;encoding=utf-8',
                     'Authorization: Bearer {}'.format(self.access_token)]

        buf = cStringIO.StringIO()

        c = pycurl.Curl()
        c.setopt(c.URL, 'https://www.googleapis.com/fitness/v1/users/me/dataSources')
        c.setopt(c.HTTPHEADER, ds_header)

        c.setopt(c.WRITEFUNCTION, buf.write)

        c.perform()
        c.close()

        body = buf.getvalue()

        # Body is a string in some encoding.
        # In Python 2, we can print it without knowing what the encoding is.
        # print(body)

        result = json.loads(body)
        if 'dataSource' in result:
            return result['dataSource']
        else:
            return None

class FitSessions:

    def __init__(self, access_token):
        self.access_token = access_token

    def get_sessions(self):
        session_header = ['Content-type: application/json;encoding=utf-8',
                  'Authorization: Bearer {}'.format(self.access_token)]

        buf = cStringIO.StringIO()

        c = pycurl.Curl()
        c.setopt(c.URL, 'https://www.googleapis.com/fitness/v1/users/me/sessions')
        c.setopt(c.HTTPHEADER, session_header)

        c.setopt(c.WRITEFUNCTION, buf.write)

        c.perform()
        c.close()

        body = buf.getvalue()

        # Body is a string in some encoding.
        # In Python 2, we can print it without knowing what the encoding is.
        # print(body)

        result = json.loads(body)
        if 'session' in result:
            return result['session']
        else:
            return None



if __name__ == '__main__':

    cwd = os.path.dirname(os.path.realpath(__file__))
    inputfile = "{}/settings.ini".format(cwd)
    settings = configparser.ConfigParser()
    settings.read(inputfile)
    access_token = settings.get('FIT', 'api.accesstoken')

    fit_datasources = FitDatasources(access_token)
    datasources = fit_datasources.get_datasources()

    # print(datasources)
    if datasources is not None:
        print("\nList of DataSources:\n-------------------")

        for datasource in datasources:
            print("Datasource: {}".format(datasource['dataStreamId']))


    fit_sessions = FitSessions(access_token)
    sessions = fit_sessions.get_sessions()


    timezone = pytz.timezone("America/Denver")

    if sessions is not None:

        print("\n\nSessions\n--------")
        for session in sessions:
            # print("{}".format(session))
            dt = datetime.fromtimestamp(int('{}000000'.format(session['startTimeMillis']))/1e9)
            dt_aware = timezone.localize(dt)
            startTimeStr = "{}".format(dt.strftime('%Y-%m-%d %H:%M:%S'))
            dt = datetime.fromtimestamp(int('{}000000'.format(session['endTimeMillis']))/1e9)
            endTimeStr = "{}".format(dt.strftime('%Y-%m-%d %H:%M:%S'))
            print("Session: (id: {}, Start: {}, End: {}, (Millis {}-{})".format(session['id'], startTimeStr,
                                                                      endTimeStr, session['startTimeMillis'],
                                                                      session['endTimeMillis']))
            fit_dataset = FitDataset(access_token)
            for datasource in datasources:
                points = fit_dataset.get_dataset_points(datasource['dataStreamId'], session['startTimeMillis'] + '000000-' + session['endTimeMillis'] + '000000')
                if points is not None and len(points) > 0:
                    print("\tDataStreamID: {}".format(datasource['dataStreamId']))

                    for point in points:

                        dt = datetime.fromtimestamp(int('{}'.format(point['startTimeNanos']))/1e9)
                        dt_aware = timezone.localize(dt)
                        startTimeStr = "{}".format(dt.strftime('%Y-%m-%d %H:%M:%S'))
                        dt = datetime.fromtimestamp(int('{}'.format(point['endTimeNanos']))/1e9)
                        endTimeStr = "{}".format(dt.strftime('%Y-%m-%d %H:%M:%S'))
                        print("\t\tValue: {}, StartTime: {}, EndTime: {}".format(point['value'], startTimeStr, endTimeStr))
                        # print("\t\tValue: {}, StartTime: {}, EndTime: {}".format(point['value'], point['startTimeNanos'], point['endTimeNanos']))
                    print("")









