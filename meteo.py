import pandas as pd
import matplotlib.pyplot as plt
import requests
import os

name = 'Extraction_ZDS_2023_03_31.csv'

df = pd.read_csv(name, sep=',', dtype=str, index_col=0)
df = df[df.LIEU_CODE_POSTAL.str.startswith('13').fillna(False)]
df['DATE'] = pd.to_datetime(df['DATE'])
plt.scatter(df.LIEU_COORD_GPS_X.astype(float), df.LIEU_COORD_GPS_Y.astype(float))
plt.show()

cols = ['numer_sta', 'date', 'dd', 'ff', 't', 'ww', 'rr3', 'rr6', 'rr12', 'rr24']

meteo_url = 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/'
for year in range(2019, 2023):
    for month in range(1, 13):
        month_url = meteo_url + f'synop.{year}{month:02}' + '.csv.gz'
        r = requests.get(month_url, allow_redirects=True)
        with open('tmp.csv.gz', 'wb') as file:
            file.write(r.content)
        met = pd.read_csv('tmp.csv.gz', sep=';')
        met = met.loc[met.numer_sta == 7650, cols]
        met.to_csv(f'meteo/meteo_{year}_{month}.csv')

year = 2023
for month in range(1, 6):
    month_url = meteo_url + f'synop.{year}{month:02}' + '.csv.gz'
    r = requests.get(month_url, allow_redirects=True)
    with open('tmp.csv.gz', 'wb') as file:
        file.write(r.content)
    met = pd.read_csv('tmp.csv.gz', sep=';')
    met = met.loc[met.numer_sta == 7650, cols]
    met.to_csv(f'meteo/meteo_{year}_{month}.csv')

meteo_data = pd.DataFrame(columns=cols)
for path in os.listdir('meteo'):
    tmp_df = pd.read_csv(f'meteo/{path}').drop('Unnamed: 0', axis=1)
    meteo_data = pd.concat([meteo_data, tmp_df])

meteo_data['hour'] = meteo_data.astype(str).date.str[8:]
meteo_data['DATE'] = pd.to_datetime(meteo_data.astype(str).date.str[:8])
meteo_data = meteo_data.replace('mq', pd.NA).dropna()
meteo_data = meteo_data[meteo_data.hour.astype(str) == '120000']
meteo_data.rr24 = meteo_data.rr24.astype(float)

meteo_data['rr_weekly'] = meteo_data.rr24.rolling(min_periods=1, window=7).sum()
meteo_data['rr_monthly'] = meteo_data.rr24.rolling(min_periods=1, window=28).sum()

df = pd.merge(df, meteo_data, how='left')
df.to_csv('Meteo_Extraction_ZDS_2023_03_31.csv')
meteo_data.to_csv('meteo_2019_2023_Marignane.csv')
