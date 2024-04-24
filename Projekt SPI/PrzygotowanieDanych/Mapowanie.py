import pandas as pd
# -------------------------------------------------------------- Michał -----------------------------------

def rain_malopolska(dane_opady, punkty_wewnatrz_malopolski):
    opady_malopolska = pd.merge(dane_opady, punkty_wewnatrz_malopolski, left_on='Kod stacji', right_on='Kod stacji',
                                how='inner')
    opady_malopolska = opady_malopolska.drop(columns=['Nazwa stacji'])
    opady_malopolska['Data'] = pd.to_datetime(
        opady_malopolska['Rok'].astype(str) + '-' + opady_malopolska['Miesiąc'].astype(str) + '-' + opady_malopolska[
            'Dzień'].astype(str), format='%Y-%m-%d')
    opady_malopolska = opady_malopolska.drop(columns=['Rok', 'Miesiąc', 'Dzień'])

    opady_malopolska = opady_malopolska[
        ['Kod stacji', 'Nazwa', 'Suma dobowa opadów [mm]', 'Data', 'Szerokość geograficzna', 'Długość geograficzna',
         'geometry', 'Rzeka'] + [col for col in opady_malopolska.columns if
                                 col not in ['Kod stacji', 'Nazwa', 'Suma dobowa opadów [mm]', 'Data',
                                             'Szerokość geograficzna', 'Długość geograficzna', 'geometry', 'Rzeka']]]
    return opady_malopolska
# --------------------------------------------------------------------------
