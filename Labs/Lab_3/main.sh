#! /bin/bash

# Định nghĩa danh sách các domain
domains=("hcmus.edu.vn" "hcmussh.edu.vn" "uit.edu.vn" "hcmut.edu.vn" "hcmiu.edu.vn" "uel.edu.vn" "hcmier.edu.vn" "vnuhcm.edu.vn")

# Tạo file kết quả hoặc mở file để ghi kết quả
output_file="zone_transfer_results.txt"
> $output_file  # Làm trống file nếu file đã tồn tại

# Lặp qua từng domain
for domain in ${domains[@]}; do
    echo "Performing zone transfer for domain: $domain" | tee -a $output_file
    
    # Lấy danh sách các nameserver cho domain
    for nameServer in $(host -t ns $domain 2> /dev/null | cut -d " " -f 4); do
        echo "Using nameserver: $nameServer" | tee -a $output_file
        
        # Thực hiện zone transfer và lưu kết quả vào file
        echo "Performing zone transfer..." | tee -a $output_file
        host -l $domain $nameServer 2>/dev/null | tee -a $output_file
        
        echo "---------------------------### End of zone transfer for $domain ###---------------------------" | tee -a $output_file
        echo | tee -a $output_file
    done
    
    echo "---------------------------### End of processing for $domain ###---------------------------" | tee -a $output_file
    echo | tee -a $output_file
done
