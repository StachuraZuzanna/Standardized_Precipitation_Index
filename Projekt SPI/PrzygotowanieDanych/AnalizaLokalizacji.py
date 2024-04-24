import geopandas as gpd
import pandas as pd
from shapely.geometry import Polygon
from shapely.geometry import Point
import pyproj
#------------------------------Zuzia---------------------------------
# Funkcja do konwersji współrzędnych na obiekty Shapely Point
def convert_to_point(row):
    lat, lon = row['Szerokość geograficzna'], row['Długość geograficzna']
    lat_deg, lat_min, lat_sec = map(float, lat.split())
    lon_deg, lon_min, lon_sec = map(float, lon.split())
    latitude = lat_deg + lat_min / 60 + lat_sec / 3600
    longitude = lon_deg + lon_min / 60 + lon_sec / 3600
    return Point(longitude, latitude)

# Czytanie wszystkich stacji pomiarowych
def all_stations():
    data = pd.read_csv('Data/kody_stacji.csv', encoding='windows-1250', delimiter=";")
    #Zwykłe kodowanie utf-8 nie działało --> po otwarciu pliku w Excelu można sprawdzić rodzaj kodowania 
    data = data.set_index('LP.')   #ustawiam indeks 
    data['geometry'] = data.apply(convert_to_point, axis=1)

    # Tworzenie ramki GeoPandas
    data_gfd = gpd.GeoDataFrame(data, geometry='geometry')
    return data_gfd

#Granice Małopolski
def malopolska_borders():
    # Wczytaj granice Małopolski jako obiekt typu Polygon
    granice_malopolski = gpd.read_file('Data/malopolska.shp')
    polygon_epsg2180 = granice_malopolski.geometry.iloc[0]
    
    # Utwórz transformator do przekształcania współrzędnych
    transformer = pyproj.Transformer.from_crs("EPSG:2180", "EPSG:4326", always_xy=True)
    
    # Przekształć współrzędne poligonu na współrzędne geograficzne
    polygon_wgs84_coords = []
    for x, y in polygon_epsg2180.exterior.coords:
        lon, lat = transformer.transform(x, y)
        polygon_wgs84_coords.append((lon, lat))
    
    # Utwórz obiekt poligonu w formacie EPSG:4326 (współrzędne geograficzne)
    polygon_wgs84 = Polygon(polygon_wgs84_coords)
    # Utworzenie GeoDataFrame z pojedynczym wierszem zawierającym ten poligon
    granice_malopolski = gpd.GeoDataFrame({'geometry': [polygon_wgs84]})
    return granice_malopolski
    
#Szukanie stacji pomiarowych tylko w Małopolsce
def stations_in_malopolska():
    data_gfd = all_stations()
    # Znajdź punkty wewnątrz granic Małopolski
    granice_maloposki = malopolska_borders()
    punkty_wewnatrz_malopolski = gpd.sjoin(data_gfd, granice_maloposki, how="inner", predicate="within")
    punkty_wewnatrz_malopolski = punkty_wewnatrz_malopolski.rename(columns={'ID': 'Kod stacji'})
    return punkty_wewnatrz_malopolski