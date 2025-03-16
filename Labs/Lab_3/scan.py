import multiprocessing
import subprocess
import platform
import ipaddress

def ping_host(ip):
    """Kiểm tra xem một host có active hay không."""
    param = "-n" if platform.system().lower() == "windows" else "-c"
    command = ["ping", param, "1", "-w", "1000", str(ip)]  # Timeout 1 giây

    try:
        result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return str(ip) if result.returncode == 0 else None  # Trả về IP nếu host active
    except Exception as e:
        return None

def ping_sweep(network_cidr):
    """Quét mạng bằng đa luồng và chỉ in các host active."""
    try:
        network = ipaddress.ip_network(network_cidr, strict=False)
        print(f"Scanning active hosts in network: {network_cidr} (Total hosts: {network.num_addresses - 2})")
        
        # Sử dụng multiprocessing để tối ưu quét mạng
        with multiprocessing.Pool(processes=multiprocessing.cpu_count()) as pool:
            active_hosts = pool.map(ping_host, network.hosts())
        
        # Loại bỏ kết quả None (host inactive) và in kết quả
        active_hosts = [host for host in active_hosts if host]
        if active_hosts:
            print("Active hosts:")
            for host in active_hosts:
                print(host)
        else:
            print("No active hosts found in the network.")
    
    except ValueError as e:
        print(f"Invalid network CIDR: {e}")

if __name__ == "__main__":
    # Định nghĩa lớp mạng cần quét
    network_cidr = "10.0.2.0/16"  # Thay đổi dải mạng tại đây
    ping_sweep(network_cidr)
