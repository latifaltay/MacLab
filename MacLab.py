import subprocess
import re
import random
from scapy.all import *


# MAC ADRESİ İŞLEMLERİ 
#####################################################################################################################################################################################################

#random mac adresi üretmemizi sağlayan fonksiyon
def get_random_mac_address():
    
    mac_parts = []

    for _ in range(6):
        # random kütüphanesi yardımıyla 0 ile 255 arasında bir byte seçiliyor
        random_byte = random.randint(0x00, 0xff)

        # seçilen byte'ı onaltılık formata çeviriyor 
        hex_byte = format(random_byte, '02x')

        # onaltılık formata çevrilen byte gruplarını mac_parts listesine ekliyoruz
        mac_parts.append(hex_byte)

    # onaltılık formata çevrilen byte gruplarını : işareti ile birleştirip mac adresi oluşturuyoruz
    mac_address = ':'.join(mac_parts)

    return mac_address


# mac adresi değiştirmeyi sağlayan fonksiyon
# kısaca subprocess kütüphanesi aracılığıyla aşağıdaki linux komutlarını çalıştırarak new_mac değişkenine atanılan random mac adresini gerçek mac adresi yerine atıyor 
def change_mac_address(interface, new_mac):
    subprocess.call(["sudo", "ifconfig", interface, "down"])
    subprocess.call(["sudo", "ifconfig", interface, "hw", "ether", new_mac])
    subprocess.call(["sudo", "ifconfig", interface, "up"])

# Mac adresinin değiştirildiğini yardıran fonksiyon
def change_mac_and_print(interface):
    new_mac_address = get_random_mac_address()
    change_mac_address(interface, new_mac_address)
    print(f"\nMAC adresi başarıyla değiştirildi. Yeni MAC adresi: {new_mac_address}")

#####################################################################################################################################################################################################



# iNTERFACE İŞLEMLERİ
#####################################################################################################################################################################################################

# Network interface'leri listeyen fonksiyon
def list_network_interfaces():
    try:
        # subprocess kütüphanesi'nin check_output özelliği ile ifconfig kodunu çalıştırıyoruz, universal_newlines=true ise ifconfig kodunun çıktısını string'e çeviriyor ve okumamızı sağlıyor
        result = subprocess.check_output(['ifconfig'], universal_newlines = True)
        return result
    except subprocess.CalledProcessError as error:
        # Eğer ifconfig kodunu çalıştırdığımızda hata alıyorsak önce hatanın kodunu sonra çıktısını dönüyoruz 
        return ("Hata Kodu: " + str(error.returncode), "\n Hata Çıktısı: " + str(error.output), " \nİnterface'ler Listelenemedi.")
    

# listelenen interface'lerden istediğimizi seçmemize olanak sağlayan fonksiyon
def select_network_interface():
    # interface'leri listeleyen fonksiyonu çağırıyoruz
    interfaces = list_network_interfaces()
    print("Mevcut İnterface'ler:")
    
    # list_network_interfaces fonksiyonunun çağırdığı sonuçları re kütüphanesi ile listeye atıyoruz
    interface_list = re.findall(r'^\S+', interfaces, re.MULTILINE)

    # listelenen interface'leri ekrana yazdırıyoruz
    for i, interface in enumerate(interface_list, 1):
        print(f"{i}. {interface}")

    
    while True:
        try:
            # listelenen interfacelerden birini kullanıcıdan alıp selection değişkenine atıyoruz
            selection = int(input("İnterface seçin (1 - n): "))
            # kullanıcıdan alınan input 1 ya da 1'den büyükse ve input interface'lerin sayısından küçükse ya da eşitse bu blok çalışır ve kullanıcının seçimine göre işlem yapmayı sağlar
            if 1 <= selection and selection <= len(interface_list):
                # diziler 0'dan başladığı için kullanıcının girdiği değerden 1 çıkartıyoruz ve kullanıcının seçmek istediği interface'nin indis numarasını bulup onu döndürüyoruz
                return interface_list[selection - 1]
            else:
                print("Geçersiz bir seçenek girdiniz. Lütfen doğru sayı girin.")
        except ValueError:
            print("Geçersiz bir giriş. Lütfen bir sayı girin.")


# random ip adresi üreten fonksiyon (Şu an kullanılmıyor ilerleyen özelliklerde eğer uygun olursa dahil edilecek)
def generate_random_ip():
    ip = []
    for _ in range(4):
        ip.append(str(random.randint(0, 255)))
    # ip dizisindeki 4 adet sayıyı . karakteri ile birleştir ve döndür
    return '.'.join(ip)

# syn paketi yollayan fonksiyon
def send_syn_packet(source_ip, target_ip, target_port, packet_count):
    # scapy kütüphanesinin bu özelliği sayesinde çıktıları ekranda görebiliyoruz bunun default değeri 2'dir.
    # fakat biz syn paketlerinin çıktısını görmek istemediğimiz için bunu 0'a çekiyoruz
    # long story short ekrana detay yazdırmak istiyorsak 2 yani default değer eğer ekrana detay yazdırmak istemiyorsak 0 yazıyoruz 
    conf.verb = 0
    
    for _ in range(packet_count):
        # paketi hangi ip'den hangi ip'ye, hangi port numarası üzerinden hangi bit'i yollayacağımızı ayarladığımız kod
        packet = IP(src=source_ip, dst=target_ip) / TCP(dport=target_port, flags="S")
        send(packet)

    print(f"SYN paketi {target_ip}:{target_port} adresine gönderildi.")


# syn paketini yolladığında ekrana yazdıran fonksiyon
def send_syn_and_print():
    source_ip = input("Kaynak IP adresini girin: ")
    target_ip = input("Hedef IP adresini girin: ")
    target_port = int(input("Hedef port numarasını girin: "))
    packet_count = int(input("Yollamak istediğiniz SYN paketlerinin sayısını giriniz: "))
    send_syn_packet(source_ip, target_ip, target_port, packet_count)




# UYGULAMANIN ANA MENÜSÜ
#####################################################################################################################################################################################################

# ana menü fonksiyonu
def main_menu():
    print("\n--- MacLab ---")
    print("1. İnterfaceleri listele ve MAC adresini değiştir")
    print("2. SYN Paketi Gönder")
    print("3. Çıkış")

#####################################################################################################################################################################################################




# MAİN METOTU
#####################################################################################################################################################################################################
def main():
    while True:
        main_menu()
        # programın ana menüsünde olan seçeneklerden birini seçmemize yardımcı olan fonksiyon
        # seçtiğimiz değeri choice değişkenine atıyor ve işlem yapıyor
        choice = input("Yukarıdakilerden Birini Seçiniz (1-3): ")

        if choice == '1':
            # eğer birinci seçeneği seçersek select_network_interface fonksiyonu çağırılıyor ve network interface'leri listeleniyor
            selected_interface = select_network_interface()
            # ardından seçtiğimiz interface'nin mac adresine random oluşturulan mac adresi atanıyor
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
