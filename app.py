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
# STYLE (CSS) - DIBERSIHKAN TOTAL
# =========================
st.markdown("""
<style>
/* Hilangkan ruang kosong di paling atas aplikasi */
.block-container { padding-top: 1rem; }

.stApp { background-color: #f8fafc; }

/* KOTAK LOGIN UTAMA */
.login-box {
    max-width: 420px;
    margin: auto;
    margin-top: 50px;
    background: white;
    padding: 35px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.1);
}

/* Memaksa Logo & Teks ke Tengah Tanpa Container Streamlit */
.center-header {
    text-align: center;
    width: 100%;
    margin-bottom: 20px;
}

.title-text {
    font-size: 26px;
    font-weight: 700;
    color: #1e293b;
    margin-top: 15px;
}

/* Memastikan st.image berada di tengah */
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
    # Buka kotak login
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    # 1. Header (Logo & Judul) - Pakai HTML murni agar tidak ada kotak hantu
    st.markdown("<div class='center-header'>", unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)
    else:
        st.write("🏫")
    
    st.markdown("""
            <div class='title-text'>SMKN 1 Denpasar</div>
            <div style='color: gray; font-size: 14px;'>
                Sistem Analisis Minat & Bakat Siswa
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.write("---") # Garis pembatas tipis

    # 2. Form Login (Langsung input, HAPUS st.tabs karena itu penyebab kotaknya)
    email = st.text_input("Email", placeholder="Masukkan email anda", key="l_user")
    password = st.text_input("Password", type="password", key="l_pass")
    
    st.write("") # Spacer
    if st.button("Login Sekarang", use_container_width=True, type="primary"):
        if email and password:
            st.session_state.login = True
            st.session_state.role = "guru"
            st.rerun()
    
    # 3. Footer Login
    st.markdown("<div style='text-align:center; font-size:12px; margin-top:15px; color:#64748b;'>Belum punya akun? <span style='color:blue; cursor:pointer;'>Daftar</span></div>", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# DASHBOARD UTAMA (SETELAH LOGIN)
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

# --- LOAD DATA ---
try:
    url = "https://docs.google.com/spreadsheets/d/1wIMyXy5C0Q6TLUb09jJcKkTWQ830F_phjYtwOUthyX8/export?format=csv"
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()

    menu = st.radio("Navigasi:", ["Dashboard", "Data", "Ranking"], horizontal=True)
    
    if menu == "Dashboard":
        st.subheader("📊 Statistik")
        st.metric("Total Responden", len(df))
        # Logika analisis singkat
        cols = ["Logika", "Kreatif", "Teknik", "Sosial"]
        # Dummy data untuk contoh jika kolom belum ada di CSV
        st.bar_chart(df.head(10)) 
    elif menu == "Data":
        st.dataframe(df, use_container_width=True)
except:
    st.error("Gagal memuat data dari Google Sheets.")
