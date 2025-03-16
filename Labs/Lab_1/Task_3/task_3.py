#!/usr/bin/env python3
from scapy.all import *
def print_pkt(pkt):
	pkt.show()

pkt = sniff(iface='br-5717e1d9934a' , filter='icmp', prn=print_pkt)
