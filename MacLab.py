import subprocess
import re
import random
from scapy.all import *

def list_network_interfaces():
    try:
        result = subprocess.check_output(['ifconfig'], universal_newlines=True)
        return result
    except subprocess.CalledProcessError:
        return "İnterface'ler listelenemedi."

def select_network_interface():
    interfaces = list_network_interfaces()
    print("Mevcut İnterface'ler:")
    interface_list = re.findall(r'^\S+', interfaces, re.MULTILINE)
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

def change_mac_address(interface, new_mac):
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

def get_random_mac_address():
    return ':'.join([format(random.randint(0x00, 0xff), '02x') for _ in range(6)])

def generate_random_ip():
    ip = []
    for _ in range(4):
        ip.append(str(random.randint(0, 255)))
    return '.'.join(ip)

def send_syn_packet(source_ip, target_ip, target_port):
    conf.verb = 0
    packet = IP(src=source_ip, dst=target_ip) / TCP(dport=target_port, flags="S")
    send(packet)

def change_mac_and_print(interface):
    new_mac_address = get_random_mac_address()
    change_mac_address(interface, new_mac_address)
    print(f"\nMAC adresi başarıyla değiştirildi. Yeni MAC adresi: {new_mac_address}")

def send_syn_and_print():
    source_ip = input("Kaynak IP adresini girin: ")
    target_ip = input("Hedef IP adresini girin: ")
    target_port = int(input("Hedef port numarasını girin: "))
    send_syn_packet(source_ip, target_ip, target_port)
    print(f"SYN paketi {target_ip}:{target_port} adresine gönderildi.")

def main_menu():
    print("\n--- MacLab ---")
    print("1. İnterfaceleri listele ve MAC adresini değiştir")
    print("2. SYN Paketi Gönder")
    print("3. Çıkış")

def main():
    while True:
        main_menu()
        choice = input("Yukarıdakilerden Birini Seçiniz (1-3): ")

        if choice == '1':
            selected_interface = select_network_interface()
            change_mac_and_print(selected_interface)
        elif choice == '2':
            send_syn_and_print()
        elif choice == '3':
            print("\nProgramdan çıkılıyor.")
            break
        else:
            print("\nGeçersiz bir seçenek girdiniz. Lütfen 1-3 arasında bir numara girin.")

if __name__ == "__main__":
    main()
