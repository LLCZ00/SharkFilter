# SharkFilter
### _Wireshark Filter Generator_
Sharkfilter.py is a Python script for quickly creating Wireshark traffic filters. It was created because 99% of network traffic is just noise, and I was tired of specifying what addresses I wanted to monitor by hand.
## Usage
```
usage: sharkfilter.py [-h] [-v] [-e] ips [ips ...]

positional arguments:
  ips            IP addresses to create filter with

optional arguments:
  -h, --help     show this help message and exit
  -v, --version  Show version number and exit
  -e, --exclude  Filter will EXCLUDE given IPs (Includes all by default)

Examples:
        sharkfilter.py 192.168.1.27 192.168.1.35 192.168.1.41
        sharkfilter.py --exclude 10.10.10.10 35.160.181.201
```
**Example Output**
```
$ ./sharkfilter.py 192.168.1.27 192.168.1.35 192.168.1.41
(ip.addr == 192.168.1.27 && (ip.addr == 192.168.1.35 || ip.addr == 192.168.1.41)) || (ip.addr == 192.168.1.35 && (ip.addr == 192.168.1.27 || ip.addr == 192.168.1.41)) || (ip.addr == 192.168.1.41 && (ip.addr == 192.168.1.27 || ip.addr == 192.168.1.35))
```
The output can be directly pasted into Wireshark's filter input box. The default *include* filter will show only traffic between any of the given IP addresses. Using the *exclude* option will show all traffic that *does not involve* the given addresses.
## Known Issues & TODO
- Add options for ports and protocols
- Combine *include* and *exclude* results, if applicable
    - This will be more necessary when port/protocol support is added
