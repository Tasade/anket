import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# ===============================
# 1. VERİYİ YÜKLEME
# ===============================



st.title("📊 Veri Analizi")

uploaded_file = st.file_uploader("CSV dosyanı yükle", type="csv")

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file, low_memory=False)

    st.write("Veri başarıyla yüklendi!")
    st.dataframe(df.head())

else:
    st.warning("Lütfen bir CSV dosyası yükleyin.")

# ===============================
# 2. VERİ TEMİZLEME
# ===============================

# Maaş sütununu seç (USD bazlı ConvertedSalary daha temiz)
df = df[['Employment', 'DevType', 'Country', 'ConvertedSalary']]

# Eksik maaşları sil
df = df.dropna(subset=['ConvertedSalary'])

# Aykırı değer temizliği (uç maaşları kırp)
q_low = df['ConvertedSalary'].quantile(0.01)
q_high = df['ConvertedSalary'].quantile(0.99)

df = df[(df['ConvertedSalary'] >= q_low) &
        (df['ConvertedSalary'] <= q_high)]

# DevType çoklu değer içeriyor → satırlara böl
df['DevType'] = df['DevType'].str.split(';')
df_exploded = df.explode('DevType')

# En çok veri olan ilk 10 departmanı seç
top_devtypes = df_exploded['DevType'].value_counts().head(10).index
df_exploded = df_exploded[df_exploded['DevType'].isin(top_devtypes)]

print("Temizlenmiş veri boyutu:", df_exploded.shape)

# ===============================
# 3. ÇALIŞMA DURUMU vs MAAŞ
# ===============================

employment_salary = (
    df.groupby('Employment')['ConvertedSalary']
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(10, 6))
sns.barplot(x=employment_salary.values,
            y=employment_salary.index)

plt.title("Çalışma Durumuna Göre Ortalama Maaş")
plt.xlabel("Ortalama Maaş (USD)")
plt.ylabel("Çalışma Durumu")
plt.tight_layout()
plt.show()

# ===============================
# 4. DEPARTMAN vs MAAŞ
# ===============================

dev_salary = (
    df_exploded.groupby('DevType')['ConvertedSalary']
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 7))
sns.barplot(x=dev_salary.values,
            y=dev_salary.index)

plt.title("Departmana Göre Ortalama Maaş")
plt.xlabel("Ortalama Maaş (USD)")
plt.ylabel("Departman")
plt.tight_layout()
plt.show()

# ===============================
# 5. KUTU GRAFİĞİ (Dağılım Analizi)
# ===============================

plt.figure(figsize=(14, 8))
sns.boxplot(data=df_exploded,
            x='ConvertedSalary',
            y='DevType')

plt.title("Departmanlara Göre Maaş Dağılımı")
plt.xlabel("Maaş (USD)")
plt.ylabel("Departman")
plt.xlim(0, df_exploded['ConvertedSalary'].quantile(0.95))
plt.tight_layout()
plt.show()

# ===============================
# 6. ÜLKE vs MAAŞ (İlk 10 ülke)
# ===============================

top_countries = df['Country'].value_counts().head(10).index
country_df = df[df['Country'].isin(top_countries)]

country_salary = (
    country_df.groupby('Country')['ConvertedSalary']
    .mean()
    .sort_values(ascending=False)
)

plt.figure(figsize=(12, 7))
sns.barplot(x=country_salary.values,
            y=country_salary.index)

plt.title("Ülkelere Göre Ortalama Maaş")
plt.xlabel("Ortalama Maaş (USD)")
plt.ylabel("Ülke")
plt.tight_layout()
plt.show()

# ===============================
# 7. KORELASYON ANALİZİ
# ===============================

df_numeric = df[['ConvertedSalary']].copy()
correlation = df_numeric.corr()

print("\nKorelasyon Matrisi:")
print(correlation)

# ===============================
# 8. ÖZET İSTATİSTİKLER
# ===============================

print("\nGenel Maaş İstatistikleri:")
print(df['ConvertedSalary'].describe())
