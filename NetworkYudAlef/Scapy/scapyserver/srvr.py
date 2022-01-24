__author__ = 'Ami Kraizel'

from scapy.all import *
from scapy.layers.inet import IP, TCP
import time

PORT = 50

# 3 way handshake
seq_num = random.randint(0, 4294967296)
syn = sniff(count=1, lfilter=lambda pkt: TCP in pkt and pkt[TCP].flags == 'S' and pkt[TCP].dport == PORT,
            iface="Npcap Loopback Adapter")[0]
syn_ack = IP(dst=syn[IP].src) / TCP(dport=syn[TCP].sport, sport=syn[TCP].dport, seq=seq_num, ack=(syn[TCP].seq + 1),
                                    flags='SA')
send(syn_ack, iface="Npcap Loopback Adapter", verbose=0)
print("Completed handshake with", syn[IP].src, "from port", syn[TCP].sport)

# receive hello from client

hello = sniff(count=1, lfilter=lambda pkt: TCP in pkt and pkt[TCP].dport == PORT, iface="Npcap Loopback Adapter")[0]
print("C:", bytes(hello[TCP].payload))
reply = IP(dst=hello[IP].src) / TCP(dport=hello[TCP].sport, sport=hello[TCP].dport, seq=hello[TCP].ack,
                                ack=(hello[TCP].seq + len(bytes(hello[TCP].payload))),flags='PA') / Raw(load="Hello from server")
send(reply, iface="Npcap Loopback Adapter",verbose=0)
print("Sent hello back")