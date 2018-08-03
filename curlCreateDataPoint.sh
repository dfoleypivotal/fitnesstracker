#!/bin/bash
# Get the refreshed access token from the https://developers.google.com/oauthplayground
if [[ -z "${ACCESS_TOKEN}" ]]; then
  echo "ACCESS_TOKEN has not been set or is invalid. Go to https://developers.google.com/oauthplayground to generate a new token"
  exit
fi
curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -X PATCH -d @dataPointsData.json https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.step_count.delta:MyStepDataSource/datasets/1533142800000-1533146400000
