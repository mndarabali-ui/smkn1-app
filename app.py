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
# STYLE
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #f8fafc;
}

/* KOTAK PUTIH HANYA UNTUK FORM (DIBERSIHKAN DARI LOGO) */
.login-box {
    max-width: 420px;
    margin: auto;
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

.title {
    font-size: 26px;
    font-weight: 700;
    margin-top: 10px;
    text-align: center;
}

/* Memaksa st.image ke tengah */
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
    st.write("##") 
    
    # 1. LOGO (DI LUAR KOTAK)
    col_l1, col_l2, col_l3 = st.columns([1.5, 0.5, 1.5])
    with col_l2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.write("🏫")

    # 2. JUDUL (DI LUAR KOTAK - Agar background putihnya hilang)
    st.markdown("""
        <div style='text-align: center; margin-bottom: 20px;'>
            <div style='font-size: 26px; font-weight: 700; color: #1e293b;'>SMKN 1 Denpasar</div>
            <div style='color: gray; font-size: 14px;'>
                Sistem Analisis Minat & Bakat Siswa
            </div>
        </div>
    """, unsafe_allow_html=True)

    # 3. KOTAK PUTIH DIMULAI DISINI (Hanya membungkus form input)
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Daftar"])
    with tab1:
        email = st.text_input("Email", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")
        if st.button("Login", use_container_width=True, type="primary"):
            if email and password:
                st.session_state.login = True
                st.session_state.role = "guru"
                st.rerun()
    
    # Penutup kotak putih
    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# ============================================================
# DASHBOARD UTAMA
# ============================================================
head1, head2 = st.columns([8, 2])
with head1:
    st.title("🏫 Dashboard Utama")
    st.caption("SMKN 1 Denpasar")
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
    
    menu = st.radio("Menu", ["Dashboard", "Data", "Ranking"], horizontal=True)
    
    if menu == "Dashboard":
        st.subheader("📊 Statistik")
        st.metric("Total Siswa", len(df))
        st.bar_chart(df.head(10)) 
    elif menu == "Data":
        st.dataframe(df, use_container_width=True)
except:
    st.error("Gagal memuat data.")
