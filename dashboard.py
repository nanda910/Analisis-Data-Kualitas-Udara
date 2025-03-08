import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from datetime import datetime

# --------------------------------------
# BIODATA PEMBUAT
# --------------------------------------
# Nama: Dewangga Megananda
# ID Dicoding: MC-13
# Kode: mc009d5y0642

# Streamlit UI
st.title("Dashboard Analisis Data PM2.5")
st.sidebar.header("Biodata Pembuat")
st.sidebar.text("Nama: Dewangga Megananda")
st.sidebar.text("ID Dicoding: MC-13")
st.sidebar.text("Kode: mc009d5y0642")

# 1. Gathering Data
df = pd.read_csv("PRSA_Data_Guanyuan_20130301-20170228.csv")

# Menampilkan informasi dasar tentang dataset
st.write("## Informasi Dataset")
st.write(df.info())
st.write(df.head())

# 2. Assesing Data
st.write("## Missing Values")
st.write(df.isnull().sum())

st.write("## Nilai Unik dalam Kolom")
for col in df.columns:
    st.write(f"{col} Unique Values: {df[col].unique()[:10]}")

duplicate_count = df.duplicated().sum()
st.write(f"Jumlah data duplikat: {duplicate_count}")

st.write("## Statistik Deskriptif")
st.write(df.describe())

pollutants = ['PM2.5', 'PM10', 'SO2', 'NO2', 'CO', 'O3']
for col in pollutants:
    invalid_values = df[df[col] < 0]
    if not invalid_values.empty:
        st.write(f"Data tidak valid ditemukan di {col}:")
        st.write(invalid_values.head())
    else:
        st.write(f"Tidak ada data tidak valid pada {col}.")

# 3. Cleaning Data
df.dropna(inplace=True)
df.drop_duplicates(inplace=True)

required_time_cols = {'year', 'month', 'day', 'hour'}
if required_time_cols.issubset(df.columns):
    df['year'] = df['year'].astype(int)
    df['month'] = df['month'].astype(int)
    df['day'] = df['day'].astype(int)
    df['hour'] = df['hour'].astype(int)
else:
    st.write("Kolom waktu tidak lengkap, konversi tipe data tidak dilakukan.")

# Handling Outliers
numerical_cols = df.select_dtypes(include=['number']).columns
for col in numerical_cols:
    Q1 = df[col].quantile(0.25)
    Q3 = df[col].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]

# --------------------------------------
# VISUALISASI DATA
# --------------------------------------

# Distribusi PM2.5
st.subheader("Distribusi PM2.5")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df['PM2.5'], bins=30, kde=True, ax=ax)
ax.set_xlabel("Konsentrasi PM2.5")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

# Tren PM2.5
st.subheader("Tren Bulanan PM2.5")
df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
df.set_index('datetime', inplace=True)
df['month_year'] = df.index.to_period('M')
fig, ax = plt.subplots(figsize=(12, 5))
df.groupby('month_year')['PM2.5'].mean().plot(ax=ax)
ax.set_title("Tren Bulanan PM2.5")
st.pyplot(fig)

# Korelasi TEMP vs PM2.5
st.subheader("Korelasi Suhu dan PM2.5")
correlation = df[['TEMP', 'PM2.5']].corr().iloc[0,1]
st.write(f"Korelasi antara suhu (TEMP) dan PM2.5: {correlation:.2f}")
fig, ax = plt.subplots(figsize=(8,5))
sns.scatterplot(x=df['TEMP'], y=df['PM2.5'], alpha=0.5, ax=ax)
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('PM2.5')
ax.set_title('Scatter Plot TEMP vs PM2.5')
st.pyplot(fig)

# --------------------------------------
# VISUALISASI PETA LOKASI STASIUN
# --------------------------------------

st.subheader("Peta Lokasi Stasiun Pemantauan")
map_center = [39.9334, 116.3406]  # Lokasi stasiun di Beijing
m = folium.Map(location=map_center, zoom_start=10)
folium.Marker(map_center, popup="Stasiun Guanyuan", tooltip="Stasiun Guanyuan").add_to(m)
folium_static(m)
