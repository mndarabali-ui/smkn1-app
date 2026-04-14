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
# STYLE
# =========================
st.markdown("""
<style>

/* Reset & Base */
.stApp {
    background-color: #f0f4f8;
}

/* Header terpusat */
.app-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    padding: 28px 0 20px;
    background-color: #ffffff;
    border-bottom: 1px solid #e2e8f0;
    margin-bottom: 24px;
}

.logo-circle {
    width: 72px;
    height: 72px;
    border-radius: 50%;
    background-color: #1a4fa0;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 28px;
    color: white;
    font-weight: 700;
    margin-bottom: 10px;
    border: 3px solid #dbeafe;
}

.school-title {
    font-size: 22px;
    font-weight: 700;
    color: #1e293b;
    text-align: center;
    margin: 0;
    letter-spacing: 0.02em;
}

.school-subtitle {
    font-size: 13px;
    color: #64748b;
    text-align: center;
    margin-top: 2px;
    letter-spacing: 0.04em;
}

/* Card metrik */
[data-testid="metric-container"] {
    background-color: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 20px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.04);
}

/* Tabel */
[data-testid="stDataFrame"] {
    border-radius: 12px;
    border: 1px solid #e2e8f0;
    overflow: hidden;
}

/* Tombol */
.stButton > button {
    background-color: #1a4fa0;
    color: white;
    border: none;
    border-radius: 8px;
    padding: 8px 24px;
    font-weight: 600;
    font-size: 14px;
    transition: background-color 0.2s;
}
.stButton > button:hover {
    background-color: #163d80;
}

/* Download button */
.stDownloadButton > button {
    background-color: #f1f5f9;
    color: #1a4fa0;
    border: 1px solid #bfdbfe;
    border-radius: 8px;
}

/* Blok konten utama */
.block-container {
    padding: 0 32px 32px 32px;
    max-width: 1200px;
}

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #1e293b;
}

/* Sembunyikan padding default streamlit di halaman login */
.login-wrap .block-container {
    padding-top: 0;
}

/* Badge rekomendasi */
.badge {
    display: inline-block;
    padding: 3px 12px;
    border-radius: 20px;
    font-size: 12px;
    font-weight: 600;
}
.badge-blue   { background: #dbeafe; color: #1a4fa0; }
.badge-green  { background: #dcfce7; color: #166534; }
.badge-orange { background: #ffedd5; color: #9a3412; }
.badge-pink   { background: #fce7f3; color: #9d174d; }

/* Divider */
hr {
    border: none;
    border-top: 1px solid #e2e8f0;
    margin: 16px 0;
}

</style>
""", unsafe_allow_html=True)

# =========================
# SISTEM PENGGUNA
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
# SESSION STATE
# =========================
if "login" not in st.session_state:
    st.session_state.login = False
if "role" not in st.session_state:
    st.session_state.role = ""
if "email" not in st.session_state:
    st.session_state.email = ""

