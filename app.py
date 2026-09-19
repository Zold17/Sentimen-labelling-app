"""
Aplikasi Data Labeling & Klasifikasi Sentimen
------------------------------------------------
Simulasi proses kerja Data Annotator: memberi label pada data teks,
lalu membandingkan dengan prediksi otomatis dari sistem AI sederhana.

Cara jalankan:
    streamlit run app.py
"""

import pandas as pd
import streamlit as st
from classifier import prediksi_sentimen

st.set_page_config(page_title="Data Labeling & Sentiment Classifier", layout="wide")

st.title("🏷️ Data Labeling & Sentiment Classifier")
st.caption(
    "Simulasi proses kerja Data Annotator — beri label manual pada data teks, "
    "lalu bandingkan dengan hasil prediksi otomatis."
)


# ---- Load data ----
@st.cache_data
def load_data():
    return pd.read_csv("data_ulasan.csv")


if "df" not in st.session_state:
    st.session_state.df = load_data()

df = st.session_state.df

# ---- Sidebar: statistik ----
st.sidebar.header("📊 Statistik")
st.sidebar.metric("Total Data", len(df))

st.sidebar.divider()
st.sidebar.subheader("Tentang Project Ini")
st.sidebar.write(
    "Aplikasi ini mensimulasikan alur kerja data annotation: "
    "membaca data mentah, memberi label, dan membandingkannya dengan "
    "hasil model AI sederhana (rule-based sentiment classifier)."
)

# ---- Tab: Labeling Manual vs Hasil Otomatis ----
tab1, tab2, tab3 = st.tabs(["📝 Labeling Manual", "🤖 Prediksi Otomatis", "📈 Perbandingan"])

with tab1:
    st.subheader("Beri Label Manual pada Data")
    st.write("Pilih label yang menurutmu paling sesuai untuk tiap ulasan.")

    for idx, row in df.iterrows():
        col1, col2 = st.columns([3, 1])
        with col1:
            st.write(f"**{row['id']}.** {row['teks_ulasan']}")
        with col2:
            label_baru = st.selectbox(
                "Label",
                ["positif", "negatif", "netral"],
                index=["positif", "negatif", "netral"].index(row["label_asli"]),
                key=f"label_{row['id']}",
                label_visibility="collapsed",
            )
            df.at[idx, "label_asli"] = label_baru

with tab2:
    st.subheader("Hasil Prediksi Otomatis (Rule-Based Classifier)")
    st.write(
        "Sistem ini memprediksi sentimen menggunakan pendekatan lexicon "
        "(kamus kata positif/negatif) — pendekatan paling dasar sebelum "
        "menggunakan model machine learning yang lebih kompleks."
    )

    hasil_prediksi = []
    for _, row in df.iterrows():
        label_pred, skor = prediksi_sentimen(row["teks_ulasan"])
        hasil_prediksi.append(label_pred)

    df["prediksi_otomatis"] = hasil_prediksi
    st.dataframe(
        df[["id", "teks_ulasan", "prediksi_otomatis"]],
        use_container_width=True,
        hide_index=True,
    )

with tab3:
    st.subheader("Perbandingan Label Manual vs Prediksi Otomatis")

    if "prediksi_otomatis" in df.columns:
        df["cocok"] = df["label_asli"] == df["prediksi_otomatis"]
        akurasi = df["cocok"].mean() * 100

        col1, col2, col3 = st.columns(3)
        col1.metric("Akurasi", f"{akurasi:.1f}%")
        col2.metric("Cocok", int(df["cocok"].sum()))
        col3.metric("Tidak Cocok", int((~df["cocok"]).sum()))

        st.divider()
        st.write("**Data yang berbeda antara label manual dan prediksi otomatis:**")
        df_beda = df[~df["cocok"]][["id", "teks_ulasan", "label_asli", "prediksi_otomatis"]]
        if len(df_beda) > 0:
            st.dataframe(df_beda, use_container_width=True, hide_index=True)
        else:
            st.success("Semua label cocok dengan prediksi otomatis!")
    else:
        st.info("Buka tab 'Prediksi Otomatis' dulu untuk menghasilkan perbandingan.")

st.divider()

# ---- Download hasil ----
st.subheader("💾 Simpan Hasil Labeling")
csv = df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="Download hasil sebagai CSV",
    data=csv,
    file_name="hasil_labeling.csv",
    mime="text/csv",
)
