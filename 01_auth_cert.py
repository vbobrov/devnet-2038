# Reference: https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/pxGrid-Consumer

import requests
import json
from config import *
from time import sleep

# Repeat Activation process until client is approved
while True:
    # Send Account Activate request
    r=requests.post(f"{pxgrid_url}/AccountActivate",
        cert=(pxgrid_cert,pxgrid_key),
        verify=pxgrid_ca,
        auth=("pxgrid-client","none"),
        json={}
    )

    # Raise an exception for HTTP errors
    r.raise_for_status()
    json_response=r.json()

    # Display the response
    print(json.dumps(json_response,indent=2))

    # Check account status
    if json_response["accountState"]=="ENABLED":
        # Exit the loop if account is approved
        print("Account Approved")
        break

    # Wait for 60 seconds before retrying
    sleep(60)
