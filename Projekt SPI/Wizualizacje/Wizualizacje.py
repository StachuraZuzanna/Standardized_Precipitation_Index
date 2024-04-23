import matplotlib.pyplot as plt
import geopandas as gpd
import os
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
    plt.show()
    plt.savefig("Polska_stations.png")
    
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
    plt.show() 

    
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

        plt.show()