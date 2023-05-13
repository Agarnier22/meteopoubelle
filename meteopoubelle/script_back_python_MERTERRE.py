#Import librairies Python
import datetime as dt
import math

import numpy as np
import pandas as pd

#Import des données brutes
name = 'Extraction_ZDS_2023_03_31.csv'

#Filtre sur marseille
df = pd.read_csv(name, sep=',', dtype=str)
df = df[df.LIEU_VILLE.str.contains('Marseille').fillna(False)]
df['DATE'] = pd.to_datetime(df['DATE'])

#Formattage données météo
cols = ['numer_sta', 'date', 'dd', 'ff', 't', 'ww', 'rr3', 'rr6', 'rr12', 'rr24']
data = pd.read_csv('./meteo_2017_2023_Marignane.csv')
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

#Merge données MERTERRE et méteo
df_meteo_brut = pd.merge(df, meteo_data, how='left')

#FILTRES des colonnes gardées et sur MARSEILLE.
data_filter = df_meteo_brut[['LIEU_VILLE','LIEU_CODE_POSTAL','LIEU_COORD_GPS_X',
         'LIEU_COORD_GPS_Y','NOM_ZONE','TYPE_LIEU_V2_1','TYPE_LIEU_V2_2',
         'TYPE_DECHET','SURFACE','DATE','VOLUME_TOTAL',
         'dd','ff24', 'ff_weekly','t','ww','rr24','rr_weekly','rr_monthly',
         'NB_DECHET_SECTEUR_ALIMENTATION','NB_DECHET_SECTEUR_TABAC','NB_DECHET_SECTEUR_PHARMACEUTIQUE/PARAMÉDICAL']]

data_seille = data_filter[data_filter['LIEU_VILLE']=="Marseille"]

#filtre pour retirer les ramassages fonds marins
data_type_filter = data_seille[data_seille.TYPE_DECHET != 'Fond']

#catégorisation du vent
data_type_filter['wind_flow'] = pd.cut(data_type_filter['dd'],
                      bins=15,
                      labels=['N','NE','ENE','E','ESE','SE','SSE','S','SSO','SO','OSO','O','ONO','NO','NNO'])

#formattage de la DATE en datetime
data_type_filter['DATE'] = pd.to_datetime(data_type_filter['DATE'],format="%Y-%m-%d")

#Categorisation des 4 saisons
data_type_filter['season'] = (data_type_filter['DATE'].dt.month%12 + 3)//3

seasons = {
             1: 'Hiver',
             2: 'Printemps',
             3: 'Eté',
             4: 'Automne'
}
data_type_filter['saison'] = data_type_filter['season'].map(seasons)
del data_type_filter['season']

#export du dataset final
data_type_filter.to_csv('dataset_meteo_filtre.csv')