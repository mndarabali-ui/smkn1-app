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

/* LOGIN BOX */
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
}

/* Memastikan Logo di Tengah Tanpa Container Tambahan */
.logo-container {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
    margin-bottom: 10px;
}

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
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)

    # PERBAIKAN: Hapus st.columns, ganti dengan div murni agar kotak kosong hilang
    st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)
    else:
        st.write("🏫")
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("""
        <div style='text-align: center;'>
            <div class='title'>SMKN 1 Denpasar</div>
            <div style='color: gray; font-size: 14px; margin-bottom: 20px;'>
                Sistem Analisis Minat & Bakat Siswa
            </div>
        </div>
    """, unsafe_allow_html=True)

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

# =========================
# DASHBOARD UTAMA
# =========================
head1, head2 = st.columns([8, 2])
with head1:
    st.title("🏫 Dashboard Utama")
    st.caption("Selamat datang di Sistem Analisis SMKN 1 Denpasar")

with head2:
    st.write("##") 
    if st.button("🚪 Logout", use_container_width=True):
        logout()

st.divider()

# LOAD DATA
url = "https://docs.google.com/spreadsheets/d/1wIMyXy5C0Q6TLUb09jJcKkTWQ830F_phjYtwOUthyX8/export?format=csv"
df = pd.read_csv(url)
df.columns = df.columns.str.strip()

# ANALISIS (Tetap Sama)
df["Logika"] = df[["Saya suka membuat program / coding", "Saya suka bekerja dengan angka / matematika", "Saya suka bekerja menggunakan komputer"]].mean(axis=1)
df["Kreatif"] = df[["Saya suka membuat desain visual (poster, video, UI)", "Saya suka menggambar / ilustrasi"]].mean(axis=1)
df["Teknik"] = df[["Saya suka memperbaiki mesin / kendaraan", "Saya suka bekerja dengan listrik / instalasi", "Saya suka merakit atau membongkar alat", "Saya suka bekerja di lapangan"]].mean(axis=1)
df["Sosial"] = df[["Saya suka berbicara di depan umum", "Saya suka bekerja dalam tim", "Saya suka memimpin atau mengatur orang lain"]].mean(axis=1)
df["Skor"] = df[["Logika", "Kreatif", "Teknik", "Sosial"]].mean(axis=1)

menu = st.radio("Menu", ["Dashboard", "Data", "Ranking", "Settings"], horizontal=True)

if menu == "Dashboard":
    st.subheader("📊 Dashboard")
    st.bar_chart(df[["Logika", "Kreatif", "Teknik", "Sosial"]])
elif menu == "Data":
    if st.session_state.role == "guru":
        st.dataframe(df)
elif menu == "Ranking":
    st.table(df.sort_values(by="Skor", ascending=False).head(10))
