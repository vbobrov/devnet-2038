# Reference: https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/Session-Directory

import requests
import websocket
import ssl
import json
from config import *
from base64 import b64encode

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

# Lookup session service
r=requests.post(f"{pxgrid_url}/ServiceLookup",
    verify=pxgrid_ca,
    auth=(username,password),
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

session_topic=service_info["properties"]["sessionTopic"]
pubsub_service=service_info["properties"]["wsPubsubService"]

# Lookup pubsub service
r=requests.post(f"{pxgrid_url}/ServiceLookup",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=("pxgrid-client","none"),
    json={
        "name": pubsub_service
    }
)
# Raise an exception for HTTP errors
r.raise_for_status()

# Display the response
print(json.dumps(r.json(),indent=2))

# Get the service information
service_info=r.json()["services"][0]


node_name=service_info["nodeName"]
ws_url=service_info["properties"]["wsUrl"]

# Get node secret
r=requests.post(f"{pxgrid_url}/AccessSecret",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=("pxgrid-client","none"),
    json={
        "peerNodeName": node_name
    }
)
# Raise an exception for HTTP errors
r.raise_for_status()

# Get the secret
secret=r.json()["secret"]

# Call back function that is called when the WebSocket connection is opened
def on_open(wsapp):
    # Send the CONNECT and SUBSCRIBE messages
    wsapp.send(f"CONNECT\naccept-version:1.2\nhost:{node_name}\n\n\x00",websocket.ABNF.OPCODE_BINARY)
    wsapp.send(f"SUBSCRIBE\ndestination:{session_topic}\nid:python\n\n\x00",websocket.ABNF.OPCODE_BINARY)

# Callback function that processes WebSocket messages
def on_message(wsapp,message):
    # Split the message into header and JSON data
    # Remove null at the end of the message
    header,ws_message=message.decode().replace("\x00","").split("\n\n")

    # Print the header
    print(header+"\n")

    try:
        # Print the JSON data if present
        print(json.dumps(json.loads(ws_message),indent=2))
    except:
        # Print the raw message if JSON parsing fails
        print(ws_message)

# Initialize SSL Context
ssl_context=ssl.create_default_context()
ssl_context.load_verify_locations(cafile=pxgrid_ca)

# Create the WebSocket connection
wsapp=websocket.WebSocketApp(ws_url,
    on_message=on_message,
    on_open=on_open,

    # Authorization header is created manually
    header={
        "Authorization": "Basic "+b64encode((f"pxgrid-client:{secret}").encode()).decode()
    }
)

# Loop forever until ^C is pressed
wsapp.run_forever(sslopt={"context": ssl_context})