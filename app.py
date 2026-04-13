import streamlit as st
import pandas as pd
import plotly.express as px
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
.stApp { background: #f5f7fb; }
.login-box {
    max-width: 420px;
    margin: auto;
    margin-top: 60px;
    background: white;
    padding: 25px;
    border-radius: 15px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
}
.login-header { text-align: center; margin-bottom: 20px; }
.title { font-size: 24px; font-weight: 700; margin-top: 10px; }
[data-testid="stImage"] { display: flex; justify-content: center; }
</style>
""", unsafe_allow_html=True)

if "login" not in st.session_state:
    st.session_state.login = False

def logout():
    st.session_state.login = False
    st.rerun()

# =========================
# LOGIN PAGE
# =========================
if not st.session_state.login:
    st.markdown("<div class='login-box'>", unsafe_allow_html=True)
    col_l1, col_l2, col_l3 = st.columns([1.3, 0.4, 1.3])
    with col_l2:
        if os.path.exists("logo.png"):
            st.image("logo.png", use_container_width=True)
        else:
            st.write("🏫")

    st.markdown("""
        <div class='login-header'>
            <div class='title'>SMKN 1 Denpasar</div>
            <div style='color: gray; font-size: 14px;'>Sistem Analisis Minat & Bakat Siswa</div>
        </div>
    """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Daftar"])
    with tab1:
        st.text_input("Email")
        st.text_input("Password", type="password")
        if st.button("Login", use_container_width=True):
            st.session_state.login = True
            st.rerun()
    with tab2:
        st.text_input("Email baru")
        st.text_input("Password baru", type="password")
        st.button("Daftar", use_container_width=True)

    st.markdown("</div>", unsafe_allow_html=True)
    st.stop()

# =========================
# DASHBOARD (KODE AWAL KAMU)
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

menu = st.radio("Menu", ["Dashboard", "Data", "Ranking", "Settings"], horizontal=True)

if menu == "Dashboard":
    st.subheader("📊 Dashboard")
    c1, c2, c3 = st.columns(3)
    c1.metric("Total Siswa", len(df))
    c2.metric("Rata-rata", 80)
    c3.metric("Status", "Aktif")
    
    # GRAFIK YANG LEBIH BAGUS (Plotly)
    st.write("### Grafik Analisis")
    # Mengambil kolom pertama sebagai contoh data
    fig = px.bar(df, 
                 x=df.index, 
                 y=df.columns[0], 
                 title="Distribusi Skor Siswa",
                 labels={'index': 'Siswa ke-', df.columns[0]: 'Skor'},
                 color_discrete_sequence=['#0078ff']) # Warna biru modern
    
    fig.update_layout(hovermode="x unified", template="plotly_white")
    st.plotly_chart(fig, use_container_width=True)

elif menu == "Data":
    st.subheader("📋 Data")
    st.dataframe(df, use_container_width=True)

elif menu == "Ranking":
    st.subheader("🏆 Ranking")
    st.dataframe(df.head(10))

elif menu == "Settings":
    st.subheader("⚙️ Settings")
    if st.button("Refresh"):
        st.rerun()
