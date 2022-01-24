from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import sys

PORT = 135

print("Server running")
final = {}
while True:

    # 3 way handshake
    seq_num = random.randint(0, 4294967296)
    syn = sniff(count=1, lfilter=lambda pkt: TCP in pkt and pkt[TCP].flags == 'S' and pkt[TCP].dport == PORT,iface="Npcap Loopback Adapter")[0]
    syn_ack = IP(dst=syn[IP].src) / TCP(dport=syn[TCP].sport,sport=syn[TCP].dport,seq=seq_num,ack=(syn[TCP].seq + 1),flags='SA')
    send(syn_ack,iface="Npcap Loopback Adapter",verbose=0)
    print("Completed hanshake")
    part = sniff(count=1,lfilter=lambda pkt: TCP in pkt and pkt[TCP].flags == 'S' and pkt[TCP].dport == PORT,iface="Npcap Loopback Adapter")[0]

    if b'$' == bytes(part[TCP].payload):
        break
    final[part[TCP].seq] = bytes(part[TCP].payload)
    

final = sorted(final.items(),key=lambda x: x[0])

print("Message: ",end='')

for index,string in final:
    print(string.decode(),end='')