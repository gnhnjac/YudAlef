import math
import time
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import scapy.config
import sys

DST_IP = '127.0.0.1'

msg = input("Enter a message please: ")
parts = int(input("How many parts do you want to split the message to?"))
part_len = math.ceil(len(msg)/parts)

msglst = []

for i in range(parts):

    seg = msg[i*part_len:(i*part_len+part_len if i*part_len+part_len < len(msg) else len(msg))]

    if seg != '':
        msglst.append([seg,i*part_len])

random.shuffle(msglst)

msglst.append(["$",len(msg)])

for part,ind in msglst:

    # 3 way handshake
    source_port = random.randint(49152, 65536)
    dst_port = 135#random.randint(0,65536)
    seq_num = random.randint(0, 4294967296)
    syn = TCP(sport=source_port, dport=dst_port, seq=seq_num, flags='S')
    packet = IP(dst=DST_IP) / syn
    res = sr1(packet,iface="Npcap Loopback Adapter",verbose=0)
    ack_packet = IP(dst=DST_IP) / TCP(sport=source_port, dport=dst_port, seq=res[TCP].ack, ack=(res[TCP].seq + 1), flags='A')
    send(ack_packet,iface="Npcap Loopback Adapter",verbose=0)
    print("Completed handshake")
    # send message part
    print(part,ind)
    scrambled = IP(dst=DST_IP) / TCP(sport=source_port, dport=dst_port, seq=ind) / part
    send(scrambled,iface="Npcap Loopback Adapter",verbose=0)
    time.sleep(1.5)

print("Sent message successfully!")