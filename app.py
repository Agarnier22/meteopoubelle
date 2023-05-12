import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

'# ☀️ 🗑 Meteopoubelle 🌊'
st.markdown('''
Découvrez les zones d'accumulation de déchets diffus à Marseille !  
Data source: [Mer-Terre](https://www.zero-dechet-sauvage.org/ressources)
''')

st.header('Explorez la zone')

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

st.map(df)

