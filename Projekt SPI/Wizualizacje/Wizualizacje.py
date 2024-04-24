import matplotlib.pyplot as plt
import geopandas as gpd
import os
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from matplotlib.colors import Normalize
import matplotlib.cm as cm
from matplotlib.cm import ScalarMappable

from PrzygotowanieDanych.AnalizaLokalizacji import *
 #------------------------------------------------ Wizualizacje --------------------------------------------
#Wizualizacja wszystkich stacji pomiarowych na mapie
def plot_all_stations(data_gfd):

    # Wczytanie granic administracyjnych Polski
    poland = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    poland = poland[poland.name == 'Poland']
    
    # Tworzenie mapy
    fig, ax = plt.subplots(figsize=(7, 5))
    poland.plot(ax=ax, color='lightgreen', edgecolor='black')
    data_gfd.plot(ax=ax, marker='o', color='red', markersize=1)
    plt.title('Mapa Polski ze wszystkimi stacjami')
    plt.xlabel('Długość geograficzna')
    plt.ylabel('Szerokość geograficzna')

    plt.savefig("Polska_stations.png")
    plt.close()
    
#Wizualizacja stacji pomiarowych w Małopolsce - krzyżykiem zaznaczono stacje z których otrzymano pomiary opadów
def plot_malopolska_stations(malopolska_stations,opady_malopolska):
    opady_plot = opady_malopolska[['Kod stacji','Nazwa','geometry']].drop_duplicates()
    # Tworzenie ramki GeoPandas z podanymi danymi
    opady_plot = gpd.GeoDataFrame(opady_plot, geometry='geometry')
    granice_maloposki = malopolska_borders()
    
    fig, ax = plt.subplots(figsize=(10, 5))
    # poland.plot(ax=ax, color='lightgreen', edgecolor='black')
    granice_maloposki.plot(ax=ax,color="lightblue")
    opady_plot.plot(ax=ax, marker='x', color='blue',alpha=0.7,label='Stacje, dla których wykonano pomiary opadów z ponad 30 lat')
    malopolska_stations.plot(ax=ax, marker='o', color='red',alpha=0.5,markersize=1,label='Wszystkie stacje pomiarowe')
                
    plt.legend()
    
    plt.title('Mapa Małopolski ze stacjami')
    plt.xlabel('Długość geograficzna')
    plt.ylabel('Szerokość geograficzna')
    if not os.path.exists("Results"):
        os.makedirs("Results")
    plt.savefig(os.path.join("Results", "Małopolska_stations.png"))
    plt.close()

    
# -------------------------------------------------------------------------------------------------------------

# ------------------------------------------------- SPI ---------------------------------------------------------
def plot_spi(spi_all_stations):
    kody_stacji = spi_all_stations['Kod stacji'].unique()
    for kod in kody_stacji:
        stacja = spi_all_stations[spi_all_stations['Kod stacji'] == kod].copy()
        stacja = stacja.reset_index(drop=True)
        nazwa = stacja['Nazwa'][0]
        fig, ax = plt.subplots(1, 3, figsize=(13, 4))
        ax[0].plot(stacja['Date'], stacja['SPI-1'], marker='o', linestyle='-')
        ax[0].set_title(f'Zmienność SPI-1 w czasie dla {kod}')  # Fix: set_title instead of title
        ax[0].set_xlabel('Data')  # Fix: set_xlabel instead of xlabel
        ax[0].set_ylabel('SPI')  # Fix: set_ylabel instead of ylabel
        ax[0].grid(True)
        ax[0].tick_params(axis='x', rotation=45)  # Fix: tick_params to set rotation of x-axis labels
        ax[1].plot(stacja['Date'], stacja['SPI-3'], marker='o', linestyle='-')
        ax[1].set_title(f'Zmienność SPI-3 w czasie dla {kod}')  # Fix: set_title instead of title
        ax[1].set_xlabel('Data')  # Fix: set_xlabel instead of xlabel
        ax[1].set_ylabel('SPI')  # Fix: set_ylabel instead of ylabel
        ax[1].grid(True)
        ax[1].tick_params(axis='x', rotation=45)  # Fix: tick_params to set rotation of x-axis labels
        ax[2].plot(stacja['Date'], stacja['SPI-12'], marker='o', linestyle='-')
        ax[2].set_title(f'Zmienność SPI-12 w czasie dla {kod} ')  # Fix: set_title instead of title
        ax[2].set_xlabel('Data')  # Fix: set_xlabel instead of xlabel
        ax[2].set_ylabel('SPI')  # Fix: set_ylabel instead of ylabel
        ax[2].grid(True)
        ax[2].tick_params(axis='x', rotation=45)  # Fix: tick_params to set rotation of x-axis labels
        plt.suptitle(f'Wykresy zmienności SPI w czasie dla stacji {nazwa}', fontsize=16)  # Title for the entire set of plots

        plt.tight_layout()  # Dostosowanie układu, aby uniknąć obcięcia etykiet osi X
        if not os.path.exists("Results/SPI_plots"):
            os.makedirs("Results/SPI_plots")
        plt.savefig(os.path.join("Results/SPI_plots", f'{nazwa} - zmienność wartości SPI.png'))

        plt.close()


# Wykres z wynikami mediany SPI-12
def plot_spi_median(merged_data):
    # Utworzenie ramki GeoPandas z danymi stacji
    gdf_stations = gpd.GeoDataFrame(merged_data, geometry='geometry')
    granice_maloposki = malopolska_borders()

    # Utworzenie mapy
    fig, ax = plt.subplots(figsize=(10, 8))

    # Narysowanie granic Małopolski na mapie
    granice_maloposki.plot(ax=ax, color="lightblue")

    # Ustawienie kolorów na podstawie wartości "Mediana SPI-12"
    norm = Normalize(vmin=gdf_stations['Mediana SPI-12'].min(), vmax=gdf_stations['Mediana SPI-12'].max())
    colors = plt.cm.coolwarm(norm(gdf_stations['Mediana SPI-12']))

    # Narysowanie stacji na mapie, gdzie intensywność koloru odpowiada wartości "Mediana SPI-12"
    gdf_stations.plot(ax=ax, color=colors, marker='o', markersize=100, legend=True)

    # Dodanie legendy
    sm = ScalarMappable(cmap='coolwarm', norm=norm)
    sm.set_array([])
    cbar = plt.colorbar(sm, ax=ax)
    cbar.set_label('Mediana SPI-12')

    # Ustawienie tytułu mapy
    plt.title('Stacje z wartościami Mediana SPI-12')
    plt.legend()

    # Ustawienie ścieżki dla zapisu pliku
    if not os.path.exists("Results/"):
        os.makedirs("Results/")
    plt.savefig(os.path.join("Results/", 'Mapa_mediana_SPI-12.png'))
    plt.close()
