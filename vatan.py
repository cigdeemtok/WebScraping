from asyncio.windows_events import NULL
import requests
from bs4 import BeautifulSoup
import time
import random
import pymongo
from pymongo import MongoClient

cluster = MongoClient("mongodb://localhost:27017")
db = cluster["yazlab"]
collection = db["notebooks"]

diskkapasitesi =""
garantitipi =""
renk = ""
islemcitipi = ""
isletimsistemi = ""
ekranboyutu = ""
islemcicekirdek = ""
cozunurluk = ""
ram = ""
islemcinesli = ""

urls = ["https://www.vatanbilgisayar.com/laptop/?page={i}" for i in range(1,6)]

rate = [i/10 for i in range(10)]
# count = 0 

for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features = "html.parser")
    
    ürünler = soup.find_all("div", attrs = {"class":"product-list"})
    #print(ürünler)
    link_basi = "https://www.vatanbilgisayar.com"

    for ürün in ürünler:
        # print(ürün)
        # count +=1
        link = ürün.a.get("href")
        full_link = link_basi + link
        #print(full_link) 
        model = ürün.find("div",attrs={"class":"product-list__product-name"}).text
        # print(model)
        marka = model.split(" ",1)
        marka_adi = marka[0]
        # print(marka_adi)
        fiyat = ürün.find("span", attrs = {"class":"product-list__price"}).text
        # print(fiyat)

        ozellikler = requests.get(full_link)
        ozellik_soup = BeautifulSoup(ozellikler.content, features = "html.parser")
        # print(ozellik_soup)

        teknik = ozellik_soup.find_all("table", attrs = {"class":"product-table"})
        # scores = ozellik_soup.find_all("div", attrs= {"class":"wrapper-star"})
    
        # for j in scores:
        #     puan = j.find("strong", attrs = {"id":"averageRankNum"})
        #     print(puan)
    
    
        for i in teknik:
            rows = i.find("tr")
            tek_isim = rows.find("td").text
            tek_oz = rows.find("p").text
            # print(ad)
            # print(t_oz)
            # print("****************")
            if(tek_isim == "İşlemci Teknolojisi"):
                islemcitipi = tek_oz
            elif(tek_isim == "Disk Kapasitesi"):
                diskkapasitesi = tek_oz
            elif(tek_isim == "Garanti"):
                garantitipi = tek_oz
            elif(tek_isim == "Renk"):
                renk = tek_oz
            elif(tek_isim == "İşletim Sistemi"):
                isletimsistemi = tek_oz
            elif(tek_isim == "Ekran Boyutu"):
                ekranboyutu = tek_oz
            elif(tek_isim == "İşlemci Çekirdek Sayısı"):
                islemcicekirdek = tek_oz
            elif(tek_isim == "Çözünürlük (Piksel)"):
                cozunurluk = tek_oz
            elif(tek_isim == "Ram (Sistem Belleği)"):
                ram = tek_oz
            elif(tek_isim == "İşlemci Nesli"):
                islemcinesli = tek_oz
            

        data ={"marka" : marka_adi, "model": model, "fiyat": fiyat, "link":full_link,
        "islemcitipi":islemcitipi,"diskkapasitesi": diskkapasitesi, "garantitipi": garantitipi,
        "renk":renk, "isletimsistemi": isletimsistemi,"ekranboyutu": ekranboyutu,
        "islemcicekirdek":islemcicekirdek,"ram":ram,"islemcinesli":islemcinesli}
        collection.insert_one(data)
    
    time.sleep(random.choice(rate))

# print(count)



