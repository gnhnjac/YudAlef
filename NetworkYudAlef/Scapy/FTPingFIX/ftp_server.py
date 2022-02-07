from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import scapy.config

print("Listening for packets")

IPP='192.168.99.49'

payload = b''

ind = 0
while True:
    packet = []

    while len(packet) == 0:
        packet = sniff(count=1, lfilter=lambda x: ICMP in x and Raw in x and b'ACK' != bytes(x[Raw])[:3],timeout=5)
    if bytes(packet[0][Raw])[:3] == b'FIN':
        finack = IP(dst=IPP)/ICMP(type="echo-request")/"FINACK"
        send(finack, verbose=0)
        print("Done")
        break

    print("Received chunk",ind)

    payload += bytes(packet[0][Raw])

    ack = IP(dst=IPP)/ICMP(type="echo-request")/"ACK"

    send(ack,verbose=0)

    print("Sent ack")

    ind+=1

with open('data.jpg','wb') as f:
    f.write(payload)