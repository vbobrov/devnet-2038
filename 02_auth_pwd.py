# Reference: https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/pxGrid-Consumer

import requests
import json
from config import *
from time import sleep
import os

# Check if the credentials file exists
if not os.path.exists(".pxgrid-creds.txt"):

    # Create new pxGrid username
    r = requests.post(f"{pxgrid_url}/AccountCreate",
        verify=pxgrid_ca,
        json={
            "nodeName": "pxgrid-client-pwd",
        }
    )

    # Raise an exception for HTTP errors
    r.raise_for_status()
    password = r.json()["password"]

    # Save the credentials to a file
    with open(".pxgrid-creds.txt", "w") as f:
        f.write(f"pxgrid-client-pwd:{password}")

# Read the credentials from the file
with open(".pxgrid-creds.txt", "r") as f:
    username, password = f.read().strip().split(":")


# Repeat Activation process until client is approved
while True:
    # Send Account Activate request
    r=requests.post(f"{pxgrid_url}/AccountActivate",
        verify=pxgrid_ca,
        auth=(username,password),
        json={}
    )
    r.raise_for_status()
    json_response=r.json()
    print(json.dumps(json_response,indent=2))
    if json_response["accountState"]=="ENABLED":
        print(f"Account Approved.")
        break

    # Wait for 60 seconds before retrying
    sleep(1)
