#!/bin/bash
# Get the refreshed access token from the https://developers.google.com/oauthplayground
if [[ -z "${ACCESS_TOKEN}" ]]; then
  echo "ACCESS_TOKEN has not been set or is invalid. Go to https://developers.google.com/oauthplayground to generate a new token"
  exit
fi
curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -X GET https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.step_count.delta:com.google.android.gms:estimated_steps/datasets/1532453580000000000-1532882935000000000
