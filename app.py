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
# STYLE (Halaman Login Rapi)
# =========================
st.markdown("""
<style>
.stApp {
    background: #f5f7fb;
}

/* LOGIN BOX */
.login-box {
    max-width: 420px;
    margin: auto;
    margin-top: 60px;
    background: white;
    padding: 30px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}

/* CENTER HEADER */
.login-header {
    text-align: center;
    margin-bottom: 20px;
}

.title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 10px;
}

/* Memaksa Logo di Tengah Kolom */
[data-testid="stImage"] {
    display: flex;
    justify-content: center;
}
</style>
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

# =========================
# LOGOUT
# =========================
def logout():
    st.session_state.login = False
    st.rerun()

# =========================
# LOGIN PAGE (Hanya Bagian Ini yang Berubah)
# =========================
if not st.session_state.login:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    # Logo dikecilkan dengan kolom [1.5, 0.5, 1.5]
    col_l1, col_l2, col_l3 = st.columns([1.5, 0.5, 1.5])
    with col_l2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.write("🏫")

    # Judul & Caption Center
    st.markdown("""
        <div class='login-header'>
            <div class='title'>SMKN 1 Denpasar</div>
            <div style='color:gray; font-size:14px;'>Sistem Analisis Minat & Bakat Siswa</div>
        </div>
    """, unsafe_allow_html=True)

    # Tabs
    tab1, tab2 = st.tabs(["Login", "Daftar"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            if email and password:
                st.session_state.login = True
                st.rerun()
            else:
                st.error("Isi email & password")

    with tab2:
        email2 = st.text_input("Email baru")
        pass2 = st.text_input("Password baru", type="password")
        role = st.selectbox("Daftar sebagai", ["siswa", "guru"])
        if st.button("Daftar", use_container_width=True):
            if email2 and pass2:
                st.success("Akun berhasil dibuat, silakan login")
            else:
                st.warning("Lengkapi data")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================
# DASHBOARD (KEMBALI KE KODE ASLI KAMU)
# =========================
col1, col2, col3 = st.columns([1, 6, 2])

with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=60)
    else:
        st.write("🏫")

with col2:
    st.title("SMKN 1 Denpasar")
    st.caption("Dashboard Analisis Minat & Bakat")

with col3:
    if st.button("🚪 Logout"):
        logout()

st.divider()

# DATA DEMO
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
    st.warning("Data tidak tersedia")
    st.stop()

# MENU
menu = st.radio("Menu", ["Dashboard", "Data", "Ranking", "Settings"], horizontal=True)

if menu == "Dashboard":
    st.subheader("📊 Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Siswa", len(df))
    c2.metric("Rata-rata", 80)
    c3.metric("Status", "Aktif")
    st.bar_chart(df.iloc[:, 0:1])

elif menu == "Data":
    st.subheader("📋 Data")
    st.dataframe(df)

elif menu == "Ranking":
    st.subheader("🏆 Ranking")
    st.dataframe(df.head(10))

elif menu == "Settings":
    st.subheader("⚙️ Settings")
    if st.button("Refresh"):
        st.rerun()
    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        file_name="data.csv"
    )
