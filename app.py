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

/* CENTER LOGIN PAGE */
.center {
    height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    text-align: center;
}

/* TITLE */
.title {
    font-size: 26px;
    font-weight: 700;
    margin-top: 10px;
}

/* CARD LOOK */
.block-container {
    padding-left: 30px;
    padding-right: 30px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SESSION
# =========================
if "login" not in st.session_state:
    st.session_state.login = False

if "page" not in st.session_state:
    st.session_state.page = "login"

# =========================
# LOGOUT
# =========================
def logout():
    st.session_state.login = False
    st.session_state.page = "login"

# =========================
# LOGIN PAGE (CENTER LOGO + TITLE)
# =========================
if not st.session_state.login:

    st.markdown("<div class='center'>", unsafe_allow_html=True)

    # LOGO CENTER
    if os.path.exists("logo.png"):
        st.image("logo.png", width=150)
    else:
        st.write("🏫")

    # TITLE CENTER
    st.markdown("""
        <div class="title">
            SMKN 1 Denpasar
        </div>
    """, unsafe_allow_html=True)

    st.caption("Sistem Analisis Minat & Bakat Siswa")

    st.markdown("</div>", unsafe_allow_html=True)

    # =========================
    # LOGIN & REGISTER
    # =========================
    tab1, tab2 = st.tabs(["Login", "Daftar"])

    # LOGIN
    with tab1:
        st.subheader("Login")
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login"):
            # SIMULASI LOGIN (bisa diganti database)
            if email and password:
                st.session_state.login = True
                st.session_state.role = "guru"
                st.rerun()
            else:
                st.error("Isi email dan password")

    # REGISTER
    with tab2:
        st.subheader("Daftar")
        email2 = st.text_input("Email baru", key="reg_email")
        pass2 = st.text_input("Password baru", type="password", key="reg_pass")
        role = st.selectbox("Daftar sebagai", ["siswa", "guru"])

        if st.button("Daftar"):
            if email2 and pass2:
                st.success("Akun berhasil dibuat! Silakan login")
            else:
                st.warning("Lengkapi data")

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
        st.rerun()

st.divider()

# =========================
# DATA (SAFE DEMO)
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
# ANALISIS (SAFE)
# =========================
try:
    df["Logika"] = df.iloc[:, 0].apply(lambda x: 3)
    df["Kreatif"] = df.iloc[:, 0].apply(lambda x: 3)
    df["Teknik"] = df.iloc[:, 0].apply(lambda x: 3)
    df["Sosial"] = df.iloc[:, 0].apply(lambda x: 3)
    df["Skor"] = 3
except:
    df["Skor"] = 0

# =========================
# MENU
# =========================
menu = st.radio("Menu", ["Dashboard", "Data", "Ranking", "Settings"], horizontal=True)

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":
    st.subheader("📊 Dashboard")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Siswa", len(df))
    c2.metric("Rata-rata Skor", round(df["Skor"].mean(), 2))
    c3.metric("Status", "Aktif")

    st.bar_chart(df["Skor"])

# =========================
# DATA
# =========================
elif menu == "Data":
    st.subheader("📋 Data Siswa")
    st.dataframe(df)

# =========================
# RANKING
# =========================
elif menu == "Ranking":
    st.subheader("🏆 Ranking")
    st.dataframe(df.head(10))

# =========================
# SETTINGS
# =========================
elif menu == "Settings":
    st.subheader("⚙️ Settings")

    if st.button("Refresh"):
        st.rerun()

    st.download_button(
        "Download Data",
        df.to_csv(index=False),
        file_name="data.csv"
    )
