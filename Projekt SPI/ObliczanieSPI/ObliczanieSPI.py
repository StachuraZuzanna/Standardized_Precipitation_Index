from scipy.stats import gamma, norm
import pandas as pd
import os

def calculate_spi(data):
    alpha, loc, beta = gamma.fit(data.dropna(), floc=0)
    cdf = gamma.cdf(data, alpha, loc=loc, scale=beta)
    spi = norm.ppf(cdf)
    return spi


def function_spi_df(opady_malopolska_iniekcja):
    kody_stacji = opady_malopolska_iniekcja['Kod stacji'].unique()
    all_results = pd.DataFrame()
    for kod in kody_stacji:
        stacja = opady_malopolska_iniekcja[opady_malopolska_iniekcja['Kod stacji'] == kod].copy()
        stacja.loc[:, 'Suma_mies'] = stacja.groupby(['Rok', 'Miesiąc'])['Suma dobowa opadów [mm]'].transform('sum')
        stacja = stacja.reset_index(drop=True)

        suma_mies = stacja.groupby(['Kod stacji', 'Rok', 'Miesiąc'])['Suma_mies'].mean().reset_index()
        suma_mies['Suma_3_mies'] = suma_mies['Suma_mies'].rolling(window=3).sum()
        suma_mies['Suma_12_mies'] = suma_mies['Suma_mies'].rolling(window=12).sum()
        suma_mies

        # SPI - 1
        stacja_spi1 = suma_mies[suma_mies['Suma_mies'] > 0].reset_index(drop=True)
        stacja_spi1.loc[:, 'SPI-1'] = calculate_spi(stacja_spi1['Suma_mies'])
        stacja_spi1.loc[:, 'SPI-3'] = calculate_spi(stacja_spi1['Suma_3_mies'])
        stacja_spi1.loc[:, 'SPI-12'] = calculate_spi(stacja_spi1['Suma_12_mies'])

        stacja_spi1['Date'] = pd.to_datetime(
            stacja_spi1[['Rok', 'Miesiąc']].rename(columns={'Rok': 'year', 'Miesiąc': 'month'}).assign(day=1))

        stacja_spi1 = stacja_spi1.reindex(columns=['Kod stacji', 'Rok', 'Miesiąc', 'SPI-1', 'SPI-3', 'SPI-12', 'Date'])

        all_results = pd.concat([all_results, stacja_spi1], ignore_index=True)
        kody_stacji = all_results['Kod stacji'].unique()
        station_names = {}

        for kod in kody_stacji:
            nazwa_stacji = opady_malopolska_iniekcja[opady_malopolska_iniekcja['Kod stacji'] == kod]['Nazwa'].iloc[0]
            station_names[kod] = nazwa_stacji

        all_results['Nazwa'] = all_results['Kod stacji'].map(station_names)
    return all_results


def save_spi_excel(df):
    # Assuming df is your DataFrame containing the data
    df = df.drop(columns=['Date'])
    if not os.path.exists("Results/SPI_results"):
        os.makedirs("Results/SPI_results")
    df.to_excel(os.path.join("Results/SPI_results", "SPI_wszystkie_stacje.xlsx"), index=False)


# Liczenie statystyk opisowych
def statistics_spi(spi_all_stations):
    grouped = spi_all_stations.groupby('Kod stacji')
    results = []
    # Wyświetlanie statystyk opisowych dla każdej grupy (stacji)
    for name, group in grouped:
        stats_df = group[['SPI-1', 'SPI-3', 'SPI-12']].agg(['min', 'max', 'mean', 'median'])
        stats_df = stats_df.T

        # Obliczanie interpretacji SPI-1
        interpretacja_spi1 = ""
        median_spi1 = stats_df.loc['SPI-1', 'median']
        if median_spi1 >= 2.0:
            interpretacja_spi1 = "ekstremalnie mokro"
        elif 1.5 <= median_spi1 < 2.0:
            interpretacja_spi1 = "bardzo mokro"
        elif 1.0 <= median_spi1 < 1.5:
            interpretacja_spi1 = "umiarkowanie mokro"
        elif -0.99 <= median_spi1 <= 0.99:
            interpretacja_spi1 = "średnie warunki"
        elif -1.49 <= median_spi1 < -1.0:
            interpretacja_spi1 = "umiarkowana susza"
        elif -1.99 <= median_spi1 < -1.5:
            interpretacja_spi1 = "silna susza"
        else:
            interpretacja_spi1 = "ekstremalna susza"
        # Dodanie interpretacji do ramki danych
        stats_df.at['SPI-1', 'interpretacja'] = interpretacja_spi1

        # Obliczanie interpretacji SPI-3
        interpretacja_spi3 = ""
        median_spi3 = stats_df.loc['SPI-3', 'median']
        if median_spi3 >= 2.0:
            interpretacja_spi3 = "ekstremalnie mokro"
        elif 1.5 <= median_spi3 < 2.0:
            interpretacja_spi3 = "bardzo mokro"
        elif 1.0 <= median_spi3 < 1.5:
            interpretacja_spi3 = "umiarkowanie mokro"
        elif -0.99 <= median_spi3 <= 0.99:
            interpretacja_spi3 = "średnie warunki"
        elif -1.49 <= median_spi3 < -1.0:
            interpretacja_spi3 = "umiarkowana susza"
        elif -1.99 <= median_spi3 < -1.5:
            interpretacja_spi3 = "silna susza"
        else:
            interpretacja_spi3 = "ekstremalna susza"
        # Dodanie interpretacji do ramki danych
        stats_df.at['SPI-3', 'interpretacja'] = interpretacja_spi3

        # Obliczanie interpretacji SPI-12
        interpretacja_spi12 = ""
        median_spi12 = stats_df.loc['SPI-12', 'median']
        if median_spi12 >= 2.0:
            interpretacja_spi12 = "ekstremalnie mokro"
        elif 1.5 <= median_spi12 < 2.0:
            interpretacja_spi12 = "bardzo mokro"
        elif 1.0 <= median_spi12 < 1.5:
            interpretacja_spi12 = "umiarkowanie mokro"
        elif -0.99 <= median_spi12 <= 0.99:
            interpretacja_spi12 = "średnie warunki"
        elif -1.49 <= median_spi12 < -1.0:
            interpretacja_spi12 = "umiarkowana susza"
        elif -1.99 <= median_spi12 < -1.5:
            interpretacja_spi12 = "silna susza"
        else:
            interpretacja_spi12 = "ekstremalna susza"
        # Dodanie interpretacji do ramki danych
        stats_df.at['SPI-12', 'interpretacja'] = interpretacja_spi12
        # Zaokrąglanie wszystkich wartości w ramce danych
        stats_df = stats_df.round(4)
        stats_df = stats_df.reset_index()
        # Dodanie wyników do listy
        results.append({'Kod stacji': name, 'Mediana SPI-12': median_spi12, 'Interpretacja': interpretacja_spi12})
        # results = pd.DataFrame(results)
        if not os.path.exists("Results/SPI_statistics"):
            os.makedirs("Results/SPI_statistics")
        stats_df.to_csv(os.path.join("Results/SPI_statistics", f'{name}_staystyki_opisowe.csv'), index=False)

    return pd.DataFrame(results)

