"""
Description of the data
https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=90&id_rubrique=32
"""

import pandas as pd
import requests

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

year = 2018
for month in range(1, 13):
    month_url = meteo_url + f'synop.{year}{month:02}' + '.csv.gz'
    r = requests.get(month_url, allow_redirects=True)
    with open('tmp.csv.gz', 'wb') as file:
        file.write(r.content)
    met = pd.read_csv('tmp.csv.gz', sep=';')
    met = met.loc[met.numer_sta == 7650, cols]
    met.to_csv(f'meteo/meteo_{year}_{month}.csv')
