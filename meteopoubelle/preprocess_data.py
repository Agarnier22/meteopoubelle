import pandas as pd

from meteopoubelle.weather_scrapping import merge_weather_data

# FILTRES des colonnes gardées
columns_to_keep = [
    'LIEU_VILLE', 'LIEU_CODE_POSTAL', 'lon',
    'lat', 'NOM_ZONE', 'TYPE_LIEU_V2_1', 'TYPE_LIEU_V2_2',
    'TYPE_DECHET', 'SURFACE', 'DATE', 'season', 'VOLUME_TOTAL',
    'dd', 'ff24', 'ff_weekly', 't', 'ww', 'rr24', 'rr_weekly', 'rr_monthly', 'direction',
    'NB_DECHET_SECTEUR_ALIMENTATION',
    'NB_DECHET_SECTEUR_TABAC',
    'NB_DECHET_SECTEUR_PHARMACEUTIQUE/PARAMÉDICAL']

seasons = {1: 'Hiver', 2: 'Printemps', 3: 'Eté', 4: 'Automne'}


def extract_data():
    # Import des données brutes
    input_data = 'data/Extraction_ZDS_2023_03_31.csv'
    df = pd.read_csv(input_data, sep=',', dtype=str).rename(
        columns={'LIEU_COORD_GPS_Y': 'lat', 'LIEU_COORD_GPS_X': 'lon'})
    df['DATE'] = pd.to_datetime(df['DATE'])
    df['NB_DECHET_SECTEUR_TABAC'] = pd.to_numeric(df['NB_DECHET_SECTEUR_TABAC'])
    df['NB_DECHET_SECTEUR_ALIMENTATION'] = pd.to_numeric(df['NB_DECHET_SECTEUR_ALIMENTATION'])
    df['SURFACE'] = pd.to_numeric(df['SURFACE'])
    df['VOLUME_TOTAL'] = pd.to_numeric(df['VOLUME_TOTAL'])
    df['lat'] = pd.to_numeric(df['lat'])
    df['lon'] = pd.to_numeric(df['lon'])

    # Filtre sur marseille
    df = df[df.LIEU_VILLE.str.contains('Marseille').fillna(False)]

    # Ajout de la saison du ramassage
    df['season'] = ((df['DATE'].dt.month % 12 + 3) // 3).map(seasons)

    # Merge données MERTERRE et méteo
    df_weather = merge_weather_data(df)
    data_filter = df_weather[columns_to_keep]

    # filtre pour retirer les ramassages fonds marins
    data_type_filter = data_filter[data_filter.TYPE_DECHET != 'Fond']
    return data_type_filter
