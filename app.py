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
# STYLE
# =========================
st.markdown("""
<style>

.stApp {
    background: #f5f7fb;
}

/* LOGIN WRAPPER */
.login-box {
    max-width: 420px;
    margin: auto;
    margin-top: 40px;
    padding: 20px;
}

/* HEADER LOGIN (NAIK KE ATAS) */
.login-header {
    text-align: center;
    margin-bottom: 15px;
}

/* TITLE */
.title {
    font-size: 24px;
    font-weight: 700;
    margin-top: 5px;
}

/* CARD DASHBOARD */
.card {
    background: white;
    padding: 15px;
    border-radius: 12px;
    box-shadow: 0 2px 10px rgba(0,0,0,0.05);
    margin-bottom: 10px;
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
# LOGIN PAGE
# =========================
if not st.session_state.login:

    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    # HEADER (NAIK KE ATAS)
    st.markdown("<div class='login-header'>", unsafe_allow_html=True)

    if os.path.exists("logo.png"):
        st.image("logo.png", width=110)
    else:
        st.write("🏫")

    st.markdown("<div class='title'>SMKN 1 Denpasar</div>", unsafe_allow_html=True)
    st.caption("Sistem Analisis Minat & Bakat Siswa")

    st.markdown("</div>", unsafe_allow_html=True)

    # TAB LOGIN
    tab1, tab2 = st.tabs(["Login", "Daftar"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if email and password:
                st.session_state.login = True
                st.rerun()
            else:
                st.error("Isi data lengkap")

    with tab2:
        email2 = st.text_input("Email baru")
        pass2 = st.text_input("Password baru", type="password")
        role = st.selectbox("Daftar sebagai", ["siswa", "guru"])

        if st.button("Daftar"):
            if email2 and pass2:
                st.success("Akun berhasil dibuat")
            else:
                st.warning("Lengkapi data")

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================
# HEADER DASHBOARD
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

# =========================
# DATA DEMO
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
    st.warning("Data tidak tersedia")
    st.stop()

# =========================
# MENU
# =========================
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
