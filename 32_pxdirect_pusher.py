import requests
import csv
from config import *


data = []
with open("pxdirect_pusher.csv") as file:
    reader = csv.DictReader(file)
    for row in reader:
        data.append(row)

pxggrid_direct_data ={
    "operation": "create",
    "data": data
}

r = requests.post(pxgrid_direct_url,
                    auth = (pxgrid_direct_user, pxgrid_direct_password),
                    verify=pxgrid_ca,
                    json=pxggrid_direct_data
)

# Raise an exception for HTTP errors
r.raise_for_status()

pass