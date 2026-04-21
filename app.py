import streamlit as st
import pandas as pd
import os

# =========================
# KONFIGURASI
# =========================
st.set_page_config(
    page_title="SMKN 1 Denpasar",
    page_icon="🏫",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# =========================
# STYLE (FIXED)
# =========================
st.markdown("""
<style>
.stApp {
    background-color: #f0f4f8;
}

.app-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 20px;
    background-color: white;
    border-bottom: 1px solid #e2e8f0;
}

.school-title {
    font-size: 22px;
    font-weight: bold;
    color: #1e293b;
}

.school-subtitle {
    font-size: 13px;
    color: #64748b;
}

.stButton > button {
    background-color: #1a4fa0;
    color: white;
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

# =========================
# FILE USER
# =========================
USER_FILE = "users.csv"

if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["email", "password", "role"]).to_csv(USER_FILE, index=False)

def load_users():
    df = pd.read_csv(USER_FILE)
    df.columns = df.columns.str.strip()

    df["email"] = df["email"].astype(str).str.strip().str.lower()
    df["password"] = df["password"].astype(str).str.strip()

    if "role" not in df.columns:
        df["role"] = "siswa"

    return df

def save_user(email, password, role):
    users = load_users()

    new = pd.DataFrame([[
        email.strip().lower(),
        password.strip(),
        role
    ]], columns=["email", "password", "role"])

    users = pd.concat([users, new], ignore_index=True)
    users.to_csv(USER_FILE, index=False)

# =========================
# SESSION
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
if "role" not in st.session_state:
    st.session_state.role = ""
if "email" not in st.session_state:
    st.session_state.email = ""

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.login:

    st.markdown("""
    <div class="app-header">
        <div class="school-title">SMKN 1 Denpasar</div>
        <div class="school-subtitle">Sistem Analisis Minat Siswa</div>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])

    # LOGIN
    with tab1:
        email_in = st.text_input("Email")
        pass_in = st.text_input("Password", type="password")

        if st.button("Masuk"):
            users = load_users()

            email_in = email_in.strip().lower()
            pass_in = pass_in.strip()

            user = users[
                (users["email"] == email_in) &
                (users["password"] == pass_in)
            ]

            if not user.empty:
                st.session_state.login = True
                st.session_state.role = user.iloc[0]["role"]
                st.session_state.email = email_in
                st.success("Login berhasil!")
                st.rerun()
            else:
                st.error("Email atau password salah!")

    # REGISTER
    with tab2:
        new_email = st.text_input("Email Baru")
        new_pass = st.text_input("Password Baru", type="password")
        new_role = st.selectbox("Role", ["siswa", "guru"])

        if st.button("Daftar"):
            users = load_users()

            if new_email.strip().lower() in users["email"].values:
                st.warning("Email sudah terdaftar!")
            elif not new_email or not new_pass:
                st.warning("Isi semua data!")
            else:
                save_user(new_email, new_pass, new_role)
                st.success("Akun berhasil dibuat!")

    st.stop()

# =========================
# HEADER
# =========================
st.markdown(f"""
<div class="app-header">
    <div class="school-title">SMKN 1 Denpasar</div>
    <div class="school-subtitle">Login sebagai: {st.session_state.email}</div>
</div>
""", unsafe_allow_html=True)

if st.button("Logout"):
    st.session_state.login = False
    st.rerun()

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    url = "https://docs.google.com/spreadsheets/d/1wIMyXy5C0Q6TLUb09jJcKkTWQ830F_phjYtwOUthyX8/export?format=csv"
    df = pd.read_csv(url)

    df["Logika"] = df[[
        "Saya suka membuat program / coding",
        "Saya suka bekerja dengan angka / matematika",
        "Saya suka bekerja menggunakan komputer"
    ]].mean(axis=1)

    df["Kreatif"] = df[[
        "Saya suka membuat desain visual (poster, video, UI)",
        "Saya suka menggambar / ilustrasi"
    ]].mean(axis=1)

    df["Teknik"] = df[[
        "Saya suka memperbaiki mesin / kendaraan",
        "Saya suka bekerja dengan listrik / instalasi",
        "Saya suka merakit atau membongkar alat",
        "Saya suka bekerja di lapangan"
    ]].mean(axis=1)

    df["Sosial"] = df[[
        "Saya suka berbicara di depan umum",
        "Saya suka bekerja dalam tim",
        "Saya suka memimpin atau mengatur orang lain"
    ]].mean(axis=1)

    df["Skor"] = df[["Logika", "Kreatif", "Teknik", "Sosial"]].mean(axis=1)

    kategori = {
        "Informatika": "Logika",
        "DKV": "Kreatif",
        "Teknik": "Teknik",
        "Manajemen": "Sosial"
    }

    df["Rekomendasi"] = df.apply(
        lambda row: max(kategori, key=lambda k: row[kategori[k]]),
        axis=1
    )

    return df

df = load_data()

# =========================
# MENU
# =========================
menu = st.radio("", ["Dashboard", "Ranking"])

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":
    st.subheader("Dashboard")

    st.metric("Total Siswa", len(df))
    st.metric("Rata-rata", round(df["Skor"].mean(), 2))

    st.bar_chart(df[["Logika", "Kreatif", "Teknik", "Sosial"]].mean())

# =========================
# RANKING
# =========================
if menu == "Ranking":
    st.subheader("Top Siswa")

    top = df.sort_values(by="Skor", ascending=False).head(10)
    st.dataframe(top[["Nama Lengkap", "Skor", "Rekomendasi"]])
