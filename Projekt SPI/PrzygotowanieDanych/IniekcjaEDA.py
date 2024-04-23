import pandas as pd
import numpy as np

def fill_missing_values(opady_malopolska_spi):
    # Zainicjuj pustą listę do przechowywania danych
    data_frames = []

    # Pętla dla każdego unikalnego ID w kolumnie Kod stacji
    for station_code in opady_malopolska_spi['Kod stacji'].unique():
        # Wybierz dane dla danego kodu stacji
        data_for_ID = opady_malopolska_spi[opady_malopolska_spi['Kod stacji'] == station_code]

        # Określ maksymalną i minimalną datę
        min_date = data_for_ID['Data'].min()
        max_date = data_for_ID['Data'].max()

        # Dodaj wszystkie brakujące daty dzienne
        full_dates = pd.date_range(start=min_date, end=max_date, freq='D')
        missing_dates = full_dates[~full_dates.isin(data_for_ID['Data'])]

        # Utwórz ramkę danych z brakującymi datami
        missing_data = pd.DataFrame(
            {'Data': missing_dates, 'Kod stacji': station_code, 'Suma dobowa opadów [mm]': np.nan})

        # Dołącz brakujące dane do oryginalnych danych
        data_for_ID = pd.concat([data_for_ID, missing_data])

        # Dodaj dodatkową datę na początku i na końcu
        data_for_ID = pd.concat([data_for_ID, pd.DataFrame({'Data': [min_date, max_date],
                                                            'Kod stacji': [station_code, station_code],
                                                            'Suma dobowa opadów [mm]': [np.nan, np.nan]})],
                                ignore_index=True)
        # ????????????????????????????????????????????/
        # # Dodaj dodatkową datę na początku i na końcu
        # data_for_ID = pd.concat([data_for_ID, pd.DataFrame({'Data': [min_date - pd.Timedelta(days=1), max_date + pd.Timedelta(days=1)],
        #                                                 'Kod stacji': [station_code, station_code],
        #                                                 'Suma dobowa opadów [mm]': [np.nan, np.nan]})], ignore_index=True)

        # Posortuj dane po dacie
        data_for_ID = data_for_ID.sort_values(by='Data').reset_index(drop=True)

        # Wypełnij brakujące wartości
        np.random.seed(69)  # Ustaw ziarno losowości dla powtarzalności
        filled_values = 3 * data_for_ID.groupby([data_for_ID['Data'].dt.year, data_for_ID['Data'].dt.day])[
            'Suma dobowa opadów [mm]'].transform('median')
        filled_values = filled_values.sample(n=len(data_for_ID), replace=True).reset_index(drop=True)
        data_for_ID['Suma dobowa opadów [mm]'].fillna(filled_values, inplace=True)

        # Dodaj DataFrame do listy
        data_frames.append(data_for_ID)

    # Połącz wszystkie ramki danych w jeden DataFrame
    opady_malopolska_iniekcja = pd.concat(data_frames)
    opady_malopolska_iniekcja = opady_malopolska_iniekcja.reset_index(drop=True)
    opady_malopolska_iniekcja['Data'] = pd.to_datetime(opady_malopolska_iniekcja['Data'])
    opady_malopolska_iniekcja['Rok'] = opady_malopolska_iniekcja['Data'].dt.year
    opady_malopolska_iniekcja['Miesiąc'] = opady_malopolska_iniekcja['Data'].dt.month
    return opady_malopolska_iniekcja