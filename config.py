import os
from dotenv import load_dotenv

# Load settings from .env file
load_dotenv()

# Get pxGrid hostname from environment variable
pxgrid_hostname = os.getenv('PXGRID_HOSTNAME')

# Format pxgrid URL prefix
pxgrid_url = f"https://{pxgrid_hostname}:8910/pxgrid/control"

# Get pxGrid Certificate files from environment variable
pxgrid_cert = os.getenv('PXGRID_CLIENT_CERT')
pxgrid_key = os.getenv('PXGRID_CLIENT_KEY')
pxgrid_ca = os.getenv('PXGRID_CA_CERT')

# Get pxGrid Direct URL
pxgrid_direct_url = os.getenv('PXGRID_DIRECT_URL')
pxgrid_direct_user = os.getenv('PXGRID_DIRECT_USER')
pxgrid_direct_password = os.getenv('PXGRID_DIRECT_PASSWORD')

# Get PSN Hostname from environment variable
psn_hostname = os.getenv('PSN_HOSTNAME')