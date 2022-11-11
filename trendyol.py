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


urls = ["https://www.trendyol.com/laptop-x-c103108?pi={i}" for i in range(1,7)]

rate = [i/10 for i in range(10)]
count = 0
say = 0
for url in urls:
    page = requests.get(url)
    soup = BeautifulSoup(page.content, features = "html.parser")


    #tum urunlerin oldugu html kismi 
    ürünler = soup.find_all("div",attrs={"class":"p-card-wrppr"})
    #print(ürünler)
    site_url = "https://www.trendyol.com"

    #tum urunleri tek tek gezdik
    for ürün in ürünler:
        a_tag = ürün.find_all("div", attrs={"class":"p-card-chldrn-cntnr"})
        if(count == 100):
            break

        for i in a_tag:

            #linkleri alip site linki ile birlestirip url yaptik
            link = i.a.get("href")
            # print(link)
            full_link = site_url + link
            # print(full_link)
            count +=1
            #urun fotografi
            imgs = i.find("div",attrs={"class":"p-card-img-wr"})
            for img in imgs:
                foto = img["src"]
                #print(foto)
            #marka adi
            markabs = i.find("span", attrs = {"class":"prdct-desc-cntnr-ttl"}).text            
            #model adi
            modelbs = i.find("span",attrs = {"class":"prdct-desc-cntnr-name"}).text
            #print(model)
            #fiyat bilgisi
            fiyatbs = i.find("div", attrs = {"class": "prc-box-dscntd"}).text
            # print(fiyat)
            #print(marka)
            #laptoplarin ozelliklerini almak icin linklerin icinde gezdik
            ozellikler = requests.get(full_link)
            ozellik_soup = BeautifulSoup(ozellikler.content, features = "html.parser")
            #teknik ozelliklerin bulundugu tablo
            teknik = ozellik_soup.find_all("li",attrs={"class":"detail-attr-item"})
            # puanlar = ozellik_soup.find_all("div",attrs={"class":"pr-rnr-sm-p"})
            # print(puanlar)
            # for a in puanlar:
            #     puan = a.span.find("span",recursive= False)
            #     print(puan)
            for j in teknik:
                #teknik ozelligin adi(key)
                tek_isim = j.find("span").text
                #teknik ozellik(value)
                tek_oz = j.find("b").text
                #print(tek_isim)
                #print(tek_oz)

                if(tek_isim == "İşlemci Tipi"):
                    islemcitipi = tek_oz
                elif(tek_isim == "SSD Kapasitesi"):
                    diskkapasitesi = tek_oz
                elif(tek_isim == "Garanti Tipi"):
                    garantitipi = tek_oz
                elif(tek_isim == "Renk"):
                    renk = tek_oz
                elif(tek_isim == "İşletim Sistemi"):
                    isletimsistemi = tek_oz
                elif(tek_isim == "Ekran Boyutu"):
                    ekranboyutu = tek_oz
                elif(tek_isim == "İşlemci Çekirdek Sayısı"):
                    islemcicekirdek = tek_oz
                elif(tek_isim == "Çözünürlük"):
                    cozunurluk = tek_oz
                elif(tek_isim == "Ram (Sistem Belleği)"):
                    ram = tek_oz
                elif(tek_isim == "İşlemci Nesli"):
                    islemcinesli = tek_oz

            data ={"marka" : markabs, "model": modelbs, "fiyat": fiyatbs, "link":full_link,
             "islemcitipi":islemcitipi,"diskkapasitesi": diskkapasitesi, "garantitipi": garantitipi,
             "renk":renk, "isletimsistemi": isletimsistemi,"ekranboyutu": ekranboyutu,
             "islemcicekirdek":islemcicekirdek,"ram":ram,"islemcinesli":islemcinesli}
            collection.insert_one(data)
    time.sleep(random.choice(rate))

print(count)

