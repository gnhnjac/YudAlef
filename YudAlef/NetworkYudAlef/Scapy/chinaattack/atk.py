from scapy.layers.inet import IP
from scapy.utils import rdpcap
from scapy import *

__author__ = "Ami Kraizel"

pcapFile = rdpcap("SynFloodSample.pcap")

pkts = {}

for pkt in pcapFile:

    if pkt[IP].src in pkts:
        pkts[pkt[IP].src].append(float(pkt.time))
    else:
        pkts[pkt[IP].src] = [float(pkt.time)]

for ip in pkts:

    pkts[ip] = sorted(pkts[ip])
    pkts[ip] = list(map(lambda x: x-pkts[ip][0],pkts[ip]))
    if len(pkts[ip]) > 5 and pkts[ip][len(pkts[ip])-1]-pkts[ip][0] < 1:
        print(ip,'is performing a DOS attack, he sent',len(pkts[ip]),'messages in',pkts[ip][len(pkts[ip])-1],'seconds')