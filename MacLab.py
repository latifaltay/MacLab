import subprocess
import re
import random

def list_network_interfaces():
    try:
        result = subprocess.check_output(['ifconfig'], universal_newlines=True)
        return result
    except subprocess.CalledProcessError:
        return "Ağ arabirimleri listelenemedi."

# network intefaceleri listeleyen fonksiyon
def select_network_interface():
    interfaces = list_network_interfaces()
    print("Mevcut ağ arabirimleri:")
    interface_list = re.findall(r'^\S+', interfaces, re.MULTILINE)
    for i, interface in enumerate(interface_list, 1):
        print(f"{i}. {interface}")

    while True:
        try:
            # kullanıcının bir ağ arabirimi seçmesini sağlayan fonksiyon
            selection = int(input("İnterface seçin (1 - n): "))
            if 1 <= selection <= len(interface_list):
                return interface_list[selection - 1]
            else:
                print("Geçersiz bir seçenek girdiniz. Lütfen doğru sayı girin.")
        except ValueError:
            print("Geçersiz bir giriş. Lütfen bir sayı girin.")

# random Mac adresi üretici fonksiyon
def get_random_mac_address():
    return ':'.join([format(random.randint(0x00, 0xff), '02x') for _ in range(6)])

# seçilen interface'e yeni Mac adresini tanımlayan fonksiyon
def change_mac_address(interface, new_mac):
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

# ana menüyü gösteren fonksiyon
def main_menu():
    print("\n--- MacLab ---")
    print("1. İnterfaceleri listele ve MAC adresini değiştir")
    print("2. Farklı Özellik")
    print("3. Daha Farklı Özellik")
    print("4. Çıkış")

def main():
    while True:
        # ana program döngüsü
        # bu döngü çalıştığı sürece kullanıcı seçim yapıp programın farklı özelliklerini kullanabilecek (Veri Yapıları bilgisi)
        
        main_menu()
        choice = input("Yukarıdakilerden Birini Seçiniz (1-4): ")

        if choice == '1':
            # interfaceleri listeleyip, seçilen interface'e rastgele bir Mac adresi atama
            selected_interface = select_network_interface()
            new_mac_address = get_random_mac_address()
            change_mac_address(selected_interface, new_mac_address)
            print(f"\nMAC adresi başarıyla değiştirildi. Yeni MAC adresi: {new_mac_address}")
        elif choice == '2':
            # örnek özellik
            print("\n Farklı Özellik")
        elif choice == '3':
            # örnek özellik
            print("\n Daha Farklı Özellik")
        elif choice == '4':
            # programdan çıkış
            print("\nProgramdan çıkılıyor.")
            break
        else:
            # hatalı seçim uyarısı 
            print("\nGeçersiz bir seçenek girdiniz. Lütfen 1-4 arasında bir numara girin.")

if __name__ == "__main__":
    main()
