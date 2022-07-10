from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import scapy.config
import sys

def main(ip):
	req = IP(ttl=1,dst=ip)/ICMP()
	res = sr1(req,verbose=0,timeout=1)
	print("1",res[IP].src,(res.time-req.time)*1000, "ms")
	i = 2
	while res[IP].src != req[IP].dst:
		req = IP(ttl=i,dst=ip)/ICMP()
		res = sr1(req,verbose=0,timeout=1)
		if res is not None:
			print(i,res[IP].src,(res.time-req.time)*1000, "ms")
		else:
			res = req
			print(i,"* * *")
		i+=1

if __name__ == "__main__":
	if (len(sys.argv) == 2):
		main(sys.argv[1])