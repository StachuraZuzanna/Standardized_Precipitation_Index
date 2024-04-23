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
