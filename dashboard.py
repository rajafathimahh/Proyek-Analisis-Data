import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

# Judul dashboard
st.title("Dashboard Penyewaan Sepeda")

# Sidebar untuk input user
st.sidebar.header('Input Parameter Pengguna')

@st.cache
def load_data():
    data = pd.read_csv('https://raw.githubusercontent.com/rajafathimahh/PROYEK-EVA/refs/heads/main/day.csv')  # Adjust the path as needed
    return data

data = load_data()

day_df = pd.DataFrame(data)
st.subheader('Dashboard ini menampilkan hasil visualisasi data yang menjawab dua pertanyaan bisnis:')
st.markdown("""
- 1. Bagaimana rata-rata jumlah penyewaan sepeda oleh pengguna casual dan pengguna registered selama 4 musim dalam dua tahun (2011-2012)?
- 2. Apakah faktor cuaca seperti temp, hum, dan windspeed mempengaruhi jumlah total penyewaan sepeda pada hari kerja (working days) dibandingkan dengan akhir pekan (weekends) selama periode 2011-2012?
""")

# Menunjukkan raw data jika di'select'
if st.sidebar.checkbox("Perlihatkan data mentah (raw)", False):
    st.subheader('Raw Dataset')
    st.write(data)


# Plot: LINE CHART 'Tren Rerata Penyewaan Sepeda Berdasarkan Musim selama 2011-2012'
seasonal_trend = day_df.groupby("season")[["casual", "registered"]].mean()
st.title("Tren Penyewaan Sepeda Berdasarkan Musim")
st.write("Visualisasi tren rerata penyewaan sepeda oleh pengguna 'Casual' dan 'Registered' dalam 2 tahun (2011-2012).")
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(seasonal_trend.index, seasonal_trend["casual"], marker="o", label="Casual Users", color="blue")
ax.plot(seasonal_trend.index, seasonal_trend["registered"], marker="o", label="Registered Users", color="red")
ax.set_title("Tren Rerata Penyewaan Sepeda oleh Pengguna 'Casual' dan 'Registered' Berdasarkan Musim")
ax.set_xlabel("Season (1=Spring, 2=Summer, 3=Fall, 4=Winter)")
ax.set_ylabel("Rata-rata Jumlah Pengguna")
ax.legend(title="Tipe Pengguna")
st.pyplot(fig) 

# Plot: BAR CHART 'Perbandingan Rerata Penggunaan Sepeda: Casual vs Registered Users di Setiap Musim'
x = np.arange(len(seasonal_trend))
width = 0.35
fig, ax = plt.subplots(figsize=(8, 5))
ax.bar(x - width/2, seasonal_trend["casual"], width, label="Casual Users", color="blue")
ax.bar(x + width/2, seasonal_trend["registered"], width, label="Registered Users", color="red")
ax.set_title("Perbandingan Rerata Penggunaan Sepeda: Casual vs Registered Users di Setiap Musim")
ax.set_xlabel("Season (1=Spring, 2=Summer, 3=Fall, 4=Winter)")
ax.set_xticks(x)
ax.set_xticklabels(seasonal_trend.index)
ax.set_ylabel("Rata-rata Jumlah Pengguna")
ax.legend(title="Tipe Pengguna")
st.pyplot(fig)

# Filter interaktif kondisi cuaca 'weather'
selected_weather = st.sidebar.selectbox('Pilih Kondisi Cuaca', data['weathersit'].unique())

st.subheader(f'Analisis Kondisi Cuaca: {selected_weather}')
filtered_data = data[data['weathersit'] == selected_weather]
st.write(filtered_data.describe())

# SCATTER PLOT
# Plot Suhu vs Total Pengguna
st.subheader('Pengaruh Suhu terhadap Total Pengguna')
fig, ax = plt.subplots()
sns.scatterplot(data=data, x='temp', y='cnt', ax=ax)
sns.regplot(x='temp', y='cnt', data=day_df, line_kws={'color': 'red'}, ax=ax)
ax.set_title('Suhu vs Jumlah Penyewa Sepeda')
st.pyplot(fig)

# Plot Kelembapan vs Total Pengguna
st.subheader('Pengaruh Kelembapan terhadap Total Pengguna')
fig, ax = plt.subplots()
sns.scatterplot(data=data, x='hum', y='cnt', ax=ax)
sns.regplot(x='hum', y='cnt', data=day_df, line_kws={'color': 'red'}, ax=ax)
ax.set_title('Kelembapan vs Jumlah Penyewa Sepeda')
st.pyplot(fig)

# Plot Kecepatan Angin vs Total Pengguna
st.subheader('Pengaruh Kecepatan Angin terhadap Total Pengguna')
fig, ax = plt.subplots()
sns.scatterplot(data=data, x='windspeed', y='cnt', ax=ax)
sns.regplot(x='windspeed', y='cnt', data=day_df, line_kws={'color': 'red'}, ax=ax)
ax.set_title('Kecepatan Angin vs Jumlah Penyewa Sepeda')
st.pyplot(fig)



# Conclusion
st.subheader('Kesimpulan')
st.markdown("""
- Pada musim semi (1), rata-rata pengguna 'casual' hanya sebesar 335, sedangkan pengguna 'registered' sebesar 2269 pengguna. Pada musim panas (2), rata-rata pengguna 'casual' sebesar 1106, sedangkan pengguna 'registered' sebesar 3886 pengguna. Pada musim gugur (3), rata-rata pengguna 'casual' sebesar 1203, sedangkan pengguna 'registered' sebesar 4442 pengguna. Terakhir, pada musim dingin (4), rata-rata pengguna 'casual' sebesar 729, sedangkan pengguna 'registered' sebesar 3999 pengguna.
- Musim yang memiliki rata-rata pengguna tertinggi baik 'casual' maupun 'registered' adalah musim gugur.

- Pada saat akhir pekan (0), dengan suhu rata-rata 0.48, kelembapan rata-rata 0.62, dan kecepatan angin rata-rata 0.19, jumlah pengguna/penyewa sepeda total mencapai rata-rata sebesar 4330 pengguna.
- Pada saat hari kerja (1), dengan suhu rata-rata 0.50, kelembapan rata-rata 0.63, dan kecepatan angin rata-rata 0.19, jumlah pengguna/penyewa sepeda total mencapai rata-rata sebesar 1878 pengguna.
- Nilai rata-rata faktor cuaca seperti suhu, kelembapan, dan kecepatan angin tidak memiliki perbedaan yang cukup signifikan pada saat akhir pekan maupun hari kerja, sehingga tidak terlalu memengaruhi jumlah pengguna/penyewa sepeda secara total. 
- Jumlah pengguna pada akhir pekan (4330) jauh lebih tinggi dibandingkan dengan hari kerja (1878). Meskipun faktor cuaca tidak menunjukkan perbedaan yang signifikan, hasil ini menunjukkan bahwa ada faktor lain yang mendorong lebih banyak orang untuk menggunakan sepeda pada akhir pekan. 
""")
