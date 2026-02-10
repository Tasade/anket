import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

st.title("🔥 YENİ VERSİYON ÇALIŞIYOR 🔥")


st.title("📊 Veri Analizi Dashboard")

uploaded_file = st.file_uploader("CSV dosyanı yükle", type="csv")

# ===============================
# CSV YÜKLENDİYSE HER ŞEY BURADA ÇALIŞIR
# ===============================

if uploaded_file is not None:

    # 1. VERİYİ YÜKLEME
    df = pd.read_csv(uploaded_file, low_memory=False)

    st.success("Veri başarıyla yüklendi!")
    st.dataframe(df.head())

    # ===============================
    # 2. VERİ TEMİZLEME
    # ===============================

    df = df[['Employment', 'DevType', 'Country', 'ConvertedSalary']]
    df = df.dropna(subset=['ConvertedSalary'])

    q_low = df['ConvertedSalary'].quantile(0.01)
    q_high = df['ConvertedSalary'].quantile(0.99)

    df = df[(df['ConvertedSalary'] >= q_low) &
            (df['ConvertedSalary'] <= q_high)]

    df['DevType'] = df['DevType'].str.split(';')
    df_exploded = df.explode('DevType')

    top_devtypes = df_exploded['DevType'].value_counts().head(10).index
    df_exploded = df_exploded[df_exploded['DevType'].isin(top_devtypes)]

    st.write("Temizlenmiş veri boyutu:", df_exploded.shape)

    # ===============================
    # 3. ÇALIŞMA DURUMU vs MAAŞ
    # ===============================

    employment_salary = (
        df.groupby('Employment')['ConvertedSalary']
        .mean()
        .sort_values(ascending=False)
    )

    fig1, ax1 = plt.subplots(figsize=(10, 6))
    sns.barplot(x=employment_salary.values,
                y=employment_salary.index,
                ax=ax1)

    ax1.set_title("Çalışma Durumuna Göre Ortalama Maaş")
    st.pyplot(fig1)

    # ===============================
    # 4. DEPARTMAN vs MAAŞ
    # ===============================

    dev_salary = (
        df_exploded.groupby('DevType')['ConvertedSalary']
        .mean()
        .sort_values(ascending=False)
    )

    fig2, ax2 = plt.subplots(figsize=(12, 7))
    sns.barplot(x=dev_salary.values,
                y=dev_salary.index,
                ax=ax2)

    ax2.set_title("Departmana Göre Ortalama Maaş")
    st.pyplot(fig2)

    # ===============================
    # 5. KUTU GRAFİĞİ
    # ===============================

    fig3, ax3 = plt.subplots(figsize=(14, 8))
    sns.boxplot(data=df_exploded,
                x='ConvertedSalary',
                y='DevType',
                ax=ax3)

    ax3.set_xlim(0, df_exploded['ConvertedSalary'].quantile(0.95))
    ax3.set_title("Departmanlara Göre Maaş Dağılımı")

    st.pyplot(fig3)

    # ===============================
    # 6. ÜLKE vs MAAŞ
    # ===============================

    top_countries = df['Country'].value_counts().head(10).index
    country_df = df[df['Country'].isin(top_countries)]

    country_salary = (
        country_df.groupby('Country')['ConvertedSalary']
        .mean()
        .sort_values(ascending=False)
    )

    fig4, ax4 = plt.subplots(figsize=(12, 7))
    sns.barplot(x=country_salary.values,
                y=country_salary.index,
                ax=ax4)

    ax4.set_title("Ülkelere Göre Ortalama Maaş")

    st.pyplot(fig4)

    # ===============================
    # 7. ÖZET İSTATİSTİKLER
    # ===============================

    st.subheader("📈 Maaş İstatistikleri")
    st.write(df['ConvertedSalary'].describe())

else:
    st.info("Lütfen bir CSV dosyası yükleyin.")

# ===============================
# 9. ANALİTİK ÇIKARIMLAR
# ===============================

st.subheader("🧠 Analitik Çıkarımlar")

# En yüksek maaşlı departmanı bul
top_department = dev_salary.idxmax()
top_salary = dev_salary.max()

insight_text = f"""
📌 **Veri analizine göre en yüksek ortalama maaşa sahip departman:**  
**{top_department}** (${top_salary:,.0f})

Bu sonuç, günümüz teknoloji ekosisteminde **kodlama ve programlama becerilerinin**
stratejik önemini açıkça göstermektedir.

Özellikle yazılım geliştirme ve yapay zeka alanları:

• Yüksek ekonomik değer üretmektedir  
• Küresel iş gücü piyasasında güçlü talep görmektedir  
• Veri odaklı karar verme süreçlerinin merkezindedir

Yapay zeka ile entegre çalışan programlama becerileri, yalnızca teknik bir
yetkinlik değil; aynı zamanda **geleceğin mesleklerinde rekabet avantajı**
sağlayan kritik bir yetkinliktir.

Bu analiz, teknoloji odaklı kariyer planlamasında **AI ve yazılım
uzmanlıklarının uzun vadede sürdürülebilir ve yüksek getirili alanlar**
olduğunu göstermektedir.
"""

st.markdown(insight_text)

