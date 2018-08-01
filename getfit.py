#! /usr/bin/env python

import json
from google.oauth2 import service_account

from datetime import datetime
from apiclient.discovery import build

# Check https://developers.google.com/fit/rest/v1/reference/users/dataSources/datasets/get
# for all available scopes
OAUTH_SCOPE = 'https://www.googleapis.com/auth/fitness.activity.read'

# DATA SOURCE
DATA_SOURCE = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"

# The ID is formatted like: "startTime-endTime" where startTime and endTime are
# 64 bit integers (epoch time with nanoseconds).
DATA_SET = "1532453580000000000-1532963273000000000"

def retrieve_data():
    SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read']
    SERVICE_ACCOUNT_FILE = '/Users/dfoley/python-client-service.json'

    credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT_FILE, scopes=SCOPES)

    fitness_service = build('fitness', 'v1', credentials=credentials)

    return fitness_service.users().dataSources(). \
              datasets(). \
              get(userId='me', dataSourceId=DATA_SOURCE, datasetId=DATA_SET). \
              execute()

def nanoseconds(nanotime):
    """
    Convert epoch time with nanoseconds to human-readable.
    """
    dt = datetime.fromtimestamp(nanotime // 1000000000)
    return dt.strftime('%Y-%m-%d %H:%M:%S')

if __name__ == "__main__":
    # Point of entry in execution mode:
    dataset = retrieve_data()
    with open('dataset.json', 'w') as outfile:
        json.dump(dataset, outfile)

    last_point = dataset["point"][-1]
    print "Start time:", nanoseconds(int(last_point.get("startTimeNanos", 0)))
    print "End time:", nanoseconds(int(last_point.get("endTimeNanos", 0)))
    print "Data type:", last_point.get("dataTypeName", None)
    print "Steps:", last_point["value"][0].get("intVal", None)
