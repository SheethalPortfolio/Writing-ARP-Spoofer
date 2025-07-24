# Q1 - ARP Spoofer using Scapy

## Student Details
Name: Sheethal Santhanam
Module: CSCI369 Ethical Hacking (S3 2025)  
Environment: Kali Linux (Attacker), Metasploitable2 (Victim)

---

## Description
This Python script performs an ARP spoofing attack using the Scapy library.
It runs on the Kali Linux VM and targets a victim (Metasploitable2) and
the default gateway (router). The script continuously sends spoofed ARP
replies to trick both devices into believing the attacker’s MAC address is 
associated with the other device’s IP. This results in a man-in-the-middle
(MITM) attack where Kali intercepts traffic between the victim and the router.

The attack stops safely when the user presses `CTRL+C`, after which the
script restores the original ARP entries using real MAC addresses
returning the network to its normal state.

---

## How to Run
This script requires **root privileges**, so use `sudo`:

    sudo python3 arpspoof.py <Victim_IP> <Router_IP>

My code:
    sudo python3 arpspoof.py 10.0.2.4 10.0.2.1

---

## How to Test
1. Run the script in one Kali terminal.
2. While it runs, switch to Metasploitable2 VM.
3. In Meta2, type: `arp -a`
4. Look at the MAC shown for the router IP (e.g. `10.0.2.1`)
5. Run `ifconfig` in Kali to compare MAC addresses.
6. If they match — spoofing was successful ✅
7. Press `CTRL+C` in Kali to stop the attack and restore ARP tables.
8. Run `arp -a` again in Meta2 to confirm the table is back to normal.

---

## Requirements
- Kali Linux (Python 3.11+)
- Metasploitable2 (on same VirtualBox network)
- Scapy: install with `sudo apt install python3-scapy`

---

## Files Submitted
- `arpspoof.py` – The main Python script
- `readme.txt` – This documentation file

