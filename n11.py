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
marka = ""
model = ""



urls = ["https://www.n11.com/bilgisayar/dizustu-bilgisayar?ipg={i}" for i in range(1,6)]

# count = 0

for url in urls:
    r = requests.get(url)
    soup = BeautifulSoup(r.content, features = "html.parser")

    ürünler = soup.find_all("li",attrs={"class":"column"})
    

    for ürün in ürünler:
        ürün_linkleri = ürün.find_all("div",attrs={"class":"columnContent"})
        for i in ürün_linkleri:

            link = i.find("div",attrs={"class":"pro"})
            link_devam = link.a.get("href")
            # print(link_devam)
            # count +=1

            fiyat = i.find("span", attrs = {"class": "priceEventClick"}).text
            print(fiyat)

            detay =requests.get(link_devam)
            detay_soup = BeautifulSoup(detay.content, features = "html.parser")
            #print(detay_soup)

            teknik_ayrintilar = detay_soup.find_all("div",attrs={"class":"unf-prop-context"})
            

      
            for teknik in teknik_ayrintilar: 
                
                detaylar = teknik.find_all("li")
                for i in detaylar:
                    tek_isim = i.find("p", attrs={"class":"unf-prop-list-title"}).text
                    tek_oz = i.find("p", attrs={"class":"unf-prop-list-prop"}).text
                
                    # print(etiket,"=",deger)

                    if(tek_isim == "İşlemci"):
                        islemcitipi = tek_oz
                    elif(tek_isim == "Disk Türü"):
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
                    elif(tek_isim == "Ekran Çözünürlüğü"):
                        cozunurluk = tek_oz
                    elif(tek_isim == "Bellek Kapasitesi"):
                        ram = tek_oz
                    elif(tek_isim == "İşlemci Modeli"):
                        islemcinesli = tek_oz
                    elif(tek_isim == "Marka"):
                        marka=tek_oz
                    elif(tek_isim == "Model"):
                        model = tek_oz
                
                data ={"marka" : marka, "model": model, "fiyat": fiyat, "link":link_devam,
                "islemcitipi":islemcitipi,"diskkapasitesi": diskkapasitesi, "garantitipi": garantitipi,
                "renk":renk, "isletimsistemi": isletimsistemi,"ekranboyutu": ekranboyutu,
                "islemcicekirdek":islemcicekirdek,"ram":ram,"islemcinesli":islemcinesli}
                collection.insert_one(data)

 
# print(count)          


    

