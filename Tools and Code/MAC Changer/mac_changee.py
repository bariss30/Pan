import random
import subprocess
import re

# MAC adresi için kullanılacak karakterler
charList = ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "A", "B", "C", "D", "E", "F"]

# Yeni MAC adresini oluştur
newMac = ""
for i in range(12):
    newMac += random.choice(charList)

# MAC adresini 2'li gruplara ayırarak, ":" ile ayıran formatta yazdır
formattedMac = ':'.join([newMac[i:i+2] for i in range(0, len(newMac), 2)])

# Ağ arayüzü bilgilerini almak için ifconfig komutunu çalıştır
ifconfigResult = subprocess.check_output("ifconfig eth0", shell=True).decode()

# Eski MAC adresini çekmek için regex kullan
oldMac = re.search("ether (\S+)", ifconfigResult).group(1)

# Yeni MAC adresi ile ağ arayüzünü güncelle
subprocess.check_output("ifconfig eth0 down", shell=True)
subprocess.check_output(f"ifconfig eth0 hw ether {formattedMac}", shell=True)
subprocess.check_output("ifconfig eth0 up", shell=True)

# Eski ve yeni MAC adreslerini yazdır
print("Old MAC:", oldMac)
print("New MAC:", formattedMac)
