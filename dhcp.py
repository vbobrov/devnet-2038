from config import *
from scapy.all import IP, UDP, BOOTP, DHCP, send
import random

def send_dhcp(vendor_class):
    mac = ":".join(f"{random.randint(0, 255):02x}" for _ in range(6))
    hw = bytes.fromhex(mac.replace(':', ''))
    packet = (
        IP(dst=psn_hostname) /
        UDP(dport=67) /
        BOOTP(chaddr=hw, xid=0x10000000) /
        DHCP(options=[
            ("message-type", "discover"),
            ("hostname", "test-client"),
            ("param_req_list", [1, 3, 6, 15, 28, 51, 58, 59]),
            ("vendor_class_id", vendor_class),
            "end"
        ])
    )

    send(packet)
    print(f"DHCP packet sent with vendor class: {vendor_class} and MAC: {mac}")

for vendor_class in ["MSFT 5.0", "Cisco AP c2800", "Cisco IP Phone 8865"]:
    send_dhcp(vendor_class)



