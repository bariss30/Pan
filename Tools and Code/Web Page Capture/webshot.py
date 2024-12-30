from selenium import webdriver
from time import sleep

#  URL'leri oku
def get_urls_from_file(file_path):
    with open(file_path, 'r') as file:
        urls = file.readlines()  # tüm satırları
    return [url.strip() for url in urls]  # boşlukları temizle

# URL'leri dosyadan al
file_path = 'urls.txt'
websites = get_urls_from_file(file_path)

# Chrome WebDriver'ı başlat
driver = webdriver.Chrome()

# Her bir URL için ekran görüntüsü al
for idx, website in enumerate(websites):
    driver.get(website)  # Web sitesini aç
    sleep(2)  # Sayfanın yüklenmesi için 
    driver.get_screenshot_as_file(f"capture_{idx + 1}.png")  # Ekran görüntüsünü 

# Tarayıcıyı kapat
driver.quit()
