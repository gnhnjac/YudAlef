__author__ = 'Ami Kraizel'

from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import sys
DST_IP = '192.168.0.109'

IFACE = "eth0"

source_port = random.randint(49152, 65536)
dst_port = 1802
seq_num = random.randint(0, 4294967296)
syn = TCP(sport=source_port, dport=dst_port, seq=seq_num, flags='S')
packet = IP(dst=DST_IP) / syn
res = sr1(packet,verbose=0,iface=IFACE)
ack_packet = IP(dst=DST_IP) / TCP(sport=source_port, dport=dst_port, seq=res[TCP].ack, ack=(res[TCP].seq + 1), flags='A')
send(ack_packet,verbose=0,iface=IFACE)
print("Completed handshake")

# send hello from client

hello = IP(dst=DST_IP) / TCP(dport=dst_port, sport=source_port, seq=ack_packet[TCP].seq,
                                ack=(ack_packet[TCP].ack),flags='PA') / Raw(load="Hello from client")
send(hello,verbose=0,iface=IFACE)
print("Sent hello")

# receive hello from server

