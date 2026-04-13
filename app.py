import streamlit as st
import pandas as pd
import os

# =========================
# CONFIG
# =========================
st.set_page_config(
    page_title="SMKN 1 Denpasar",
    layout="wide"
)

# =========================
# STYLE (CSS FINAL - HAPUS KOTAK)
# =========================
st.markdown("""
<style>
/* Hilangkan padding berlebih dari Streamlit */
.block-container { 
    padding-top: 2rem; 
}

.stApp { 
    background-color: #f8fafc; 
}

/* LOGIN BOX - Didesain ulang agar bersih */
.login-box {
    max-width: 420px;
    margin: auto;
    margin-top: 30px;
    background: white;
    padding: 35px;
    border-radius: 15px;
    box-shadow: 0 4px 25px rgba(0,0,0,0.1);
}

/* Container untuk Logo & Teks agar Center tanpa Kolom */
.center-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    text-align: center;
    width: 100%;
}

.title-text {
    font-size: 26px;
    font-weight: 700;
    color: #1e293b;
    margin-top: 15px;
    margin-bottom: 5px;
}

.subtitle-text {
    color: #64748b;
    font-size: 14px;
    margin-bottom: 25px;
}

/* Memaksa gambar logo yang dipanggil via st.image agar center */
[data-testid="stImage"] {
    display: flex;
    justify-content: center;
    margin-bottom: 0px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION & LOGOUT
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
if "role" not in st.session_state:
    st.session_state.role = None

def logout():
    st.session_state.login = False
    st.session_state.role = None
    st.rerun()

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.login:
    # Membuka div login-box
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    
    # 1. Header (Logo & Judul) dalam satu div center
    st.markdown("<div class='center-header'>", unsafe_allow_html=True)
    
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)
    else:
        st.write("🏫")
        
    st.markdown("""
        <div class='title-text'>SMKN 1 Denpasar</div>
        <div class='subtitle-text'>Sistem Analisis Minat & Bakat Siswa</div>
    </div>
    """, unsafe_allow_html=True)

    # 2. Tabs Login (Tanpa Kolom di atasnya)
    tab1, tab2 = st.tabs(["Login", "Daftar"])
    
    with tab1:
        email = st.text_input("Email", placeholder="Masukkan email anda", key="l_user")
        password = st.text_input("Password", type="password", key="l_pass")
        if st.button("Login Sekarang", use_container_width=True, type="primary"):
            if email and password:
                st.session_state.login = True
                st.session_state.role = "guru"
                st.rerun()
            else:
                st.error("Isi email dan password!")
                
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# DASHBOARD UTAMA (SETELAH LOGIN)
# ============================================================

# HEADER ATAS & TOMBOL LOGOUT
h_col1, h_col2 = st.columns([8, 2])
with h_col1:
    st.title("🏫 Dashboard Utama")
    st.caption("Selamat datang kembali di sistem SMKN 1 Denpasar")

with h_col2:
    st.write("##") # Penyeimbang posisi vertikal
    if st.button("🚪 Logout", use_container_width=True):
        logout()

st.divider()

# =========================
# LOAD DATA & ANALISIS
# =========================
@st.cache_data
def load_data():
    try:
        url = "https://docs.google.com/spreadsheets/d/1wIMyXy5C0Q6TLUb09jJcKkTWQ830F_phjYtwOUthyX8/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("Gagal memuat data dari sumber.")
    st.stop()

# Kalkulasi Skor
df["Logika"] = df[["Saya suka membuat program / coding", "Saya suka bekerja dengan angka / matematika", "Saya suka bekerja menggunakan komputer"]].mean(axis=1)
df["Kreatif"] = df[["Saya suka membuat desain visual (poster, video, UI)", "Saya suka menggambar / ilustrasi"]].mean(axis=1)
df["Teknik"] = df[["Saya suka memperbaiki mesin / kendaraan", "Saya suka bekerja dengan listrik / instalasi", "Saya suka merakit atau membongkar alat", "Saya suka bekerja di lapangan"]].mean(axis=1)
df["Sosial"] = df[["Saya suka berbicara di depan umum", "Saya suka bekerja dalam tim", "Saya suka memimpin atau mengatur orang lain"]].mean(axis=1)
df["Skor"] = df[["Logika", "Kreatif", "Teknik", "Sosial"]].mean(axis=1)

# =========================
# MENU UTAMA
# =========================
menu = st.radio("Pilih Menu:", ["Dashboard", "Data Siswa", "Ranking"], horizontal=True)

if menu == "Dashboard":
    st.subheader("📊 Analisis Statistik")
    
    c1, c2 = st.columns(2)
    jurusan = c1.selectbox("Filter Jurusan", ["Semua"] + list(df["Jurusan SMK"].dropna().unique()))
    search = c2.text_input("Cari Nama")

    temp = df.copy()
    if jurusan != "Semua":
        temp = temp[temp["Jurusan SMK"] == jurusan]
    if search:
        temp = temp[temp["Nama Lengkap"].str.contains(search, case=False, na=False)]

    st.metric("Total Siswa", len(temp))
    st.bar_chart(temp[["Logika", "Kreatif", "Teknik", "Sosial"]])

elif menu == "Data Siswa":
    st.subheader("📋 Database")
    if st.session_state.role == "guru":
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Akses dibatasi.")

elif menu == "Ranking":
    st.subheader("🏆 Top 10 Siswa")
    top = df.sort_values(by="Skor", ascending=False).head(10)
    st.table(top[["Nama Lengkap", "Jurusan SMK", "Skor"]])
