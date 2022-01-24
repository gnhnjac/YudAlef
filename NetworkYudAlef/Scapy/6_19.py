from scapy.all import *
from scapy.layers.inet import IP, TCP
import asyncio

async def check_port(p, dst_ip):

    if round(((p-20)/1004)*100) % 5 == 0:
        print(f"{round(((p-20)/1004)*100)}%")

    packet = IP(dst=dst_ip) / TCP(dport=p, seq=123, flags='S')
    res = sr1(packet, verbose=0)

    if res == None:
        return

    if 'R' not in res[TCP].flags:
        print(f"Port {p} is open")


async def main():
    ip = input("Enter ip address")

    for port in range(20,1024):
        await check_port(port, ip)

asyncio.run(main())