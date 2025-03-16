#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include <thread>
#include <mutex>
#include <deque>
#include <functional>
#include <condition_variable>
#include <cstdlib>
#include <cstdio>
#include <Windows.h>

std::mutex file_mutex;  // Mutex để đảm bảo việc ghi vào file đồng bộ
std::ofstream result_file("result.txt");  // File kết quả

// Class ThreadPool để quản lý các luồng và công việc
class ThreadPool {
public:
    ThreadPool(size_t numThreads) {
        for (size_t i = 0; i < numThreads; ++i) {
            threads.push_back(std::thread([this] {
                while (true) {
                    std::function<void()> task;
                    {
                        std::unique_lock<std::mutex> lock(mtx);
                        cond_var.wait(lock, [this] { return stop || !tasks.empty(); });
                        if (stop && tasks.empty()) return;
                        task = std::move(tasks.front());
                        tasks.pop_front();
                    }
                    task();
                }
            }));
        }
    }

    template <typename F>
    void enqueue(F&& f) {
        {
            std::unique_lock<std::mutex> lock(mtx);
            tasks.push_back(std::function<void()>(std::forward<F>(f)));
        }
        cond_var.notify_one();
    }

    ~ThreadPool() {
        {
            std::unique_lock<std::mutex> lock(mtx);
            stop = true;
        }
        cond_var.notify_all();
        for (std::thread& t : threads) {
            t.join();
        }
    }

private:
    std::vector<std::thread> threads;
    std::deque<std::function<void()>> tasks;
    std::mutex mtx;
    std::condition_variable cond_var;
    bool stop = false;
};

// Hàm xử lý DNS lookup và lấy địa chỉ IPv4
void resolveDns(const std::string& subdomain) {
    // Thực hiện truy vấn DNS bằng std::system, yêu cầu chỉ IPv4
    std::string command = "nslookup -4 " + subdomain + ".megacorpone.com";
    FILE* fp = _popen(command.c_str(), "r");
    if (fp == nullptr) {
        std::cerr << "Error with DNS lookup for: " << subdomain << std::endl;
        return;
    }

    char buffer[128];
    std::string ip_address;

    // Đọc kết quả của lệnh nslookup
    bool found_ip = false;
    while (fgets(buffer, sizeof(buffer), fp)) {
        // Kiểm tra nếu dòng có chứa "Address" và địa chỉ không phải là IPv6
        if (strstr(buffer, "Address") != nullptr && strstr(buffer, "fe80") == nullptr) {
            // Tìm địa chỉ IPv4
            char* ip_start = strchr(buffer, ':');
            if (ip_start) {
                ip_start++; // bỏ qua dấu ':'
                ip_address = std::string(ip_start);
                ip_address.erase(ip_address.find_last_not_of(" \r\n") + 1);  // Xóa khoảng trắng thừa
                found_ip = true;
                break;  // Chỉ lấy IP đầu tiên tìm được
            }
        }
    }

    fclose(fp);

    // Nếu tìm thấy địa chỉ IPv4, ghi vào file kết quả
    if (found_ip) {
        std::unique_lock<std::mutex> lock(file_mutex);
        result_file << subdomain << ".megacorpone.com" << " - " << ip_address << std::endl;
    } else {
        std::cerr << "No IPv4 address found for: " << subdomain << std::endl;
    }
}

int main() {
    // Đọc danh sách các subdomains từ file subdomains-top1million-5000.txt
    std::ifstream input_file("subdomains-top1million-5000.txt");
    if (!input_file) {
        std::cerr << "Unable to open subdomains-top1million-5000.txt" << std::endl;
        return 1;
    }

    // Đọc từng dòng trong file vào vector namelist
    std::vector<std::string> namelist;
    std::string subdomain;
    while (std::getline(input_file, subdomain)) {
        namelist.push_back(subdomain);
    }
    input_file.close();

    // Tạo ThreadPool với 12 luồng
    ThreadPool pool(12);

    // Đẩy công việc vào thread pool
    for (const std::string& subdomain : namelist) {
        pool.enqueue([subdomain] { resolveDns(subdomain); });
    }

    return 0;
}
