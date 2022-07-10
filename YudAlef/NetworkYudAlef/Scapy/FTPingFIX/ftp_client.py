from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import scapy.config

DSIZE = 1472

IPP='192.168.0.113'

# print(scapy.config.conf.ifaces)

data = b''
with open('Strawberry.jpg','rb') as f:
    data = f.read()

chunks = [data[i:i+DSIZE] for i in range(0, len(data), DSIZE)]

ind = 0
for chunk in chunks:

    while True:

        print("Sending chunk",ind,"out of",len(chunks))

        req = IP(dst=IPP) / ICMP(type="echo-request") / chunk

        send(req, verbose=0)

        ack = sniff(count=1, lfilter=lambda x: ICMP in x and bytes(x[Raw]) == b'ACK', timeout=5)
        
        if len(ack) == 0:
            continue
        break
        
    ind+=1
    
    if ind == len(chunks):
        while True:
            fin = IP(dst=IPP) / ICMP(type="echo-request") / "FIN"
            send(fin, verbose=0)
            finack = sniff(count=1, lfilter=lambda x: ICMP in x and bytes(x[Raw])==b'FINACK', timeout=5)
            if len(finack) == 0:
                continue

            print("Finished")
            break