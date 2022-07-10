from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import sys
source_port = random.randint(1,1000)
seq_num = random.randint(0,4294967296)
syn = TCP(sport=source_port,dport=80,seq=seq_num,flags='S')
packet = IP(dst='www.facebook.com')/syn
res = sr1(packet)
ack_packet = IP(dst='www.facebook.com')/TCP(sport=source_port,dport=80,seq=res[TCP].ack,ack=(res[TCP].seq+1),flags='A')
ack_packet.show()
send(ack_packet)