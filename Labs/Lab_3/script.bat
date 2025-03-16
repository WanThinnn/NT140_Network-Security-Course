@echo off
powershell -NoProfile -ExecutionPolicy Bypass -Command "& {
    $namelist = Get-Content 'C:\Users\WanThinnn\Documents\UIT\Nam_3\HK1\NT140-ATM\Thuc_hanh\Lab_3\subdomains-top1million-5000.txt';
    $namelist | ForEach-Object -Parallel {
        param ($domain)
        $result = Resolve-DnsName \"$domain.megacorpone.com\" -ErrorAction SilentlyContinue
        if ($result) {
            $domain
        }
    } -ArgumentList $_ -ThrottleLimit 18
}"
