import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os

# Set gaya seaborn
sns.set(style='dark')

# Menyiapkan helper function
def create_monthly_trend_df(df):
    monthly_trend_df = df.groupby(['year', 'month'])['PM2.5'].mean().reset_index()
    monthly_trend_df['waktu'] = pd.to_datetime(monthly_trend_df[['year', 'month']].assign(DAY=1))
    return monthly_trend_df

def create_station_df(df):
    stasiun_df = df.groupby('station')['PM2.5'].mean().sort_values(ascending=False).reset_index()
    return stasiun_df

# Load data
@st.cache_data
def load_data():
    base_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(base_dir, "main_data.csv")
    try:
        data = pd.read_csv(csv_path)
    except FileNotFoundError:
        data = pd.read_csv("main_data.csv")
    
    data['datetime'] = pd.to_datetime(data[['year', 'month', 'day', 'hour']])
    return data

try:
    df = load_data()
except Exception as e:
    st.error(f"Gagal memuat data! Error: {e}")
    st.stop()

# Konfigurasi Sidebar
min_date = df["datetime"].min().date()
max_date = df["datetime"].max().date()

with st.sidebar:
    st.title('🌤️ Filter Data')
    
    # Filter 1: Input Tanggal
    start_date, end_date = st.date_input(
        label='Rentang Waktu',
        value=[min_date, max_date],
        min_value=min_date,
        max_value=max_date
    )
    
    # Filter 2: Dropdown Pilihan Stasiun (Kota)
    stasiun_list = ["Semua Stasiun"] + list(df['station'].unique())
    selected_station = st.selectbox("Pilih Stasiun Pengamatan:", stasiun_list)

st.sidebar.markdown("---")
st.sidebar.markdown("Dashboard Analisis Data Air Quality Dataset - Steven Wijaya Lim")

# Eksekusi Filter
main_df = df[(df["datetime"].dt.date >= start_date) & (df["datetime"].dt.date <= end_date)]
if selected_station != "Semua Stasiun":
    main_df = main_df[main_df["station"] == selected_station]


# Header Dashboard Utama
st.title('🌤️ Air Quality Dashboard (Beijing)')
st.markdown("""
Dashboard interaktif ini menyediakan rangkuman eksplorasi data kualitas udara dari berbagai stasiun metereologi.
""")

# Menampilkan 6 Metrik Polutan Khusus Rata-Rata per Waktu/Stasiun
st.subheader(f"Statistik Rata-Rata Polutan: {selected_station}")
st.markdown(f"*(Data Kalkulasi berdasar Filter Tanggal: {start_date} hingga {end_date})*")

# Membuat 3 Kolom sejajar untuk visualisasi metrik (KPI)
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Partikel PM2.5 (µg/m³)", value=round(main_df['PM2.5'].mean(), 1))
    st.metric("Ozon O3 (µg/m³)", value=round(main_df['O3'].mean(), 1))

with col2:
    st.metric("Partikel PM10 (µg/m³)", value=round(main_df['PM10'].mean(), 1))
    st.metric("Sulfur Dioksida SO2", value=round(main_df['SO2'].mean(), 1))

with col3:
    st.metric("Karbon Monoksida CO", value=round(main_df['CO'].mean(), 1))
    st.metric("Nitrogen Dioksida NO2", value=round(main_df['NO2'].mean(), 1))

st.markdown("---")

# Visualisasi 1: Tren Polusi Bulanan
st.subheader("Tren Fluktuasi Polusi PM2.5")

monthly_trend_df = create_monthly_trend_df(main_df)
fig, ax = plt.subplots(figsize=(14, 5))
sns.lineplot(
    data=monthly_trend_df, 
    x='waktu', 
    y='PM2.5', 
    marker='o', 
    color='#e74c3c', 
    linewidth=2,
    ax=ax
)

ax.set_title(f"Tren PM2.5 per Bulan - {selected_station}", fontsize=16, pad=15)
ax.set_xlabel("Waktu", fontsize=12)
ax.set_ylabel("Konsentrasi PM2.5", fontsize=12)
ax.grid(axis='y', linestyle='--', alpha=0.7)

st.pyplot(fig)

with st.expander("Lihat Penjelasan (Tren Bulanan)"):
    st.write("Dapat terlihat jelas letak lonjakan partikel PM2.5 seiring transisi pertukaran bulan. Membuktikan pola perubahan iklim dan alam sekitar secara drastis berdampak pada menumpuknya angka polutan.")

st.markdown("---")

# Visualisasi 2: Stasiun Polutan Tertinggi dan Terendah (Hanya relevan jika 'Semua Stasiun' terpilih)
if selected_station == "Semua Stasiun":
    st.subheader("Perbandingan Tingkat Polusi (PM2.5) Antar Stasiun")
    
    stasiun_df = create_station_df(main_df)
    fig, ax = plt.subplots(figsize=(12, 6))
    
    # Highlight pewarnaan
    station_terburuk = stasiun_df['station'].iloc[0]
    station_terbaik = stasiun_df['station'].iloc[-1]
    warna = ['#e74c3c' if s == station_terburuk else '#2ecc71' if s == station_terbaik else '#bdc3c7' for s in stasiun_df['station']]
    
    sns.barplot(
        data=stasiun_df, 
        x='PM2.5', 
        y='station', 
        hue='station',
        palette=warna, 
        legend=False,
        ax=ax
    )
    
    ax.set_title("Rata-Rata Konsentrasi PM2.5 per Stasiun Pengukuran", fontsize=16, pad=15)
    ax.set_xlabel("Rata-rata Konsentrasi PM2.5", fontsize=12)
    ax.set_ylabel(None) 
    
    st.pyplot(fig)
else:
    st.info(f"Grafik komparasi stasiun disembunyikan karena Anda sedang memfokuskan data hanya pada stasiun **{selected_station}**.")

st.caption("Copyright © 2026 - Analisis Data Capstone")
