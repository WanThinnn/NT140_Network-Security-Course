from scapy.all import rdpcap, Raw, IP, ICMP, UDP
import binascii

# Define the protocol you want to filter
protocol = 'ICMP'  # Change to 'UDP' if needed

try:
    packets = rdpcap('exfil-1.pcap')
except FileNotFoundError:
    print("File not found.")
    packets = []

payloads = []

if len(packets) > 0:
    for packet in packets:
        if IP in packet:
            if protocol == 'ICMP' and ICMP in packet:
                if packet.haslayer(Raw):  # Check if the packet has a payload
                    hex_payload = binascii.hexlify(packet[Raw].load)  # Convert payload to hex
                    ascii_payload = binascii.unhexlify(hex_payload).decode('ascii', errors='ignore')  # Convert hex to ASCII
                    payloads.append(ascii_payload)

full_data = ''.join(payloads)  # Join all payloads together

# Save the result to a text file
with open('payloads.txt', 'w') as file:
    file.write(full_data)