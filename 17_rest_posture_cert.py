# Reference: https://developer.cisco.com/docs/pxgrid/subscribing-to-posture-topic/

# As of May 6, 2025 and ISE 3.4 P1, this code does not work

import requests
import json
from config import *

# Lookup posture service
r=requests.post(f"{pxgrid_url}/ServiceLookup",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=("pxgrid-client","none"),
    json={
        "name": "com.cisco.ise.posture"
    }
)

# Raise an exception for HTTP errors
r.raise_for_status()

# Display the response
print(json.dumps(r.json(),indent=2))

# Get the service information
service_info=r.json()["services"][0]

# Get the restBaseUrl
rest_url=service_info["properties"]["restBaseUrl"]

# Get postured MACs
r=requests.post(f"{rest_url}/getPosturedMacs",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=("pxgrid-client","none"),
    json={}
)
# Raise an exception for HTTP errors
r.raise_for_status()

# Get postured MACs
r=requests.post(f"{rest_url}/getPostureDataByMacList",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=("pxgrid-client","none"),
    json={
        "macAddresses": ["32:23:39:AC:57:F6"],
        "category": "hardware",
    }
)

# Raise an exception for HTTP errors
r.raise_for_status()

# Display the response
print(json.dumps(r.json(),indent=2))