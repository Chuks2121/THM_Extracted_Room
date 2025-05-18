# TryHackMe - Extracted Room

This repository contains the full write-up and all associated scripts used to complete the **Extracted** room on [TryHackMe](https://tryhackme.com/).

## 📁 Contents

- `TryHackMe_Extracted_Report.md` - Detailed professional walkthrough report.
- `README.md` - Overview of the challenge and project.
- `scripts/` - Custom Python scripts used to decode and extract data.
- `passlist.txt` - Generated wordlist for brute-forcing KeePass.
- `hash.txt` - Extracted KeePass hash (replace with your own).
- `Database1337.kdbx` - Final KeePass file (not included due to sensitivity).

## ⚒️ Tools Used

- Wireshark / TShark
- Python 3
- John the Ripper
- keepass_dump
- kpcli

## 🚀 How to Use

1. Analyze network traffic in `traffic.pcapng`.
2. Use the included `scripts/` for decoding base64 + XOR encoded files.
3. Run brute-force script to generate a password list.
4. Crack the KeePass database using `john`.
5. Open the database with `kpcli` to retrieve flags.

## 💡 Key Learning Points

- Packet inspection and custom data extraction.
- Multi-layer encoding reversal.
- KeePass decryption and analysis.

## 📄 License

This project is for educational purposes only.

---

**Author:** [Chuks Ogwugwa](https://github.com/your_username)  
**Room:** TryHackMe - Extracted