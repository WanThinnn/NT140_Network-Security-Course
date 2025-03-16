import pyshark

def extract_summary_with_echo(pcap_file, output_file):
    # Mở file pcap
    cap = pyshark.FileCapture(pcap_file, display_filter='http')
    
    # Mở file với mã hóa UTF-8 để ghi
    with open(output_file, 'w', encoding='utf-8') as f:
        # Duyệt qua các gói tin trong file pcap
        for packet in cap:
            try:
                # Kiểm tra nếu chuỗi 'echo' có trong nội dung của gói HTTP
                if "echo" in str(packet['http']):
                    # Trích xuất thông tin cần thiết
                    packet_no = packet.number
                    time = packet.sniff_time
                    src_ip = packet.ip.src
                    dst_ip = packet.ip.dst
                    protocol = 'HTTP'
                    info = packet['http'].request_full_uri
                    
                    # Ghi thông tin theo định dạng yêu cầu
                    f.write(f"{packet_no}\t{time}\t{src_ip}\t{dst_ip}\t{protocol}\t{info}\n")
            except AttributeError:
                # Bỏ qua những gói tin không có lớp HTTP hoặc không hợp lệ
                pass

    print(f"Extraction completed. Summary saved to {output_file}")

if __name__ == "__main__":
    pcap_file = 'attack.pcap'  # File pcap cần xử lý
    output_file = 'filtered_summary.txt'  # File xuất kết quả

    extract_summary_with_echo(pcap_file, output_file)
