# Reference: https://github.com/cisco-pxgrid/pxgrid-rest-ws/wiki/Endpoint-Asset

import requests
import websocket
import ssl
import json
from config import *
from base64 import b64encode

# Register endpoint asset service
r=requests.post(f"{pxgrid_url}/ServiceRegister",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=("pxgrid-client","none"),
    json={
        "name": "com.cisco.endpoint.asset",
        "properties": {
            "wsPubsubService": "com.cisco.ise.pubsub",
            "assetTopic":"/topic/com.cisco.endpoint.asset"
        }
    }
)

# Raise an exception for HTTP errors
r.raise_for_status()

# Display the response
print(json.dumps(r.json(),indent=2))

# Lookup pubsub service
r=requests.post(f"{pxgrid_url}/ServiceLookup",
    cert=(pxgrid_cert,pxgrid_key),
    verify=pxgrid_ca,
    auth=("pxgrid-client","none"),
    json={
        "name": "com.cisco.ise.pubsub"
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

# Initialize SSL context
ssl_context=ssl.create_default_context()
ssl_context.load_verify_locations(cafile=pxgrid_ca)
ssl_context.load_cert_chain(certfile=pxgrid_cert, keyfile=pxgrid_key)

# Create a WebSocket connection
ws=websocket.create_connection(ws_url,
    sslopt={"context": ssl_context},
    header={"Authorization": "Basic "+b64encode((f"pxgrid-client:none").encode()).decode()}
)

# Load the endpoint asset JSON file
with open("endpoint.json","r") as f:
    endpoint=json.dumps(json.loads(f.read()))

# Send the endpoint asset to ISE
ws.send(f"CONNECT\naccept-version:1.2\nhost:{node_name}\n\n\x00",websocket.ABNF.OPCODE_BINARY)
ws.send(f"SEND\ndestination:/topic/com.cisco.endpoint.asset\ncontent-length:{len(endpoint)}\n\n{endpoint}\x00".encode("utf-8"),websocket.ABNF.OPCODE_BINARY)
ws.close()