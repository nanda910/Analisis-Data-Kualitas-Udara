import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Biodata Pembuat
st.sidebar.title("Biodata Pembuat")
st.sidebar.write("**Nama:** Dewangga Megananda")
st.sidebar.write("**Kode:** MC-13")
st.sidebar.write("**ID:** mc009d5y0642")

def load_data():
    df = pd.read_csv("PRSA_Data_Guanyuan_20130301-20170228.csv")  # Ganti dengan path dataset
    df.dropna(inplace=True)
    
    # Menghapus outlier
    numerical_cols = ['PM2.5', 'TEMP']
    for col in numerical_cols:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df = df[(df[col] >= lower_bound) & (df[col] <= upper_bound)]
    
    df['datetime'] = pd.to_datetime(df[['year', 'month', 'day', 'hour']])
    df.set_index('datetime', inplace=True)
    df['month_year'] = df.index.to_period('M')
    return df

df = load_data()

st.title("Dashboard Kualitas Udara Guanyuan")

# Distribusi PM2.5
st.subheader("Distribusi PM2.5")
fig, ax = plt.subplots(figsize=(10, 5))
sns.histplot(df['PM2.5'], bins=30, kde=True, ax=ax)
ax.set_xlabel("Konsentrasi PM2.5")
ax.set_ylabel("Frekuensi")
st.pyplot(fig)

# Tren PM2.5
st.subheader("Tren Bulanan PM2.5")
fig, ax = plt.subplots(figsize=(12, 5))
df.groupby('month_year')['PM2.5'].mean().plot(ax=ax)
ax.set_title("Tren Bulanan PM2.5")
st.pyplot(fig)

# Statistik PM2.5
desc_trend = df.groupby('month_year')['PM2.5'].mean().describe()
st.write(f"Rata-rata PM2.5 bulanan: {desc_trend['mean']:.2f}")
st.write(f"Nilai maksimum bulanan: {desc_trend['max']:.2f}")
st.write(f"Nilai minimum bulanan: {desc_trend['min']:.2f}")

# Korelasi TEMP vs PM2.5
st.subheader("Korelasi Suhu dan PM2.5")
correlation = df[['TEMP', 'PM2.5']].corr().iloc[0,1]
st.write(f"Korelasi antara suhu (TEMP) dan PM2.5: {correlation:.2f}")
if correlation < 0:
    st.write("Terdapat korelasi negatif antara suhu dan PM2.5. Semakin tinggi suhu, semakin rendah polusi PM2.5.")
elif correlation > 0:
    st.write("Terdapat korelasi positif antara suhu dan PM2.5. Semakin tinggi suhu, semakin tinggi polusi PM2.5.")
else:
    st.write("Tidak ada korelasi yang signifikan antara suhu dan PM2.5.")

fig, ax = plt.subplots(figsize=(8,5))
sns.scatterplot(x=df['TEMP'], y=df['PM2.5'], alpha=0.5, ax=ax)
ax.set_xlabel('Temperature (°C)')
ax.set_ylabel('PM2.5')
ax.set_title('Scatter Plot TEMP vs PM2.5')
st.pyplot(fig)