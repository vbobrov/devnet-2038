# Reference: https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/Endpoint

import requests
import json
from config import *

# Lookup endpoint service
r=requests.post(f"{pxgrid_url}/ServiceLookup",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=("pxgrid-client","none"),
    json={
        "name": "com.cisco.ise.endpoint"
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

# Get endpoints
r=requests.post(f"{rest_url}/getEndpoints",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=("pxgrid-client","none"),
    json={ 
        "order":"asc",
        "startCreateTimestamp":"2024-07-20T00:00:00.000+05:30",
        "startUpdateTimestamp":"2025-07-20T00:00:00.000+05:30",
        "startIndex":0,
        "count":100,
        "filter": "macAddress==9B:E5:27:32:6D:7A"
    }
)

# Raise an exception for HTTP errors
r.raise_for_status()

# Display the response
print(json.dumps(r.json(),indent=2))