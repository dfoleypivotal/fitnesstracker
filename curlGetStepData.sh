#!/bin/bash
# Get the refreshed access token from the https://developers.google.com/oauthplayground
curl \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ya29.GlsGBsK0LfZSDCAlzu52wCvL1ecr752wgoAChsBG4Tae4I9xGdbR1s8C3odznSF_xpRwOANG0NMwf_1b-UBYTK3vibtGsxWedfAUOgtAUE3zXbaXTpuOLkxKKKbB" \
  -X GET https://www.googleapis.com/fitness/v1/users/me/dataSources/derived:com.google.step_count.delta:Example%20Manufacturer:ExampleTablet:1000001:MyStepDataSource
