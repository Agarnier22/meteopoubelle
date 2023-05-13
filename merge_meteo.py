import pandas as pd
import numpy as np

name = 'Extraction_ZDS_2023_03_31.csv'

df = pd.read_csv(name, sep=',', dtype=str, index_col=0)
df = df[df.LIEU_VILLE.str.contains('Marseille').fillna(False)]
df['DATE'] = pd.to_datetime(df['DATE'])

cols = ['numer_sta', 'date', 'dd', 'ff', 't', 'ww', 'rr3', 'rr6', 'rr12', 'rr24']
data = pd.read_csv('../MerTerre/meteo_2017_2023_Marignane.csv')
meteo_data = pd.DataFrame(data, columns=cols)

meteo_data['hour'] = meteo_data.astype(str).date.str[8:]
meteo_data['DATE'] = pd.to_datetime(meteo_data.astype(str).date.str[:8])
meteo_data = meteo_data.replace('mq', pd.NA).dropna()
meteo_data['ff_X'] = meteo_data.ff.astype(float) * np.cos(meteo_data.dd.astype(float) * np.pi / 180)
meteo_data['ff_Y'] = meteo_data.ff.astype(float) * np.sin(meteo_data.dd.astype(float) * np.pi / 180)
meteo_data['ff_weekly'] = np.sqrt(
    meteo_data.ff_X.rolling(min_periods=1, window=8*7).sum()**2
    + meteo_data.ff_Y.rolling(min_periods=1, window=8*7).sum()**2
)
meteo_data['ff24'] = np.sqrt(
    meteo_data.ff_X.rolling(min_periods=1, window=8).sum()**2
    + meteo_data.ff_Y.rolling(min_periods=1, window=8).sum()**2
)
meteo_data = meteo_data[meteo_data.hour.astype(str) == '120000']
meteo_data.rr24 = meteo_data.rr24.astype(float)

meteo_data['rr_weekly'] = meteo_data.rr24.rolling(min_periods=1, window=7).sum()
meteo_data['rr_monthly'] = meteo_data.rr24.rolling(min_periods=1, window=28).sum()

df = pd.merge(df, meteo_data, how='left')
df.to_csv('Meteo_Extraction_ZDS_2023_03_31.csv')
meteo_data.to_csv('meteo_2017_2023_Marignane.csv')
