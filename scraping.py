from lib2to3.pgen2 import driver
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from bs4 import BeautifulSoup
import pandas as pd
import time

# setting webdriver
option = webdriver.ChromeOptions()
option.add_argument("--headless")
service = Service('chromedriver.exe')

driver = webdriver.Chrome(service=service, options=option)

# Masukan keyword yang ingin dicari dan halaman berapa yang akan di tuju
keyword = input("Enter the keyword: ")
page = int(input("Enter the page number: "))
shopee_url = 'https://shopee.co.id/search?keyword={}&page={}'.format(keyword, page)

# set ukutan window untuk screanshoot
driver.set_window_size(1920, 1080)

# ambil url
driver.get(shopee_url)   

rentang = 200

for i in range(1, 20):
    end = rentang * i
    aksi = "window.scrollTo(0, {})".format(end)
    driver.execute_script(aksi)
    time.sleep(1) 

time.sleep(5)
# ambil gambar page
driver.save_screenshot('screenshot.png')

    
content = driver.page_source
driver.quit()

# setting BeautifulSoup
data = BeautifulSoup(content, 'html.parser')
# print(data.encode('utf-8'))
count = 0

# list untuk menyimpan dataFrame
list_merk, list_price, list_location, list_buy = [], [], [], []

# looping untuk mengambil data
for d in data.find_all('div', 'col-xs-2-4 shopee-search-item-result__item'):
    count += 1
    print('---------------')
    print('prosessing ke-{}'.format(count))
    merk = d.find('div', 'ie3A+n bM+7UW Cve6sh').get_text()
    price = d.find('span', 'ZEgDH9').get_text()
    location = d.find('div', 'zGGwiV').get_text()
    terjual = d.find('div', 'r6HknA uEPGHT')
    if terjual != None:
        terjual = d.find('div', 'r6HknA uEPGHT').get_text()
        
    list_merk.append(merk)
    list_price.append(price)
    list_location.append(location)
    list_buy.append(terjual)

# menyimpan data ke dataframe lalu menyimpan ke csv
df = pd.DataFrame({'merk': list_merk, 'price': list_price, 'location': list_location, 'buy': list_buy})
df.to_csv('hasil/hasil_scaping_{}_page-{}.csv'.format(keyword, page), index=False)  