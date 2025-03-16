from scapy.all import rdpcap, IP, TCP
from urllib.parse import urlparse
import re

# Hàm để kiểm tra xem URL có phải là mã độc hay không
def is_malicious(url):
    # Các biểu thức chính quy hoặc từ khóa có thể xác định mã độc
    patterns = [
        r"(cmd=ftp)",  # Tìm lệnh FTP
        r"(telnetd)",  # Tìm telnetd
        r"(\/cgi-bin\/)",  # Tìm các yêu cầu đến cgi-bin
        r"(\/bin\/sh)",  # Tìm các yêu cầu đến shell
        r"(perl)",  # Tìm lệnh perl
        r"(echo)",  # Tìm lệnh echo trong các payload
    ]
    
    for pattern in patterns:
        if re.search(pattern, url):
            return True
    return False

# Hàm để phân tích gói và tìm yêu cầu HTTP
def find_malicious_requests(pcap_file):
    packets = rdpcap(pcap_file)
    
    # Mở file log.txt để ghi
    with open('log.txt', 'w', encoding='utf-8') as log_file:
        for packet in packets:
            # Kiểm tra xem gói có phải là TCP và có payload không
            if packet.haslayer(TCP) and packet.haslayer(IP):
                payload = str(packet[TCP].payload)

                # Tìm các yêu cầu HTTP
                if b"GET" in bytes(payload, 'utf-8') or b"POST" in bytes(payload, 'utf-8'):
                    # Giải mã payload thành chuỗi
                    try:
                        decoded_payload = payload.encode('utf-8').decode('utf-8', 'ignore')
                        if "HTTP" in decoded_payload:
                            # Tách URL
                            url = decoded_payload.split(" ")[1]
                            parsed_url = urlparse(url)
                            full_url = f"{parsed_url.scheme}://{parsed_url.netloc}{parsed_url.path}"

                            # Kiểm tra URL có phải là mã độc không
                            if is_malicious(full_url):
                                print(f"Malicious request found: {full_url}")
                                log_file.write(f"Malicious request found: {full_url}\n")  # Ghi vào file log
                    except Exception as e:
                        print(f"Error decoding payload: {e}")

# Đường dẫn đến file pcap
pcap_file = 'attack.pcap'
find_malicious_requests(pcap_file)