# =========================
# HALAMAN LOGIN
# =========================
if not st.session_state.login:

    # Header terpusat dengan logo.png
    col_l, col_c, col_r = st.columns([1, 1.2, 1])
    with col_c:
        import base64
        logo_html = ""
        if os.path.exists("logo.png"):
            with open("logo.png", "rb") as f:
                b64 = base64.b64encode(f.read()).decode()
            logo_html = f'<img src="data:image/png;base64,{b64}" style="width:64px; height:64px; object-fit:contain; margin-bottom:8px;">'

        st.markdown(f"""
            <div style="display:flex; flex-direction:column; align-items:center; text-align:center; margin-bottom:16px;">
                {logo_html}
                <p class="school-title">SMKN 1 Denpasar</p>
                <p class="school-subtitle">Sistem Analisis Minat Siswa</p>
            </div>
        """, unsafe_allow_html=True)

        tab1, tab2 = st.tabs(["🔐 Masuk", "📝 Daftar"])

        with tab1:
            email_in = st.text_input("Alamat Email", placeholder="contoh@email.com", key="login_email")
            pass_in  = st.text_input("Password", type="password", placeholder="Masukkan password", key="login_pass")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Masuk", use_container_width=True):
                users = load_users()
                user = users[(users["email"] == email_in) & (users["password"] == pass_in)]
                if not user.empty:
                    st.session_state.login = True
                    st.session_state.role  = user.iloc[0]["role"]
                    st.session_state.email = email_in
                    st.rerun()
                else:
                    st.error("Email atau password salah. Silakan coba lagi.")

        with tab2:
            st.markdown("#### Buat Akun Baru")
            new_email = st.text_input("Alamat Email", placeholder="contoh@email.com", key="reg_email")
            new_pass  = st.text_input("Password", type="password", placeholder="Buat password", key="reg_pass")
            new_role  = st.selectbox("Daftar sebagai", ["siswa", "guru"], key="reg_role")
            st.markdown("<br>", unsafe_allow_html=True)

            if st.button("Buat Akun", use_container_width=True):
                users = load_users()
                if new_email in users["email"].values:
                    st.warning("Email ini sudah terdaftar. Silakan masuk.")
                elif not new_email or not new_pass:
                    st.warning("Harap isi semua kolom.")
                else:
                    save_user(new_email, new_pass, new_role)
                    st.success("✅ Akun berhasil dibuat! Silakan masuk.")

    st.stop()

# Header setelah login dengan logo.png
with st.container():
    import base64
    logo_html = ""
    if os.path.exists("logo.png"):
        with open("logo.png", "rb") as f:
            b64 = base64.b64encode(f.read()).decode()
        logo_html = f'<img src="data:image/png;base64,{b64}" style="width:60px; height:60px; object-fit:contain; margin-bottom:6px;">'

    st.markdown(f"""
        <div style="display:flex; flex-direction:column; align-items:center; text-align:center;
                    padding: 20px 0 16px; background:#ffffff;
                    border-bottom: 1px solid #e2e8f0; margin-bottom:16px;">
            {logo_html}
            <p class="school-title">SMKN 1 Denpasar</p>
            <p class="school-subtitle">Sistem Analisis Minat Siswa</p>
        </div>
    """, unsafe_allow_html=True)

# Info pengguna & logout di pojok kanan atas
col_info, col_logout = st.columns([6, 1])
with col_info:
    role_label = "Guru" if st.session_state.role == "guru" else "Siswa"
    st.markdown(
        f"<small style='color:#64748b;'>Masuk sebagai <strong>{st.session_state.email}</strong> "
        f"&nbsp;·&nbsp; <span style='color:#1a4fa0;'>{role_label}</span></small>",
        unsafe_allow_html=True
    )
with col_logout:
    if st.button("Keluar"):
        st.session_state.login = False
        st.session_state.role  = ""
        st.session_state.email = ""
        st.rerun()

st.markdown("<hr>", unsafe_allow_html=True)

# =========================
# NAVIGASI
# =========================
menu = st.radio(
    "",
    ["📊 Dashboard", "📋 Data Siswa", "🏆 Ranking", "⚙️ Pengaturan"],
    horizontal=True,
    label_visibility="collapsed"
)

st.markdown("<br>", unsafe_allow_html=True)

# =========================
# MUAT & ANALISIS DATA
# =========================
@st.cache_data(ttl=300)
def load_data():
    url = (
        "https://docs.google.com/spreadsheets/d/"
        "1wIMyXy5C0Q6TLUb09jJcKkTWQ830F_phjYtwOUthyX8/export?format=csv"
    )
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()

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

    kategori = {"Informatika": "Logika", "DKV": "Kreatif", "Teknik": "Teknik", "Manajemen": "Sosial"}

    def rekomendasi(row):
        return max(kategori, key=lambda k: row[kategori[k]])

    df["Rekomendasi"] = df.apply(rekomendasi, axis=1)
    return df

df = load_data()

