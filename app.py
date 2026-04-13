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
# STYLE (DIPERBAIKI)
# =========================
st.markdown("""
<style>
/* Background aplikasi */
.stApp {
    background-color: #f8fafc;
}

/* Menghilangkan border default tabs dan memberi style kotak putih */
[data-testid="stTabContent"] {
    background: white;
    padding: 30px;
    border-radius: 0 0 15px 15px;
    box-shadow: 0 10px 20px rgba(0,0,0,0.05);
}

/* Mempercantik bagian atas tab */
div[data-testid="stTabs"] {
    max-width: 420px;
    margin: auto;
    background: #ffffff;
    border-radius: 15px 15px 0 0;
    padding-top: 10px;
}

/* Memaksa Logo ke tengah */
[data-testid="stImage"] {
    display: flex;
    justify-content: center;
}

.title-text {
    font-size: 28px;
    font-weight: 800;
    color: #1e293b;
    text-align: center;
    margin-bottom: 5px;
}

.subtitle-text {
    color: #64748b;
    font-size: 14px;
    text-align: center;
    margin-bottom: 25px;
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
    st.write("##") 
    
    # 1. LOGO (Bersih di luar kotak)
    col_l1, col_l2, col_l3 = st.columns([1.5, 0.6, 1.5])
    with col_l2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.write("<h1 style='text-align:center;'>🏫</h1>", unsafe_allow_html=True)

    # 2. JUDUL (Bersih di luar kotak)
    st.markdown("<div class='title-text'>SMKN 1 Denpasar</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle-text'>Sistem Analisis Minat & Bakat Siswa</div>", unsafe_allow_html=True)

    # 3. FORM LOGIN (Otomatis dibungkus kotak putih oleh CSS)
    tab1, tab2 = st.tabs(["🔒 Login", "📝 Daftar"])
    
    with tab1:
        email = st.text_input("Email", key="login_user", placeholder="Masukkan email anda")
        password = st.text_input("Password", type="password", key="login_pass", placeholder="Masukkan password")
        st.write("##")
        if st.button("Masuk Sekarang", use_container_width=True, type="primary"):
            if email and password:
                st.session_state.login = True
                st.session_state.role = "guru"
                st.rerun()
            else:
                st.error("Silahkan isi email dan password.")
    
    with tab2:
        st.info("Fitur pendaftaran siswa baru sedang dalam pemeliharaan.")

    st.stop()

# ============================================================
# DASHBOARD UTAMA (Hanya muncul jika sudah login)
# ============================================================
head1, head2 = st.columns([8, 2])
with head1:
    st.title("🏫 Dashboard Utama")
    st.caption("Selamat datang di Sistem Analisis SMKN 1 Denpasar")
with head2:
    st.write("##") 
    if st.button("🚪 Logout", use_container_width=True):
        logout()

st.divider()

# LOAD DATA & ANALISIS
url = "https://docs.google.com/spreadsheets/d/1wIMyXy5C0Q6TLUb09jJcKkTWQ830F_phjYtwOUthyX8/export?format=csv"
try:
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    
    menu = st.radio("Pilih Menu", ["📊 Statistik", "📄 Data Siswa", "🏆 Ranking"], horizontal=True)
    
    if "Statistik" in menu:
        st.subheader("Ringkasan Data")
        st.metric("Total Siswa Terdata", len(df))
        st.bar_chart(df.select_dtypes(include=['number']).head(10)) 
        
    elif "Data Siswa" in menu:
        st.dataframe(df, use_container_width=True)
        
except Exception as e:
    st.error(f"Gagal memuat data dari Google Sheets. Pastikan link publik. Error: {e}")
