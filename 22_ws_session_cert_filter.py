# Reference: https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/Session-Directory

import requests
import websocket
import ssl
import json
from config import *
from base64 import b64encode

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

# Call back function that is called when the WebSocket connection is opened
def on_open(wsapp):
    # Send the CONNECT and SUBSCRIBE messages
    wsapp.send(f"CONNECT\naccept-version:1.2\nhost:{node_name}\n\n\x00",websocket.ABNF.OPCODE_BINARY)
    wsapp.send(f"SUBSCRIBE\ndestination:{session_topic}\nfilter:userName=='jsmith'\nid:python\n\n\x00",websocket.ABNF.OPCODE_BINARY)

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

# Initialize SSL Context with client certificate authentication
ssl_context = ssl.create_default_context()
ssl_context.load_verify_locations(cafile=pxgrid_ca)
ssl_context.load_cert_chain(certfile=pxgrid_cert, keyfile=pxgrid_key)

# Create the WebSocket connection
wsapp=websocket.WebSocketApp(ws_url,
    on_message=on_message,
    on_open=on_open,

    # Authorization header is created manually
    header={
        "Authorization": "Basic "+b64encode((f"pxgrid-client:none").encode()).decode()
    }
)

# Loop forever until ^C is pressed
wsapp.run_forever(sslopt={"context": ssl_context})