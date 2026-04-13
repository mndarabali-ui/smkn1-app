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
# STYLE (CSS)
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
}

/* LOGIN BOX UTAMA */
.login-box {
    max-width: 420px;
    margin: auto;
    margin-top: 50px;
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.title {
    font-size: 26px;
    font-weight: 700;
    margin-top: 15px;
    text-align: center;
}

/* Memaksa Logo di Tengah */
[data-testid="stImage"] {
    display: flex;
    justify-content: center;
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
    # Pembungkus utama dipindahkan ke sini
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    # Logo Center (Menggunakan kolom untuk mengatur ukuran)
    with col_l2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.write("🏫")

    # Teks Judul Center
    st.markdown("""
        <div style='text-align: center;'>
            <div class='title'>SMKN 1 Denpasar</div>
            <div style='color: gray; font-size: 14px; margin-bottom: 20px;'>
                Sistem Analisis Minat & Bakat Siswa
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Form Login & Daftar
    tab1, tab2 = st.tabs(["Login", "Daftar"])
    with tab1:
        email = st.text_input("Email", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True, type="primary"):
            if email and password:
                st.session_state.login = True
                st.session_state.role = "guru"
                st.rerun()
    
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# DASHBOARD UTAMA
# ============================================================

# HEADER & TOMBOL LOGOUT
head1, head2 = st.columns([8, 2])
with head1:
    st.title("🏫 Dashboard Utama")
    st.caption("Selamat datang di Sistem Analisis SMKN 1 Denpasar")

with head2:
    st.write("##") 
    if st.button("🚪 Logout", use_container_width=True):
        logout()

st.divider()

# =========================
# LOAD DATA
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
    st.warning("Data tidak tersedia.")
    st.stop()

# =========================
# ANALISIS SKOR
# =========================
df["Logika"] = df[["Saya suka membuat program / coding", "Saya suka bekerja dengan angka / matematika", "Saya suka bekerja menggunakan komputer"]].mean(axis=1)
df["Kreatif"] = df[["Saya suka membuat desain visual (poster, video, UI)", "Saya suka menggambar / ilustrasi"]].mean(axis=1)
df["Teknik"] = df[["Saya suka memperbaiki mesin / kendaraan", "Saya suka bekerja dengan listrik / instalasi", "Saya suka merakit atau membongkar alat", "Saya suka bekerja di lapangan"]].mean(axis=1)
df["Sosial"] = df[["Saya suka berbicara di depan umum", "Saya suka bekerja dalam tim", "Saya suka memimpin atau mengatur orang lain"]].mean(axis=1)
df["Skor"] = df[["Logika", "Kreatif", "Teknik", "Sosial"]].mean(axis=1)

# =========================
# MENU NAVIGASI
# =========================
menu = st.radio(
    "Navigasi Menu:",
    ["Dashboard", "Data", "Ranking", "Settings"],
    horizontal=True
)

if menu == "Dashboard":
    st.subheader("📊 Statistik Siswa")
    
    col_f1, col_f2 = st.columns(2)
    with col_f1:
        jurusan = st.selectbox("Filter Jurusan", ["Semua"] + list(df["Jurusan SMK"].dropna().unique()))
    with col_f2:
        search = st.text_input("Cari Nama Siswa")

    temp = df.copy()
    if jurusan != "Semua":
        temp = temp[temp["Jurusan SMK"] == jurusan]
    if search:
        temp = temp[temp["Nama Lengkap"].str.contains(search, case=False, na=False)]

    m1, m2 = st.columns(2)
    m1.metric("Total Responden", len(temp))
    m2.metric("Rata-rata Skor", round(temp["Skor"].mean(), 2))

    st.bar_chart(temp[["Logika", "Kreatif", "Teknik", "Sosial"]], use_container_width=True)

elif menu == "Data":
    st.subheader("📋 Database Lengkap Siswa")
    if st.session_state.role == "guru":
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Hanya guru yang bisa melihat database.")

elif menu == "Ranking":
    st.subheader("🏆 Top 10 Ranking")
    top = df.sort_values(by="Skor", ascending=False).head(10)
    st.table(top[["Nama Lengkap", "Jurusan SMK", "Skor"]])

elif menu == "Settings":
    st.subheader("⚙️ Pengaturan")
    if st.button("Refresh Data"):
        st.rerun()
    st.download_button("Download CSV", df.to_csv(index=False), file_name="data.csv")
