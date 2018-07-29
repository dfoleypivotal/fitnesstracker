#!/bin/bash
# Get the refreshed access token "Bearer" from the https://developers.google.com/oauthplayground
ACCESS_TOKEN="ya29.GlsHBhOcnlzGLAD3mK6rOatijcNCNrdb0lIW0b0t6FOYWPWgNTUkRPG-r-KpLg1e-VYXNveLoPA_yAAiEkrMX9NTaX31_uNvTPdUzNNw7JXo6B_e-AaBPRuklrZ9"
curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  https://www.googleapis.com/fitness/v1/users/me/dataSources
