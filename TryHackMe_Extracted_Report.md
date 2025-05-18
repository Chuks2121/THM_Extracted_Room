# TryHackMe - Extracted Room Walkthrough

## Author: Chuks Ogwugwa
**Date:** May 2025  
**Platform:** TryHackMe.com  
**Room:** Extracted

---

## Overview

In this challenge, I was tasked with analyzing a packet capture file (`traffic.pcapng`) to identify suspicious activity, recover an encoded payload, perform layered decryption, extract credentials from a KeePass database, and ultimately retrieve two flags.

This report outlines the step-by-step process used, including traffic inspection, binary data extraction, XOR and base64 decoding, custom scripting, and KeePass database analysis.

---

## Tools Used
- Wireshark / TShark
- Python
- Hashcat / John the Ripper
- keepass_dump
- kpcli
- xxd

---

## Step-by-Step Process

### 1. Initial PCAP Analysis
I opened `traffic.pcapng` in **Wireshark** and noticed unusual HTTP traffic occurring over TCP port **1337**. This traffic appeared to contain encoded data.

### 2. Extract HTTP Payload (Port 1337)
Using `tshark`, I filtered for traffic sent to port 1337 with a minimum frame length, and extracted the HTTP payload:

```bash
time tshark -r traffic.pcapng -T fields -Y 'tcp.dstport == 1337 and frame.len > 100' -e data.data | xxd -ps -r > 539.dmp
```

### 3. First Layer Decryption (Base64 + XOR with 'A')
I created a Python script to decode the base64-encoded data and XOR it using key `'A'`:

```python
# get_dumpfile.py
import base64

with open('539.dmp', 'r') as file:
    encoded_data = file.read()

binary_data = base64.b64decode(encoded_data)
xor_key = b'A'
decrypted_data = bytearray(len(binary_data))

for i in range(len(binary_data)):
    decrypted_data[i] = binary_data[i] ^ xor_key[i % len(xor_key)]

with open('1337.dmp', 'wb') as file:
    file.write(decrypted_data)

print("Decryption completed, saved to 1337.dmp")
```

Executed with:
```bash
time python3 get_dumpfile.py
```

### 4. Second Layer Decryption (Base64 + XOR with 'B')
The output `1337.dmp` contained another base64 string. I saved it in a file called `Database1337` and decrypted it:

```python
# get_kdbx.py
import base64

with open('Database1337', 'r') as file:
    encoded_data = file.read()

binary_data = base64.b64decode(encoded_data)
xor_key = b'B'
decrypted_data = bytearray(len(binary_data))

for i in range(len(binary_data)):
    decrypted_data[i] = binary_data[i] ^ xor_key[i % len(xor_key)]

with open('Database1337.kdbx', 'wb') as file:
    file.write(decrypted_data)

print("Decryption completed, saved to Database1337.kdbx")
```

Executed with:
```bash
time python3 get_kdbx.py
```

### 5. Analyzing the KeePass File
I cloned the `keepass_dump` repository to extract data from the KeePass database:

```bash
git clone https://github.com/z-jxy/keepass_dump.git
cd keepass_dump
python3 keepass_dump.py -f ../1337.dmp --skip --debug
```

### 6. Generating a Brute-Force Wordlist
Based on clues, I created a simple brute-force script:

```python
# brute.py
l = '!"#$%&\'()+,-./0123456789:;?@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_abcdefghijklmnopqrstuvwxyz{|}~'
w = 'NoWaYIcanF0rGetThis123'
i = 0

while i < len(l):
    print(l[i] + w)
    i += 1
```

Executed with:
```bash
python3 brute.py > passlist.txt
```

### 7. Cracking the KeePass Password
I extracted the KeePass hash and used John to brute-force it:

```bash
keepass2john Database1337.kdbx > hash.txt
john hash.txt --wordlist=passlist.txt
```

John successfully recovered the password, which I used to open the KeePass database.

### 8. Retrieving the Flags
With the password, I accessed the database using `kpcli`:

```bash
kpcli --kdb Database1337.kdbx
```

I used the first flag as the password. Once inside:
```bash
cd Database1337/
ls
show 2
```

This revealed the final flag.

---

## Final Notes
- Layered XOR and base64 encoding are common CTF techniques; custom Python scripts are essential to reverse such transformations.
- Understanding traffic analysis and binary manipulation is crucial in real-world digital forensics and red-team operations.
- The challenge reinforced the value of tool chaining and scripting.

---

## Flags Acquired
- ✅ First Flag: Obtained via John and used as KeePass password
- ✅ Final Flag: Retrieved from within KeePass using `kpcli`

---

## References
- https://github.com/z-jxy/keepass_dump
- https://www.wireshark.org/
- https://www.openwall.com/john/
- https://hashcat.net/

---

**GitHub:** [your_username](https://github.com/your_username)

**Project Repository:** [link to this report's repo]