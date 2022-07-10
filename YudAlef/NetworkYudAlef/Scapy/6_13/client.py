from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import sys

for letter in input("Enter a message please: "):

    send(IP(dst="192.168.1.187")/UDP(dport=ord(letter),len=0),return_packets=True)
    time.sleep(1)