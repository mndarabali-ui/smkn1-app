import streamlit as st
import pandas as pd
import os

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="SMKN 1 Denpasar",
    layout="wide",
    page_icon="🏫"
)

# =========================
# MODERN STYLE
# =========================
st.markdown("""
<style>

/* background */
.stApp {
    background: #f5f7fb;
}

/* HEADER */
.header {
    display: flex;
    align-items: center;
    gap: 15px;
    padding: 15px 20px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 20px;
}

/* TITLE */
.title {
    font-size: 22px;
    font-weight: 700;
}

/* CARD */
.card {
    background: white;
    padding: 20px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

/* BUTTON */
.stButton button {
    border-radius: 8px;
    border: none;
    background: #2563eb;
    color: white;
    padding: 8px 16px;
}

/* RADIO MENU */
div[role="radiogroup"] > label {
    padding: 6px 14px;
    border-radius: 8px;
    background: white;
    margin-right: 5px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
col1, col2 = st.columns([1, 8])

with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=70)
    else:
        st.write("🏫")

with col2:
    st.markdown("<div class='title'>SMKN 1 Denpasar</div>", unsafe_allow_html=True)
    st.caption("Sistem Analisis Minat & Bakat Siswa")

st.divider()

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1wIMyXy5C0Q6TLUb09jJcKkTWQ830F_phjYtwOUthyX8/export?format=csv"
    try:
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.error("Data gagal dimuat")
    st.stop()

# =========================
# ANALISIS
# =========================
df["Logika"] = df[[
    "Saya suka membuat program / coding",
    "Saya suka bekerja dengan angka / matematika",
    "Saya suka bekerja menggunakan komputer"
]].mean(axis=1)

df["Kreatif"] = df[[
    "Saya suka membuat desain visual (poster, video, UI)",
    "Saya suka menggambar / ilustrasi"
]].mean(axis=1)

df["Teknik"] = df[[
    "Saya suka memperbaiki mesin / kendaraan",
    "Saya suka bekerja dengan listrik / instalasi",
    "Saya suka merakit atau membongkar alat",
    "Saya suka bekerja di lapangan"
]].mean(axis=1)

df["Sosial"] = df[[
    "Saya suka berbicara di depan umum",
    "Saya suka bekerja dalam tim",
    "Saya suka memimpin atau mengatur orang lain"
]].mean(axis=1)

df["Skor"] = df[["Logika","Kreatif","Teknik","Sosial"]].mean(axis=1)

# =========================
# MENU
# =========================
menu = st.radio("Menu", ["Dashboard", "Data", "Ranking", "Settings"], horizontal=True)

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.markdown("### 📊 Dashboard")

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Siswa", len(df))
    col2.metric("Rata-rata Skor", round(df["Skor"].mean(), 2))
    col3.metric("Kategori Tertinggi", "Analisis Minat")

    st.markdown("### 📈 Grafik Minat")

    st.bar_chart(df[["Logika","Kreatif","Teknik","Sosial"]])

# =========================
# DATA
# =========================
elif menu == "Data":

    st.markdown("### 📋 Data Siswa")
    st.dataframe(df, use_container_width=True)

# =========================
# RANKING
# =========================
elif menu == "Ranking":

    st.markdown("### 🏆 Top Ranking")

    top = df.sort_values("Skor", ascending=False).head(10)
    st.dataframe(top, use_container_width=True)

# =========================
# SETTINGS
# =========================
elif menu == "Settings":

    st.markdown("### ⚙️ Settings")

    if st.button("Refresh Data"):
        st.rerun()

    st.download_button(
        "Download Data CSV",
        df.to_csv(index=False),
        file_name="siswa.csv"
    )
