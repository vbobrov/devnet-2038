# Reference: https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/Session-Directory

import requests
import json
from config import *

# Lookup session service
r=requests.post(f"{pxgrid_url}/ServiceLookup",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=("pxgrid-client","none"),
    json={
        "name": "com.cisco.ise.session"
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

# Get sessions
r=requests.post(f"{rest_url}/getSessions",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=("pxgrid-client","none"),
    json={}
)

# Raise an exception for HTTP errors
r.raise_for_status()

# Display the response
print(json.dumps(r.json(),indent=2))