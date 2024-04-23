import requests
import pandas as pd
import io
from zipfile import ZipFile, BadZipFile
# ---------------------------------------------Krzysiek ----------------------------------------------------------------
# Pobieranie danych pomiarowych z 30 lat
def download_weather_data():
    columns = ["Kod stacji", "Nazwa stacji", "Rok", "Miesiąc", "Dzień", "Suma dobowa opadów [mm]",
               "Status pomiaru SMDB",
               "Rodzaj opadu [S/W/ ]", "Wysokość pokrywy śnieżnej [cm]", "Status pomiaru PKSN",
               "Wysokość świeżospałego śniegu [cm]",
               "Status pomiaru HSS", "Gatunek śniegu  [kod]", "Status pomiaru GATS", "Rodzaj pokrywy śnieżnej [kod]",
               "Status pomiaru RPSN"]
    dane = pd.DataFrame(columns=columns)
    lata = ["1991_1995/", "1996_2000/", "2001/", "2002/", "2003/", "2004/", "2005/", "2006/", "2007/", "2008/",
            "2009/", "2010/", "2011/", "2012/", "2013/", "2014/", "2015/", "2016/", "2017/", "2018/", "2019/",
            "2020/", "2021/", "2022/", "2023/", "2024/"]

    base_url = "https://danepubliczne.imgw.pl/data/dane_pomiarowo_obserwacyjne/dane_meteorologiczne/dobowe/opad/"

    # Iteracja przez lata
    for rok in lata:
        if "_" in rok:
            rok_start, rok_end = map(int, rok.rstrip("/").split("_"))
            url = base_url + rok + f"{rok_start}_o.zip"
            response = requests.get(url)
            # print(f"{url}")
            print(f"Response_code = {response.status_code}, Pobieranie danych dla roku = {rok}")
            # Sprawdzenie, czy żądanie się powiodło
            if response.status_code == 200:
                # Wczytanie danych z pliku ZIP do ramki danych
                try:
                    with ZipFile(io.BytesIO(response.content)) as z:
                        for file_name in z.namelist():
                            with z.open(file_name) as f:
                                # Ustawienie odpowiedniego kodowania
                                df = pd.read_csv(f, delimiter=",", header=None, names=columns, encoding="latin-1")
                                dane = pd.concat([dane, df], ignore_index=True)
                except BadZipFile:
                    print(f"Bad ZIP file for {rok}")
        else:
            print(f"Response_code = {response.status_code}, Pobieranie danych dla roku ={rok}")
            for miesiac in range(1, 13):
                # Pobieranie pliku ZIP
                url = base_url + rok + f"{rok[:-1]}_{miesiac:02d}_o.zip"
                response = requests.get(url)
                # print(f"Tu jestem 2 - response_code = {response.status_code}, rok = {rok}, miesiac = {miesiac}")
                # Sprawdzenie, czy żądanie się powiodło
                if response.status_code == 200:
                    # Wczytanie danych z pliku ZIP do ramki danych
                    try:
                        with ZipFile(io.BytesIO(response.content)) as z:
                            for file_name in z.namelist():
                                with z.open(file_name) as f:
                                    # Ustawienie odpowiedniego kodowania
                                    df = pd.read_csv(f, delimiter=",", header=None, names=columns, encoding="latin-1")
                                    dane = pd.concat([dane, df], ignore_index=True)
                    except BadZipFile:
                        print(f"Bad ZIP file for {rok}")
    return dane
# --------------------------------------------------------------------------------------------------------------------------
