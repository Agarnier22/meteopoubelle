import pandas as pd

from meteopoubelle.weather_scrapping import merge_weather_data

# Import des données brutes
name = 'data/Extraction_ZDS_2023_03_31.csv'
df = pd.read_csv(name, sep=',', dtype=str)
df['DATE'] = pd.to_datetime(df['DATE'])

# Filtre sur marseille
df = df[df.LIEU_VILLE.str.contains('Marseille').fillna(False)]

# Ajout de la saison du ramassage
seasons = {
             1: 'Hiver',
             2: 'Printemps',
             3: 'Eté',
             4: 'Automne'
}
df['season'] = ((df['DATE'].dt.month % 12 + 3) // 3).map(seasons)

# Merge données MERTERRE et méteo
df_weather = merge_weather_data(df)

# FILTRES des colonnes gardées
columns_to_keep = [
    'LIEU_VILLE', 'LIEU_CODE_POSTAL', 'LIEU_COORD_GPS_X',
    'LIEU_COORD_GPS_Y', 'NOM_ZONE', 'TYPE_LIEU_V2_1', 'TYPE_LIEU_V2_2',
    'TYPE_DECHET', 'SURFACE', 'DATE', 'VOLUME_TOTAL',
    'dd', 'ff24', 'ff_weekly', 't', 'ww', 'rr24', 'rr_weekly', 'rr_monthly',
    'NB_DECHET_SECTEUR_ALIMENTATION', 'NB_DECHET_SECTEUR_TABAC',
    'NB_DECHET_SECTEUR_PHARMACEUTIQUE/PARAMÉDICAL']

data_filter = df_weather[columns_to_keep]

# filtre pour retirer les ramassages fonds marins
data_type_filter = data_filter[data_filter.TYPE_DECHET != 'Fond']

# export du dataset final
data_type_filter.to_csv('data/dataset_meteo_filtre.csv')
