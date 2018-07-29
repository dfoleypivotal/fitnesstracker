#!/bin/bash
# Get the refreshed access token from the https://developers.google.com/oauthplayground
curl \
  -H "Content-Type: application/json;encoding=utf-8" \
  -H "Authorization: Bearer ya29.GlsHBkne2Wo-uqiXJtKCnlzrZNsQ_Um1pbYyZLK7XCXr0Tb6_wy3VbmO4uQLylKV6zTG9KMmM2L3nV1ScUEf1nwjk8TYCVGY8s8Isv2oOA-uRzoOn9OvITDNFc85" \
  -X GET https://www.googleapis.com/fitness/v1/users/me/sessions



