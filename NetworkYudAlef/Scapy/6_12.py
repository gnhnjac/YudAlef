from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import sys

addr = input("Enter address you want to get ip for: ")

packet = sr1(IP(dst="8.8.8.8")/UDP()/DNS(qd=DNSQR(qname=addr)),verbose=0)[0]
if addr in packet[DNSQR].qname.decode():

    for i in range(packet[DNS].ancount):
        res = packet[DNSRR][i]

        # If is not cname record
        if res.type != 5:
            print(res.rdata)