from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import sys

while True:

    letter = sniff(count=1, lfilter=lambda x: UDP in x and IP in x and x[UDP].len == 0)[0]
    print(chr(letter[UDP].dport), end='')
