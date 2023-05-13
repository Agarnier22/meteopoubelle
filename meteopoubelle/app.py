import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pydeck as pdk

import zoom as z

st.set_page_config(layout="wide")

'# ☀️ MétéoPoubelle 🌊🗑'
st.markdown('''
Découvrez les zones d'accumulation de déchets diffus à Marseille !
Data source: [Mer-Terre](https://www.zero-dechet-sauvage.org/ressources)
''')

# st.header('Explorez la zone')

df = pd.read_csv('dataset_meteo_filtre.csv').rename(columns={'LIEU_COORD_GPS_Y': 'lat', 'LIEU_COORD_GPS_X': 'lon'})

st.write('Selectionner un scénario')

rain = ["Pas de filtre", "Pluie"]
wind_type = ["Pas de filtre", "Mistral", "Sirocco"]
meteo = ["Aucun", "Mistral","Sirocco", "Pluie"]
season = ["Annuel", "Estival", "Hivernal"]
arrondissement = [
   "13001", "13002", "13003", "13004", "13005", "13005", "13006", "13007", "13008", "13009", "13010", "13011", "13012", "13013", "13014", "13015", "13016"
]

rain_choice = st.sidebar.selectbox(':rain_cloud: Pluie', rain)
wind_type_choice = st.sidebar.selectbox(':leaves: Vent', wind_type)
season_choice = st.sidebar.radio(':sunny: Saisonalité', season)
city_part_choice = st.sidebar.multiselect('Arrondissements :', arrondissement)

if wind_type_choice == "Pas de filtre":
    st.wind_strength_choice = "Pas de filtre"

if len(city_part_choice) > 0:
    df = df[df['LIEU_CODE_POSTAL'].isin(map(float, city_part_choice))]

if season_choice == "Estival":
    df = df[df['saison'].isin(["Eté", "Printemps"])]
elif season_choice == "Hivernal":
    df = df[df['saison'].isin(["Hiver", "Automne"])]

if rain_choice == "Pluie":
    df = df[df['rr_monthly'] >= 80]

if wind_type_choice == "Mistral":
    df = df[df['wind_flow'].isin(['NNO', 'O', 'NO', 'ONO', 'N', 'OON'])]
elif wind_type_choice == "Sirocco":
    df = df[df['wind_flow'].isin(['SSE', 'SE', 'E', 'S', 'ESE', 'EES'])]

data_count = len(df.index)
color = "green"

city_parts_number = len(city_part_choice)
if (city_parts_number == 0):
    city_parts_number = 16

if (data_count < city_parts_number * 30):
    color = "red"

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(f':{color}[Nombre de ramassages]', data_count)

with col2:
    if data_count == 0:
        tabac_count = 0
    else:
        tabac_count = round(df['NB_DECHET_SECTEUR_TABAC'].sum()/data_count)
    st.metric("Déchets tabac par ramassage", tabac_count)

with col3:
    if data_count == 0:
        alimentaire_count = 0
    else:
        alimentaire_count = round(df['NB_DECHET_SECTEUR_ALIMENTATION'].sum()/data_count)
    st.metric("Déchets alimentaires par ramassage", alimentaire_count)

df = df.fillna(0)
df = df[df['SURFACE'].astype(float) >= 100]
# df = df[df['Unnamed: 0'] != 252]
df['VOLUME_SURFACIQUE'] = df['VOLUME_TOTAL'].astype(float)/df['SURFACE'].astype(float)*100

df["lon"] = df["lon"].round(2)
df["lat"] = df["lat"].round(2)
df_grouped = df.groupby(['LIEU_CODE_POSTAL','lat','lon']).sum(numeric_only=True).reset_index()

min_lat = df['lat'].min()
max_lat = df['lat'].max()
min_lon = df['lon'].min()
max_lon = df['lon'].max()
center_lat = (max_lat + min_lat) / 2.0
center_lon = (max_lon + min_lon) / 2.0
range_lon = abs(max_lon - min_lon)
range_lat = abs(max_lat - min_lat)

if range_lon > range_lat:
    longitude_distance = range_lon
else:
    longitude_distance = range_lat

zoom = z.get_zoom_level(longitude_distance)

st.pydeck_chart(pdk.Deck(
   map_style=None,
   initial_view_state=pdk.ViewState(
       latitude=center_lat,
       longitude=center_lon,
       zoom=zoom
   ),
   layers=[
       pdk.Layer(
           'ScatterplotLayer',
           data=df_grouped,
           get_position='[lon, lat]',
           get_color='[200, 30, 0, 160]',
           get_radius=['VOLUME_SURFACIQUE'],
       ),
   ],
))

# ### Pre process
# df = df[df['LIEU_CODE_POSTAL'] == 13009]
# df["lon"] = df["lon"].round(2)
# df["lat"] = df["lat"].round(2)
# df_grouped = df.groupby([
#    'lat','lon','LIEU_CODE_POSTAL']).sum(numeric_only=True).reset_index()

### Aggregate
df.set_index(['TYPE_LIEU_V2_1'])
print(df.columns)
df_grouped_sized = df[[
   "TYPE_LIEU_V2_1","NB_DECHET_SECTEUR_TABAC",
   "NB_DECHET_SECTEUR_PHARMACEUTIQUE/PARAMÉDICAL","NB_DECHET_SECTEUR_ALIMENTATION"
]].groupby(["TYPE_LIEU_V2_1"]).size()

df_grouped= df[[
   "TYPE_LIEU_V2_1","NB_DECHET_SECTEUR_TABAC",
   "NB_DECHET_SECTEUR_PHARMACEUTIQUE/PARAMÉDICAL","NB_DECHET_SECTEUR_ALIMENTATION"
]].groupby(["TYPE_LIEU_V2_1"]).sum().rename(columns={
   "NB_DECHET_SECTEUR_TABAC" : "Tabac",
   "NB_DECHET_SECTEUR_PHARMACEUTIQUE/PARAMÉDICAL":"Pharmaceutique",
   "NB_DECHET_SECTEUR_ALIMENTATION": "Alimentataire"})

### Plot
fig = plt.figure()
ax = plt.subplot()
df_grouped=df_grouped.reset_index()
df_grouped.plot(kind='barh', stacked=True, x="TYPE_LIEU_V2_1", y=[
   "Tabac","Pharmaceutique","Alimentataire"], ax=ax, cmap="Set3", ylabel="")
ax.spines['top'].set_visible(False)
ax.spines['right'].set_visible(False)
ax.spines['left'].set_visible(False)
ax.spines['bottom'].set_color('#DDDDDD')
ax.tick_params(bottom=False, left=False)
ax.xaxis.grid(False)

plt.xticks(rotation=30)
ax.bar_label(ax.containers[0], df_grouped_sized, label_type="edge")
plt.legend(loc='best')
plt.title("Nombre de déchets par secteur économique")


st.pyplot(fig)






