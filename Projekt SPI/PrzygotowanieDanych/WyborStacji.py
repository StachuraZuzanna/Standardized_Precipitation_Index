import pandas as pd
def stations_with_range(opady_malopolska):
    result = pd.DataFrame(columns=['Kod stacji', 'Nazwa', 'geometry', 'Zakres dat'])
    for station_code in opady_malopolska['Kod stacji'].unique():
        # Wybierz dane dla danego kodu stacji
        data_for_ID = opady_malopolska[opady_malopolska['Kod stacji'] == station_code]

        # Określ maksymalną i minimalną datę
        min_year = data_for_ID['Data'].dt.year.min()
        max_year = data_for_ID['Data'].dt.year.max()

        # Obliczanie długości trwania zakresu dat
        dl = max_year - min_year

        station_name = data_for_ID['Nazwa'].iloc[0]  # Pobierz nazwę stacji
        geometry = data_for_ID['geometry'].iloc[0]  # Pobierz geometrię stacji

        # Dodaj wiersz do wynikowej ramki danych
        result = pd.concat([result, pd.DataFrame({'Kod stacji': [station_code], 'Nazwa': [station_name],
                                                  'geometry': [geometry], 'Zakres dat': [f"{min_year} - {max_year}"],
                                                  'Długość': dl})], ignore_index=True)

        # Filtracja stacji, które mają zakres lat minimum 30letni
        stacje_30lat = result[result['Długość'] >= 30]
        stacje_30lat = stacje_30lat.reset_index(drop=True)

    return stacje_30lat

## Zmergowanie danych opadowych z małopolski ze stacjami które mają zakres 30 lat danych, tak aby zostawić te stacje i pomiary dla nich
def merge_rain_malopolska_range(opady_malopolska,stacje_30lat):
    lokalizowane_stacje = opady_malopolska.loc[opady_malopolska['Nazwa'].isin(stacje_30lat['Nazwa'])]

    return lokalizowane_stacje