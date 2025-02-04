import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

autizhongxin_df = pd.read_csv("data/PRSA_Data_Aotizhongxin_20130301-20170228.csv")
changping_df = pd.read_csv("data/PRSA_Data_Changping_20130301-20170228.csv")
dingling_df = pd.read_csv("data/PRSA_Data_Dingling_20130301-20170228.csv")
dongsi_df = pd.read_csv("data/PRSA_Data_Dongsi_20130301-20170228.csv")
guanyuan_df = pd.read_csv("data/PRSA_Data_Guanyuan_20130301-20170228.csv")
gucheng_df = pd.read_csv("data/PRSA_Data_Gucheng_20130301-20170228.csv")
huairou_df = pd.read_csv("data/PRSA_Data_Huairou_20130301-20170228.csv")
nongzhanguan_df = pd.read_csv("data/PRSA_Data_Nongzhanguan_20130301-20170228.csv")
shunyi_df = pd.read_csv("data/PRSA_Data_Shunyi_20130301-20170228.csv")
tiantan_df = pd.read_csv("data/PRSA_Data_Tiantan_20130301-20170228.csv")
wanliu_df = pd.read_csv("data/PRSA_Data_Wanliu_20130301-20170228.csv")
wanshouxigong_df = pd.read_csv("data/PRSA_Data_Wanshouxigong_20130301-20170228.csv")

urls = {
    "Aotizhongxin": autizhongxin_df,
    "Changping": changping_df,
    "Dingling": dingling_df,
    "Dongsi": dongsi_df,
    "Guanyuan": guanyuan_df,
    "Gucheng": gucheng_df,
    "Huairou": huairou_df,
    "Nongzhanguan": nongzhanguan_df,
    "Shunyi": shunyi_df,
    "Tiantan": tiantan_df,
    "Wanliu": wanliu_df,
    "Wanshouxigong": wanshouxigong_df,
}

df = pd.concat(urls.values(), ignore_index=True)

# Judul Dashboard
st.title("Dashboard Kualitas Udara")

# Cleaning Data
df_clean = df.copy()
numeric_cols = df_clean.select_dtypes(include=[np.number]).columns
df_clean[numeric_cols] = df_clean[numeric_cols].apply(lambda x: x.fillna(x.mode()[0]))
df_clean["datetime"] = pd.to_datetime(df_clean[["year", "month", "day", "hour"]], errors="coerce")
df_clean = df_clean.drop(columns=["year", "month", "day", "hour"])
df_clean = df_clean[(df_clean["PM2.5"] < 999) & (df_clean["PM10"] < 999)]

# Sidebar untuk filter
st.sidebar.header("Filter Data")
start_date = st.sidebar.date_input("Mulai Tanggal", df_clean["datetime"].min().date())
end_date = st.sidebar.date_input("Akhir Tanggal", df_clean["datetime"].max().date())

# Terapkan filter pada dataframe yang sudah dibersihkan
filtered_df_clean = df_clean[
    (df_clean["datetime"] >= pd.Timestamp(start_date)) &
    (df_clean["datetime"] <= pd.Timestamp(end_date))
]

# Debugging: Cek jumlah data setelah difilter
print(f"Jumlah data setelah difilter: {len(filtered_df_clean)}")

# Visualisasi 1: Tren Kualitas Udara
city_avg = filtered_df_clean.groupby('station')[['PM2.5', 'PM10']].mean().reset_index()
city_avg_melted = city_avg.melt(id_vars='station', value_vars=['PM2.5', 'PM10'],
                                var_name='Polutan', value_name='Rata-Rata Konsentrasi')

st.subheader("Tren Kualitas Udara pada Setiap Distrik")
plt.figure(figsize=(12, 6))
sns.barplot(x='station', y='Rata-Rata Konsentrasi', hue='Polutan', data=city_avg_melted, palette='Set2')
plt.xlabel("Kota")
plt.ylabel("Rata-Rata Konsentrasi (µg/m³)")
plt.title("Perbandingan Kualitas Udara di 12 Kota (PM2.5 dan PM10)")
plt.xticks(rotation=45)
plt.legend(title="Polutan")
plt.tight_layout()
st.pyplot(plt)

# Visualisasi 2: Heatmap Korelasi
bins = [-0.01, 0, 1, 5, np.inf]
labels = ['Tanpa Hujan', 'Hujan Ringan', 'Hujan Sedang', 'Hujan Lebat']
df_clean['RAIN_category'] = pd.cut(df_clean['RAIN'], bins=bins, labels=labels)
agg_data = df_clean.groupby('RAIN_category', observed=True)[['PM2.5', 'PM10', 'TEMP', 'PRES', 'DEWP']].mean().reset_index()

st.subheader("Korelasi Intensitas Hujan dengan Sebaran Polutan Udara")
plt.figure(figsize=(10, 6))
sns.barplot(x='RAIN_category', y='PM2.5', data=agg_data, color='steelblue', label='PM2.5')
sns.barplot(x='RAIN_category', y='PM10', data=agg_data, color='indianred', alpha=0.7, label='PM10')
plt.xlabel("Kategori Intensitas Hujan")
plt.ylabel("Rata-Rata Konsentrasi (µg/m³)")
plt.title("Pengaruh Intensitas Hujan terhadap Konsentrasi PM2.5 dan PM10")
plt.legend()
plt.tight_layout()
st.pyplot(plt)

plt.figure(figsize=(12, 5))
plt.subplot(1, 2, 1)
sns.boxplot(data=df_clean, x='RAIN_category', y='PM2.5')
plt.xlabel("Kategori Curah Hujan")
plt.ylabel("PM2.5 (µg/m³)")
plt.title("Distribusi PM2.5 Berdasarkan Curah Hujan")
plt.subplot(1, 2, 2)
sns.boxplot(data=df_clean, x='RAIN_category', y='PM10')
plt.xlabel("Kategori Curah Hujan")
plt.ylabel("PM10 (µg/m³)")
plt.title("Distribusi PM10 Berdasarkan Curah Hujan")
plt.tight_layout()
st.pyplot(plt)