import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import pydeck as pdk
import matplotlib.pyplot as plt


'# ☀️ 🗑 Météopoubelle 🌊'
st.markdown('''
Découvrez les zones d'accumulation de déchets diffus à Marseille !  
Data source: [Mer-Terre](https://www.zero-dechet-sauvage.org/ressources)
''')


if 'params' not in st.session_state:
    st.session_state.df = pd.read_csv('coords_gps')

df = st.session_state.df

st.write('Selectionner un scénario')

wind = ["Mistral","Sirocco"]
season = ["Eté", "Hiver"]
rain = ["Pluie"]

wind_choice = st.sidebar.selectbox('', wind)
season_choice = st.sidebar.selectbox('', season)
rain_choice = st.sidebar.selectbox('', rain)

#st.map(df)
st.pydeck_chart(pdk.Deck(
    map_style=None,
    initial_view_state=pdk.ViewState(
        latitude=43.2,
        longitude=5.35,
        zoom=11
      #  pitch=50,
    ),
    layers=[
        pdk.Layer(
            'ScatterplotLayer',
            data=df,
            get_position='[lon, lat]',
            get_color='[200, 30, 0, 160]',
            get_radius=['POIDS_TOTAL'],
        ),
    ],
))


# Pie chart, where the slices will be ordered and plotted counter-clockwise:
#pie_chart = pd.read_csv('piechart')
#fig = px.pie(pie_chart, values='vals',  title='Population of European continent')
#st.pyplot(pie_chart)
