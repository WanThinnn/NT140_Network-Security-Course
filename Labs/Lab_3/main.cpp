#include <iostream>
#include <fstream>
#include <thread>
#include <vector>
#include <string>
#include <cstdlib>  // For system()
#include <cstring>  // For strstr
#include <sstream>  // For stringstream

// Function to resolve DNS and get the IPv4 address
void resolveDns(const std::string& domain, std::ofstream& outFile) {
    std::string command = "nslookup " + domain + ".megacorpone.com";
    FILE* fp = _popen(command.c_str(), "r"); // Open the command output

    if (fp == nullptr) {
        std::cerr << "Error executing nslookup" << std::endl;
        return;
    }

    char buffer[128];
    bool found = false;
    std::string ipv4;

    // Read the output of the nslookup command
    while (fgets(buffer, sizeof(buffer), fp)) {
        if (strstr(buffer, "Name:") != nullptr) {
            // If "Name:" found, the domain is valid
            found = true;
        }

        // Check for IPv4 address
        if (strstr(buffer, "Address:") != nullptr) {
            std::string line(buffer);
            // Extract the IP address after "Address:"
            std::stringstream ss(line);
            std::string temp;
            ss >> temp >> temp;  // Skip the "Address:"
            ipv4 = temp;  // Get the IPv4 address
        }
    }

    if (found && !ipv4.empty()) {
        outFile << domain << ".megacorpone.com " << ipv4 << std::endl;
    }

    _pclose(fp); // Close the command output
}

int main() {
    std::ifstream infile("subdomains-top1million-5000.txt");
    std::string line;
    std::ofstream outFile("result.txt");

    if (!outFile) {
        std::cerr << "Error opening result.txt for writing" << std::endl;
        return 1;
    }

    std::vector<std::thread> threads;  // Vector to hold the threads
    const int maxThreads = 12;  // Limit to 12 threads

    // Read the file line by line and start a new thread for each domain
    while (std::getline(infile, line)) {
        // Start a new thread for each domain
        threads.push_back(std::thread(resolveDns, line, std::ref(outFile)));

        // If we have reached the maximum number of threads, wait for them to finish
        if (threads.size() >= maxThreads) {
            for (auto& t : threads) {
                t.join();  // Wait for each thread to complete
            }
            threads.clear();  // Clear the thread vector
        }
    }

    // Wait for any remaining threads to complete
    for (auto& t : threads) {
        t.join();
    }

    std::cout << "DNS resolution complete. Valid hostnames and IPs saved to result.txt." << std::endl;
    return 0;
}
