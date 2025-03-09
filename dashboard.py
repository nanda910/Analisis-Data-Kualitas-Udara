import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load dataset
def load_data():
    data = pd.read_csv("PRSA_Data_Guanyuan_20130301-20170228.csv")  # Ganti dengan path dataset asli
    return data

data = load_data()

# Sidebar untuk filter
# Sidebar untuk filter
st.sidebar.header("Filter Data")
selected_year = st.sidebar.selectbox("Pilih Tahun", data["year"].unique())
selected_month = st.sidebar.selectbox("Pilih Bulan", data["month"].unique())

# Filter data berdasarkan input pengguna
filtered_data = data[(data["year"] == selected_year) & (data["month"] == selected_month)]

# Informasi tentang PM2.5 dan Polusi Udara
st.markdown("## Tentang Polusi Udara")
st.markdown("**PM2.5** adalah partikel udara berukuran kecil (diameter ≤2.5µm) yang dapat masuk ke paru-paru dan menyebabkan masalah kesehatan serius, seperti penyakit pernapasan dan kardiovaskular.")
st.markdown("**PM10** terdiri dari partikel yang sedikit lebih besar tetapi masih berbahaya jika terhirup dalam jumlah besar.")
st.markdown("Polusi udara dapat dipengaruhi oleh faktor seperti cuaca, musim, dan aktivitas manusia seperti transportasi dan industri.")

# Visualisasi 1: Tren PM2.5 selama setahun terakhir
st.subheader("Tren PM2.5 Selama Setahun Terakhir")
fig, ax = plt.subplots()
sns.lineplot(data=data[data["year"] == selected_year], x="month", y="PM2.5", estimator="mean", ci=None, ax=ax)
plt.xlabel("Bulan")
plt.ylabel("Rata-rata PM2.5 (µg/m³)")
st.pyplot(fig)

# Insight dan Kesimpulan Visualisasi 1
st.markdown("**Insight:** Dari visualisasi ini, kita dapat melihat bagaimana tren rata-rata PM2.5 berubah sepanjang tahun. Jika terdapat lonjakan tertentu, kemungkinan besar disebabkan oleh faktor lingkungan seperti musim, pola cuaca, atau aktivitas manusia.")
st.markdown("**Kesimpulan:** Tren PM2.5 bervariasi sepanjang tahun. Jika pola menunjukkan peningkatan signifikan di bulan tertentu, ini dapat menjadi indikasi polusi yang lebih tinggi akibat musim dingin atau peningkatan aktivitas industri dan transportasi.")

# Visualisasi 2: Korelasi antara Suhu dan PM2.5
st.subheader("Korelasi antara Suhu dan PM2.5")
fig, ax = plt.subplots()
sns.scatterplot(data=filtered_data, x="TEMP", y="PM2.5", hue="hour", palette="coolwarm", ax=ax)
plt.xlabel("Suhu (°C)")
plt.ylabel("Konsentrasi PM2.5 (µg/m³)")
st.pyplot(fig)

# Insight dan Kesimpulan Visualisasi 2
st.markdown("**Insight:** Scatter plot menunjukkan hubungan antara suhu dan konsentrasi PM2.5. Jika titik-titik cenderung membentuk pola tertentu, maka ada indikasi korelasi antara kedua variabel ini.")
st.markdown("**Kesimpulan:** Jika terdapat korelasi negatif yang jelas, berarti suhu yang lebih rendah cenderung meningkatkan konsentrasi PM2.5, yang bisa disebabkan oleh inversi suhu di musim dingin yang menjebak polutan di lapisan udara bawah.")

# Tambahkan deskripsi interaktif
st.sidebar.write("Gunakan filter di atas untuk mengeksplorasi data berdasarkan tahun dan bulan!")
