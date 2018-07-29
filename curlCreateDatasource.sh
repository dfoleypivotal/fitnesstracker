#!/bin/bash
# Get the refreshed access token from the https://developers.google.com/oauthplayground
#!/bin/bash
ACCESS_TOKEN="ya29.GlsGBhuqthWCXS2iVJCmpkfsqodGjUK4rH2c3dPScLWZYqSYDWud0aayEio59Iz3MuCl5_7SNARJFOVsxBl_s2w5ls0aFpuKaX0d_6nmnAfHxguj5oafCjibp8cQ"
curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer $ACCESS_TOKEN" \
  -X POST -d @stepDataSource.txt https://www.googleapis.com/fitness/v1/users/me/dataSources