# =========================
# DASHBOARD
# =========================
if menu == "📊 Dashboard":

    st.subheader("Ringkasan Data Siswa")

    col1, col2 = st.columns(2)
    with col1:
        jurusan_list = ["Semua"] + sorted(df["Jurusan SMK"].dropna().unique().tolist())
        jurusan = st.selectbox("Filter Jurusan", jurusan_list)
    with col2:
        search = st.text_input("Cari Nama Siswa", placeholder="Ketik nama...")

    # Filter
    temp = df.copy()
    if jurusan != "Semua":
        temp = temp[temp["Jurusan SMK"] == jurusan]
    if search:
        temp = temp[temp["Nama Lengkap"].str.contains(search, case=False, na=False)]

    st.markdown("<br>", unsafe_allow_html=True)

    # Metrik utama
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Total Siswa",    len(temp))
    m2.metric("Rata-rata Skor", round(temp["Skor"].mean(), 2))
    m3.metric("Skor Tertinggi", round(temp["Skor"].max(), 2))
    m4.metric("Skor Terendah",  round(temp["Skor"].min(), 2))

    st.markdown("<br>", unsafe_allow_html=True)

    # Grafik kompetensi
    st.markdown("**Distribusi Skor Kompetensi**")
    chart_data = temp[["Logika", "Kreatif", "Teknik", "Sosial"]].mean().reset_index()
    chart_data.columns = ["Kategori", "Rata-rata"]
    st.bar_chart(chart_data.set_index("Kategori"), use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Rekomendasi jurusan
    st.markdown("**Distribusi Rekomendasi Jurusan**")
    recom_counts = temp["Rekomendasi"].value_counts()
    recom_df = recom_counts.reset_index()
    recom_df.columns = ["Jurusan", "Jumlah Siswa"]
    recom_df["Persentase"] = (recom_df["Jumlah Siswa"] / len(temp) * 100).round(1).astype(str) + "%"
    st.dataframe(recom_df, use_container_width=True, hide_index=True)

# =========================
# DATA SISWA
# =========================
elif menu == "📋 Data Siswa":

    st.subheader("Data Lengkap Siswa")

    if st.session_state.role == "guru":
        kolom_tampil = ["Nama Lengkap", "Jurusan SMK", "Logika", "Kreatif", "Teknik", "Sosial", "Skor", "Rekomendasi"]
        kolom_ada    = [k for k in kolom_tampil if k in df.columns]
        st.dataframe(df[kolom_ada].round(2), use_container_width=True, hide_index=True)
    else:
        st.info("🔒 Akses terbatas. Hanya guru yang dapat melihat data lengkap siswa.")

# =========================
# RANKING
# =========================
elif menu == "🏆 Ranking":

    st.subheader("Peringkat 10 Siswa Terbaik")

    jumlah = st.slider("Tampilkan peringkat teratas", min_value=5, max_value=50, value=10, step=5)
    top    = df.sort_values(by="Skor", ascending=False).head(jumlah).reset_index(drop=True)
    top.index = top.index + 1

    kolom_rank = ["Nama Lengkap", "Jurusan SMK", "Skor", "Rekomendasi"]
    kolom_ada  = [k for k in kolom_rank if k in top.columns]
    st.dataframe(top[kolom_ada].round(2), use_container_width=True)

# =========================
# PENGATURAN
# =========================
elif menu == "⚙️ Pengaturan":

    st.subheader("Pengaturan Aplikasi")

    st.markdown("**Data**")
    col_r, col_d = st.columns([1, 1])

    with col_r:
        if st.button("🔄 Perbarui Data"):
            st.cache_data.clear()
            st.rerun()

    with col_d:
        st.download_button(
            label="⬇️ Unduh CSV",
            data=df.to_csv(index=False).encode("utf-8"),
            file_name="data_siswa_smkn1_denpasar.csv",
            mime="text/csv"
        )

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("**Informasi Akun**")
    st.markdown(f"- **Email:** {st.session_state.email}")
    st.markdown(f"- **Peran:** {'Guru' if st.session_state.role == 'guru' else 'Siswa'}")
    st.markdown(f"- **Total data:** {len(df)} siswa")
