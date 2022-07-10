import sys
from scapy.all import *
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, TCP, UDP, ICMP
from scapy.layers.l2 import Ether

conf.L3socket=L3RawSocket

def dns_filter(packet):

    return DNS in packet and packet[UDP].dport == 53 and (packet[DNSQR].qtype == 1 or packet[DNSQR].qtype == 12)

while True:

    packet = sniff(count=1, lfilter=dns_filter)[0]
    packet.show()
    with open('database.txt', 'r') as f:

        for line in f.readlines():

            values = line.split(',')

            type = 1 if values[0].replace('type:','') == 'A' else 12
            do_ttl = int(values[1].replace('ttl:', ''))
            name = values[2].replace('qname:','')
            data = values[3].replace('data:','')

            if packet[DNSQR].qtype != type:
                continue

            if name not in packet[DNSQR].qname.decode():
                continue

            to_send = Ether(dst=packet[Ether].src) / IP() / UDP(dport=packet[UDP].sport) / DNS(id=packet[DNS].id) / DNSRR(ttl=do_ttl,rrname=name,rdata=data)
            to_send.show()
            send(to_send)