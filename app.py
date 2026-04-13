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

/* FULL CENTER LOGIN */
.center-screen {
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
    margin-top: 15px;
}

/* container */
.block-container {
    padding-left: 40px;
    padding-right: 40px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# USER SYSTEM
# =========================
USER_FILE = "users.csv"

if not os.path.exists(USER_FILE):
    pd.DataFrame(columns=["email", "password", "role"]).to_csv(USER_FILE, index=False)

def load_users():
    df = pd.read_csv(USER_FILE)
    if "role" not in df.columns:
        df["role"] = "siswa"
    return df

def save_user(email, password, role):
    users = load_users()
    new = pd.DataFrame([[email, password, role]], columns=["email", "password", "role"])
    users = pd.concat([users, new], ignore_index=True)
    users.to_csv(USER_FILE, index=False)

# =========================
# SESSION
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
if "role" not in st.session_state:
    st.session_state.role = None

# TARUH FUNGSI INI DI ATAS
def logout():
    st.session_state.login = False
    st.session_state.role = None
    st.rerun()
# =========================
# LOGIN PAGE
# =========================
if not st.session_state.login:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    
    # ... (Kodingan Logo & Judul kamu yang sudah rapi tadi) ...
    col_l1, col_l2, col_l3 = st.columns([1.5, 0.5, 1.5])
    with col_l2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
    
    st.markdown("<h2 style='text-align: center;'>SMKN 1 Denpasar</h2>", unsafe_allow_html=True)

    if st.button("Masuk Sebagai Guru (Demo)", use_container_width=True):
        st.session_state.login = True
        st.session_state.role = "guru" # Penting agar menu Data tidak error
        st.rerun()
    
    st.stop()
# =========================
# LOAD DATA
# =========================
url = "https://docs.google.com/spreadsheets/d/1wIMyXy5C0Q6TLUb09jJcKkTWQ830F_phjYtwOUthyX8/export?format=csv"
df = pd.read_csv(url)
df.columns = df.columns.str.strip()

# =========================
# ANALISIS
# =========================
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

def rekom(x):
    return max({
        "Informatika": x["Logika"],
        "DKV": x["Kreatif"],
        "Teknik": x["Teknik"],
        "Manajemen": x["Sosial"]
    }, key=lambda k: {
        "Informatika": x["Logika"],
        "DKV": x["Kreatif"],
        "Teknik": x["Teknik"],
        "Manajemen": x["Sosial"]
    }[k])

df["Rekomendasi"] = df.apply(rekom, axis=1)

# =========================
# MENU
# =========================
menu = st.radio(
    "Menu",
    ["Dashboard", "Data", "Ranking", "Settings"],
    horizontal=True
)

# =========================
# DASHBOARD
# =========================
with head1:
    st.title("🏫 Dashboard Utama")
    st.caption("Selamat datang di Sistem Analisis SMKN 1 Denpasar")

with head2:
    st.write(" ") # Kasih spasi dikit biar sejajar sama judul
    # TOMBOL LOGOUT DI SINI
    if st.button("🚪 Logout", use_container_width=True):
        logout()

st.divider()

if menu == "Dashboard":

    st.subheader("📊 Dashboard")

    col1, col2 = st.columns(2)
    jurusan = col1.selectbox("Filter Jurusan", ["Semua"] + list(df["Jurusan SMK"].dropna().unique()))
    search = col2.text_input("Cari Nama")

    temp = df.copy()

    if jurusan != "Semua":
        temp = temp[temp["Jurusan SMK"] == jurusan]

    if search:
        temp = temp[temp["Nama Lengkap"].str.contains(search, case=False, na=False)]

    st.metric("Total Siswa", len(temp))
    st.metric("Rata-rata Skor", round(temp["Skor"].mean(), 2))

    st.bar_chart(temp[["Logika", "Kreatif", "Teknik", "Sosial"]], use_container_width=True)

# =========================
# DATA
# =========================
elif menu == "Data":

    st.subheader("📋 Data Siswa")

    if st.session_state.role == "guru":
        st.dataframe(df, use_container_width=True)
    else:
        st.warning("Hanya guru yang bisa melihat data")

# =========================
# RANKING
# =========================
elif menu == "Ranking":

    st.subheader("🏆 Ranking")

    top = df.sort_values(by="Skor", ascending=False).head(10)
    st.dataframe(top, use_container_width=True)

# =========================
# SETTINGS
# =========================
elif menu == "Settings":

    st.subheader("⚙️ Settings")

    if st.button("Refresh Data"):
        st.rerun()

    st.download_button(
        "Download CSV",
        df.to_csv(index=False),
        file_name="data_siswa.csv"
    )
