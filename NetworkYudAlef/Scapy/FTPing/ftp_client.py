from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import scapy.config

DSIZE = 65000

# print(scapy.config.conf.ifaces)

data = b''
with open('Strawberry.jpg','rb') as f:
    data = f.read()

chunks = [data[i:i+DSIZE] for i in range(0, len(data), DSIZE)]

ind = 0
for chunk in chunks:
    while True:

        print("Sending chunk",ind)

        req = IP(dst="127.0.0.1") / ICMP(type="echo-request") / chunk

        send(req, iface="Software Loopback Interface 1",verbose=0)

        ack = sniff(count=1, lfilter=lambda x: ICMP in x, iface="Software Loopback Interface 1", timeout=5)

        if len(ack) == 0:
            continue

        if bytes(ack[0][Raw]) == b'ACK' and ind == len(chunks)-1:

            while True:
                fin = IP(dst="127.0.0.1") / ICMP(type="echo-request") / "FIN"
                send(fin, iface="Software Loopback Interface 1",verbose=0)
                finack = sniff(count=1, lfilter=lambda x: ICMP in x, iface="Software Loopback Interface 1", timeout=5)
                if len(finack) == 0:
                    continue
                if bytes(finack[0][Raw]) == b'FINACK':
                    break

            print("Finished")
            break
        elif bytes(ack[0][Raw]) == b'ACK':
            break
    ind+=1