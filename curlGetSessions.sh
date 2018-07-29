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
