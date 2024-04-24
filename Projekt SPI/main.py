from ObliczanieSPI.ObliczanieSPI import *
from PrzygotowanieDanych.AnalizaLokalizacji import *
from PrzygotowanieDanych.IniekcjaEDA import *
from PrzygotowanieDanych.Mapowanie import *
from PrzygotowanieDanych.PobranieDanych import *
from PrzygotowanieDanych.WyborStacji import *
from Wizualizacje.Wizualizacje import *

# Wszystkie stacje pomiarowe zlokalizowane w Małopolsce
malopolska_stations = stations_in_malopolska()

#--------- Krzysiek - pobranie wszystkich danych z 30 lat ----------------
all_stations_data = download_weather_data()

#---------- Michał - stacje pomiarowe w Małopolsce z pomiarami opadów
opady_malopolska = rain_malopolska(all_stations_data, malopolska_stations)
# -------------------
stacje_z_zakresem_30 = stations_with_range(opady_malopolska)
opady_malopolska_spi = merge_rain_malopolska_range(opady_malopolska,stacje_z_zakresem_30)
opady_malopolska_iniekcja = fill_missing_values(opady_malopolska_spi)

plot_malopolska_stations(malopolska_stations,stacje_z_zakresem_30)

spi_all_stations = function_spi_df(opady_malopolska_iniekcja)
save_spi_excel(spi_all_stations)

plot_spi(spi_all_stations)

results_df = statistics_spi(spi_all_stations)

merged_data = pd.merge(results_df, malopolska_stations, left_on='Kod stacji', right_on='Kod stacji', how='left')
plot_spi_median(merged_data)