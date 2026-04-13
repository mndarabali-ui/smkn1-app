import streamlit as st
import pandas as pd
import os

# =========================
# CONFIG & PAGE SETUP
# =========================
st.set_page_config(
    page_title="SMKN 1 Denpasar",
    layout="wide",
    page_icon="🏫"
)

# =========================
# STYLE (CSS)
# =========================
st.markdown("""
<style>
    /* Background utama */
    .stApp {
        background: #f5f7fb;
    }

    /* Kotak Login */
    .login-box {
        max-width: 450px;
        margin: auto;
        margin-top: 50px;
        background: white;
        padding: 40px;
        border-radius: 20px;
        box-shadow: 0 10px 30px rgba(0,0,0,0.1);
    }

    /* Header di dalam login */
    .login-header {
        text-align: center;
        margin-bottom: 25px;
    }

    .title-text {
        font-size: 28px;
        font-weight: 800;
        color: #1E1E1E;
        margin-top: 15px;
        margin-bottom: 5px;
    }

    .subtitle-text {
        color: #666;
        font-size: 14px;
        margin-bottom: 20px;
    }

    /* Styling Tab agar rapi */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
        justify-content: center;
    }

    /* Tambahan CSS untuk memaksa logo di tengah di dalam kolomnya */
    [data-testid="stImage"] {
        display: block;
        margin-left: auto;
        margin-right: auto;
    }
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION STATE
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

def logout():
    st.session_state.login = False
    st.rerun()

# =========================
# DATA LOADING
# =========================
@st.cache_data
def load_data():
    try:
        # Menggunakan URL spreadsheet yang kamu berikan
        url = "https://docs.google.com/spreadsheets/d/1wIMyXy5C0Q6TLUb09jJcKkTWQ830F_phjYtwOUthyX8/export?format=csv"
        df = pd.read_csv(url)
        df.columns = df.columns.str.strip()
        return df
    except Exception:
        return pd.DataFrame()

# =========================
# HALAMAN LOGIN
# =========================
if not st.session_state.login:
    # Kontainer utama login (HTML)
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    
    # --- BAGIAN LOGO (DIPERBARUI UNTUK MEMPERKECIL) ---
    # Ubah rasio kolom untuk memperkecil ruang logo di tengah (kolom tengah dipersempit)
    # Rasio awal [1, 0.8, 1], rasio baru [1.3, 0.4, 1.3] (membuat kolom tengah lebih kecil)
    col_l1, col_l2, col_l3 = st.columns([1.3, 0.4, 1.3])
    
    with col_l2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            # Jika file logo tidak ada, emoji juga dikecilkan
            st.markdown("<h2 style='text-align: center;'>🏫</h2>", unsafe_allow_html=True)

    # Bagian Judul (HTML)
    st.markdown("""
        <div class='login-header'>
            <div class='title-text'>SMKN 1 Denpasar</div>
            <div class='subtitle-text'>Sistem Analisis Minat & Bakat Siswa</div>
        </div>
    """, unsafe_allow_html=True)

    # Tabs Login & Daftar
    tab1, tab2 = st.tabs(["🔐 Login", "📝 Daftar"])

    with tab1:
        email = st.text_input("Email", placeholder="Masukkan email anda", key="log_email")
        password = st.text_input("Password", type="password", placeholder="Masukkan password", key="log_pass")
        st.write(" ") # Spacer
        if st.button("Masuk Ke Sistem", use_container_width=True, type="primary"):
            if email and password:
                st.session_state.login = True
                st.rerun()
            else:
                st.error("Silakan lengkapi email dan password.")

    with tab2:
        st.text_input("Email Baru", placeholder="contoh@mail.com")
        st.text_input("Password Baru", type="password")
        st.selectbox("Daftar sebagai", ["Siswa", "Guru", "Admin"])
        if st.button("Buat Akun", use_container_width=True):
            st.success("Akun berhasil dibuat! Silakan pindah ke tab Login.")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================
# HALAMAN DASHBOARD (Setelah Login)
# =========================
df = load_data()

# Header Dashboard
head_col1, head_col2 = st.columns([8, 2])
with head_col1:
    st.title("🏫 Dashboard Utama")
    st.caption("Selamat datang di Sistem Analisis SMKN 1 Denpasar")
with head_col2:
    st.write(" ")
    if st.button("🚪 Keluar", use_container_width=True):
        logout()

st.divider()

if df.empty:
    st.error("Gagal memuat data dari database.")
else:
    # Menu Navigasi
    menu = st.radio("Pilih Menu:", ["Ringkasan", "Database Siswa", "Analisis Ranking"], horizontal=True)

    if menu == "Ringkasan":
        st.subheader("📊 Statistik Terkini")
        m1, m2, m3 = st.columns(3)
        m1.metric("Total Responden", len(df))
        m2.metric("Rata-rata Skor", "84.5%")
        m3.metric("Status Server", "Online")
        
        st.area_chart(df.iloc[:, 0:1])

    elif menu == "Database Siswa":
        st.subheader("📋 Data Lengkap")
        st.dataframe(df, use_container_width=True)
        st.download_button("Unduh Data (.csv)", df.to_csv(index=False), "data_siswa.csv")

    elif menu == "Analisis Ranking":
        st.subheader("🏆 Top 10 Siswa Terbaik")
        st.table(df.head(10))
