import time

from scapy import *
from scapy.layers.inet import IP, ICMP
from scapy.sendrecv import send, sniff, sr1
import threading,sys

ip = "192.168.0.113"

for i in range(1200,1600):
    pack = IP(dst=ip) / ICMP() / ("A" * i)
    res = sr1(pack, timeout=5, verbose=0)
    if res is None:
        print("MAX:", i - 1)
        break
    elif len(res) == 0:
        print("MAX:", i - 1)
        break

    print(i)
