from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import scapy.config

print("Listening for packets")

payload = b''

ind = 0
while True:
    packet = []

    while len(packet) == 0:
        packet = sniff(count=1, lfilter=lambda x: ICMP in x, iface="Software Loopback Interface 1",timeout=5)

    if bytes(packet[0][Raw]) == b'FIN':
        finack = IP(dst="127.0.0.1")/ICMP(type="echo-request")/"FINACK"
        send(finack, iface="Software Loopback Interface 1", verbose=0)
        print("Done")
        break

    print("Received chunk",ind)

    payload += bytes(packet[0][Raw])

    ack = IP(dst="127.0.0.1")/ICMP(type="echo-request")/"ACK"

    send(ack,iface="Software Loopback Interface 1",verbose=0)

    print("Sent ack")

    ind+=1

with open('data.jpg','wb') as f:
    f.write(payload)