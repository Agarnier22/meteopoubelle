"""Gets past weather data from Meteo france.

Description of the data
https://donneespubliques.meteofrance.fr/?fond=produit&id_produit=90&id_rubrique=32
"""
from pathlib import Path

import numpy as np
import pandas as pd
import requests

cols = ['numer_sta', 'date', 'dd', 'ff', 't', 'ww', 'rr3', 'rr6', 'rr12', 'rr24']
meteo_url = 'https://donneespubliques.meteofrance.fr/donnees_libres/Txt/Synop/Archive/'
wind_directions = ['N', 'NE', 'ENE',
                   'E', 'ESE', 'SE',
                   'SSE', 'S', 'SSO',
                   'SO', 'OSO', 'O',
                   'ONO', 'NO', 'NNO']


def get_monthly_weather(year, month):
    month_url = meteo_url + f'synop.{year}{month:02}' + '.csv.gz'
    r = requests.get(month_url, allow_redirects=True)
    with open('tmp.csv.gz', 'wb') as file:
        file.write(r.content)
    met = pd.read_csv('tmp.csv.gz', sep=';')
    return met.loc[met.numer_sta == 7650, cols]


def get_weather_period(start, stop):
    weather_data = pd.DataFrame(columns=cols)
    stop_year = stop.year
    for year in range(start.year, stop_year + 1):
        stop_month = 13 if year < stop_year else stop.month
        for month in range(1, stop_month):
            monthly = get_monthly_weather(year, month)
            weather_data = pd.concat([weather_data, monthly])
    return weather_data


def process_weather(weather_data):
    weather_data['hour'] = weather_data.astype(str).date.str[8:]
    weather_data['DATE'] = pd.to_datetime(weather_data.astype(str).date.str[:8])
    weather_data = weather_data.replace('mq', pd.NA).dropna()
    weather_data['ff_X'] = weather_data.ff.astype(float) * np.cos(
        weather_data.dd.astype(float) * np.pi / 180)
    weather_data['ff_Y'] = weather_data.ff.astype(float) * np.sin(
        weather_data.dd.astype(float) * np.pi / 180)
    weather_data['ff_weekly'] = np.sqrt(
        weather_data.ff_X.rolling(min_periods=1, window=8 * 7).sum() ** 2
        + weather_data.ff_Y.rolling(min_periods=1, window=8 * 7).sum() ** 2
    )
    weather_data['ff24'] = np.sqrt(
        weather_data.ff_X.rolling(min_periods=1, window=8).sum() ** 2
        + weather_data.ff_Y.rolling(min_periods=1, window=8).sum() ** 2
    )
    weather_data['direction'] = pd.cut(weather_data['dd'], bins=15, labels=wind_directions)
    weather_data = weather_data[weather_data.hour.astype(str) == '120000']
    weather_data.rr24 = weather_data.rr24.astype(float)
    weather_data['rr_weekly'] = weather_data.rr24.rolling(min_periods=1, window=7).sum()
    weather_data['rr_monthly'] = weather_data.rr24.rolling(min_periods=1, window=28).sum()
    return weather_data


def merge_weather_data(df):
    df['DATE'] = pd.to_datetime(df['DATE'])
    path_to_weather = Path('data/weather/weather_2017_2023_Marignane.csv')
    if df.DATE.min().year >= 2017 and path_to_weather.exists():
        weather_data = pd.read_csv(path_to_weather)
    else:
        weather_data = get_weather_period(df.DATE.min(), df.DATE.max())
    weather_data = process_weather(weather_data)
    return pd.merge(df, weather_data, how='left')
