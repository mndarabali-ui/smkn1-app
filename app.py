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
# STYLE MODERN
# =========================
st.markdown("""
<style>

.stApp {
    background: #f5f7fb;
}

/* HEADER */
.header {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 12px 18px;
    background: white;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 15px;
}

/* TITLE */
.title {
    font-size: 22px;
    font-weight: 700;
}

/* CARD */
.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}

/* BUTTON */
.stButton button {
    border-radius: 8px;
    background: #2563eb;
    color: white;
    border: none;
}

/* MENU */
div[role="radiogroup"] > label {
    background: white;
    padding: 6px 12px;
    border-radius: 8px;
    margin-right: 5px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION LOGIN
# =========================
if "login" not in st.session_state:
    st.session_state.login = True  # langsung login biar fokus UI

# =========================
# LOGOUT FUNCTION
# =========================
def logout():
    st.session_state.login = False
    st.rerun()

# =========================
# LOGIN CHECK
# =========================
if not st.session_state.login:
    st.title("🔒 Silakan Login")
    if st.button("Login"):
        st.session_state.login = True
        st.rerun()
    st.stop()

# =========================
# HEADER (LOGO + TITLE + LOGOUT)
# =========================
col1, col2, col3 = st.columns([1, 6, 2])

with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=60)
    else:
        st.write("🏫")

with col2:
    st.markdown("<div class='title'>SMKN 1 Denpasar</div>", unsafe_allow_html=True)
    st.caption("Sistem Analisis Minat & Bakat Siswa")

with col3:
    st.button("🚪 Logout", on_click=logout)

st.divider()

# =========================
# LOAD DATA (AMAN)
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
    st.error("Data tidak bisa dimuat")
    st.stop()

# =========================
# ANALISIS
# =========================
try:
    df["Logika"] = df[
        ["Saya suka membuat program / coding",
         "Saya suka bekerja dengan angka / matematika",
         "Saya suka bekerja menggunakan komputer"]
    ].mean(axis=1)

    df["Kreatif"] = df[
        ["Saya suka membuat desain visual (poster, video, UI)",
         "Saya suka menggambar / ilustrasi"]
    ].mean(axis=1)

    df["Teknik"] = df[
        ["Saya suka memperbaiki mesin / kendaraan",
         "Saya suka bekerja dengan listrik / instalasi",
         "Saya suka merakit atau membongkar alat",
         "Saya suka bekerja di lapangan"]
    ].mean(axis=1)

    df["Sosial"] = df[
        ["Saya suka berbicara di depan umum",
         "Saya suka bekerja dalam tim",
         "Saya suka memimpin atau mengatur orang lain"]
    ].mean(axis=1)

    df["Skor"] = df[["Logika","Kreatif","Teknik","Sosial"]].mean(axis=1)

except:
    st.warning("Kolom tidak sesuai, Skor diset 0")
    df["Skor"] = 0

# =========================
# MENU
# =========================
menu = st.radio(
    "Menu",
    ["Dashboard", "Data", "Ranking", "Settings"],
    horizontal=True
)

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":

    st.markdown("### 📊 Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Siswa", len(df))
    c2.metric("Rata-rata Skor", round(df["Skor"].mean(), 2))
    c3.metric("Kategori", "Minat & Bakat")

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

    st.markdown("### 🏆 Ranking Top 10")
    st.dataframe(df.sort_values("Skor", ascending=False).head(10))

# =========================
# SETTINGS
# =========================
elif menu == "Settings":

    st.markdown("### ⚙️ Settings")

    if st.button("Refresh Data"):
        st.rerun()

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        file_name="data_siswa.csv"
    )
