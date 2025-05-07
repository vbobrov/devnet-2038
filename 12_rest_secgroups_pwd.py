# Reference: https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/TrustSec-configuration
 
import requests
import json
from config import *

# Read the credentials from the file
with open(".pxgrid-creds.txt", "r") as f:
    username, password = f.read().strip().split(":")

# Lookup trustsec service
r=requests.post(f"{pxgrid_url}/ServiceLookup",
    verify=pxgrid_ca,
    auth=(username,password),
    json={
        "name": "com.cisco.ise.config.trustsec"
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

# Get the nodeName
node_name=service_info["nodeName"]

# Get Access Secret
r=requests.post(f"{pxgrid_url}/AccessSecret",
    verify=pxgrid_ca,
    auth=(username,password),
    json={
        "peerNodeName": node_name
    }
)
r.raise_for_status()
secret=r.json()["secret"]

# Get the security groups
r=requests.post(f"{rest_url}/getSecurityGroups",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=(username,secret),
    json={}
)

# Raise an exception for HTTP errors
r.raise_for_status()

# Display the response
print(json.dumps(r.json(),indent=2))