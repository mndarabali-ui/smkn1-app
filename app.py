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
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    min-height: 100vh;
}

/* FULL CENTER LOGIN */
.center-screen {
    position: relative;
    width: 100%;
    display: flex;
    justify-content: center;
    align-items: center;
    flex-direction: column;
    text-align: center;
    padding-top: 40px;
    padding-bottom: 30px;
}

/* LOGO CONTAINER */
.logo-container {
    background: white;
    border-radius: 50%;
    width: 140px;
    height: 140px;
    display: flex;
    align-items: center;
    justify-content: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.2);
    margin-bottom: 20px;
}

.logo-container img {
    width: 120px;
    height: 120px;
}

/* TITLE */
.title {
    font-size: 36px;
    font-weight: 900;
    margin-top: 20px;
    color: white;
    text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
    letter-spacing: 1px;
}

.subtitle {
    font-size: 14px;
    color: #e0e0e0;
    margin-top: 8px;
    font-weight: 300;
}

/* container */
.block-container {
    padding-left: 40px;
    padding-right: 40px;
}

/* LOGIN FORM CONTAINER */
.login-container {
    background: white;
    border-radius: 15px;
    padding: 40px;
    box-shadow: 0 20px 60px rgba(0, 0, 0, 0.3);
    max-width: 420px;
    margin: 30px auto;
    width: 100%;
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

if "page" not in st.session_state:
    st.session_state.page = "Dashboard"

# =========================
# LOGIN PAGE (CENTER FULL)
# =========================
if not st.session_state.login:

    st.markdown("<div class='center-screen'>", unsafe_allow_html=True)

    # LOGO CENTER - With improved styling
    st.markdown("<div class='logo-container'>", unsafe_allow_html=True)
    if os.path.exists("logo.png"):
        st.image("logo.png", width=120, use_container_width=False)
    else:
        # SVG Logo Default
        st.markdown("""
        <svg width="120" height="120" viewBox="0 0 120 120" xmlns="http://www.w3.org/2000/svg">
            <!-- School Building Shape -->
            <circle cx="60" cy="50" r="35" fill="#667eea" opacity="0.2"/>
            <path d="M 40 80 L 40 40 L 60 30 L 80 40 L 80 80" stroke="#667eea" stroke-width="2.5" fill="none" stroke-linecap="round" stroke-linejoin="round"/>
            <!-- Roof -->
            <polygon points="40,40 60,25 80,40" fill="#764ba2" stroke="#764ba2" stroke-width="2"/>
            <!-- Door -->
            <rect x="54" y="56" width="12" height="24" fill="#764ba2" stroke="#764ba2" stroke-width="1.5" rx="2"/>
            <!-- Windows -->
            <rect x="43" y="45" width="8" height="8" fill="#667eea" stroke="#667eea" stroke-width="1.5" rx="1"/>
            <rect x="69" y="45" width="8" height="8" fill="#667eea" stroke="#667eea" stroke-width="1.5" rx="1"/>
            <rect x="43" y="60" width="8" height="8" fill="#667eea" stroke="#667eea" stroke-width="1.5" rx="1"/>
            <rect x="69" y="60" width="8" height="8" fill="#667eea" stroke="#667eea" stroke-width="1.5" rx="1"/>
            <!-- Flag on roof -->
            <line x1="60" y1="25" x2="60" y2="15" stroke="#764ba2" stroke-width="2"/>
            <polygon points="62,15 62,19 68,17" fill="#e74c3c"/>
        </svg>
        """, unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    # TITLE
    st.markdown("""
        <div class="title">
            SMKN 1 Denpasar
        </div>
        <div class="subtitle">
            Sekolah Menengah Kejuruan Negeri 1 Denpasar
        </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # LOGIN / REGISTER - In container
    st.markdown("<div class='login-container'>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Daftar"])

    with tab1:
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            users = load_users()
            user = users[(users["email"] == email) & (users["password"] == password)]

            if not user.empty:
                st.session_state.login = True
                st.session_state.role = user.iloc[0]["role"]
                st.rerun()
            else:
                st.error("Login gagal")

    with tab2:
        email = st.text_input("Email baru")
        password = st.text_input("Password baru", type="password")
        role = st.selectbox("Daftar sebagai", ["siswa", "guru"])

        if st.button("Daftar"):
            users = load_users()

            if email in users["email"].values:
                st.warning("Email sudah terdaftar")
            else:
                save_user(email, password, role)
                st.success("Akun berhasil dibuat!")

    st.markdown("</div>", unsafe_allow_html=True)
    
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
st.markdown("""
    <div class="title" style="margin-bottom: 10px;">
        SMKN 1 Denpasar
    </div>
""", unsafe_allow_html=True)
menu = st.radio(
    "",
    ["Dashboard", "Data", "Ranking", "Settings"],
    horizontal=True
)

# =========================
# DASHBOARD
# =========================
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
