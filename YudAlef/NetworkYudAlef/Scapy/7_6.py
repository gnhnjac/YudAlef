from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether
import scapy.config
import sys


#def main(ip,amt):
	
#	print("Sending",amt,"packets to",ip)
	
#	recvd = 0
#	for i in range(int(amt)):
#		req = IP(dst=ip)/ICMP()
#		res = sr1(req,verbose=0,timeout=0.1)
#		if res is not None:
#			recvd+=1
#	print("Received",recvd,"reply packets.")

def main(ip,amt):
	
	print("Sending",amt,"packets to",ip)
	
	req = IP(dst=ip)/ICMP()
	resp = srloop(req,count=int(amt),verbose=0,timeout=0.1)
	recvd = len(resp[0])
	
	print("Received",recvd,"reply packets.")

if __name__ == "__main__":
	if len(sys.argv) == 3:
		main(sys.argv[1],sys.argv[2])