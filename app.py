import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
import nltk
nltk.download('stopwords')

# ===================== PAGE CONFIG =====================
st.set_page_config(
    page_title="Dashboard Big Data Roblox",
    page_icon="🎮",
    layout="wide"
)

# ===================== SESSION STATE MENU =====================
if "menu" not in st.session_state:
    st.session_state.menu = "Beranda"

# ===================== GLOBAL STYLE =====================
st.markdown("""
<style>
/* ----- CARD & SECTION ----- */
.section-box {
    padding:20px;
    border-radius:15px;
    background:rgba(255,255,255,0.05);
    transition:all 0.3s ease-in-out;
}
.section-box:hover {
    transform:translateY(-5px);
    box-shadow:0px 10px 25px rgba(0,0,0,0.15);
}

/* ----- NAV CARD BUTTON ----- */
.nav-card-btn button {
    width: 100%;
    height: 130px;
    border-radius: 20px;
    background: linear-gradient(135deg,#3b82f6,#6366f1);
    color: white;
    font-size: 18px;
    font-weight: 600;
    border: none;
    padding: 10px;
    transition: all 0.35s ease;
    box-shadow: 0 8px 20px rgba(0,0,0,0.15);
}

.nav-card-btn button:hover {
    transform: translateY(-6px) scale(1.05);
    box-shadow: 0 14px 30px rgba(0,0,0,0.25);
}

/* ===== NAV CARD CLICKABLE ===== */
.nav-card-btn button {
    all: unset;
    width: 100%;
    cursor: pointer;
}

.nav-card-btn button div {
    text-align:center;
    padding:20px;
    border-radius:15px;
    background:linear-gradient(135deg,#3b82f6,#6366f1);
    color:white;
    transition:all 0.3s ease;
}

.nav-card-btn button div:hover {
    transform:scale(1.05);
}

.nav-wrapper {
    position: relative;
}

.nav-wrapper button {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    opacity: 0;
    cursor: pointer;
}

/* ===== NAV CARD CLICKABLE FIX ===== */
.nav-card-wrapper {
    position: relative;
}

.nav-card-wrapper button {
    position: absolute;
    inset: 0;
    opacity: 0;
    cursor: pointer;
}

/* ----- METRIC ----- */
div[data-testid="metric-container"] {
    background:rgba(255,255,255,0.05);
    padding:15px;
    border-radius:15px;
    transition:transform 0.25s ease;
}
div[data-testid="metric-container"]:hover {
    transform:scale(1.05);
}

/* ----- SIDEBAR COLOR ----- */
section[data-testid="stSidebar"] {
    background: linear-gradient(135deg,#60a5fa,#a78bfa);
}
section[data-testid="stSidebar"] * {
    color: white !important;
}

/* ----- FIX MULTISELECT BACKGROUND ----- */
div[data-baseweb="select"] > div {
    background-color: rgba(255,255,255,0.15) !important;
}

/* ----- RESPONSIVE ----- */
@media (max-width: 768px) {
    h1 { font-size:26px !important; }
    h3 { font-size:18px !important; }
}
</style>
""", unsafe_allow_html=True)

# ===================== LOAD DATA =====================
df = pd.read_csv("roblox_reviews.csv")
logo = Image.open("roblox_logo.jpg")
wordcloud_img = Image.open("wordcloud.png")

# ===================== HEADER =====================
st.markdown("""
<div style="padding:30px;border-radius:20px;
background:linear-gradient(135deg,#60a5fa,#a78bfa);color:white;">
<h1>🎮 Big Data Analytics Dashboard</h1>
<h3>Analisis Sentimen Ulasan Game Roblox</h3>
<p>
Dashboard interaktif ini menyajikan hasil analisis Big Data terhadap ulasan pengguna
game Roblox dengan pendekatan data mining, machine learning, dan visual analytics.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ===================== SIDEBAR =====================
st.sidebar.markdown("## 🎮 Roblox Analytics")
st.sidebar.image(logo, width=150)

st.session_state.menu = st.sidebar.radio(
    "🧭 Navigasi",
    ["Beranda","Eksplorasi Dataset","Analisis Sentimen","Visualisasi & Insight"],
    index=["Beranda","Eksplorasi Dataset","Analisis Sentimen","Visualisasi & Insight"].index(st.session_state.menu)
)

st.sidebar.markdown("---")
st.sidebar.subheader("🔍 Filter Data")

sentiment_filter = st.sidebar.multiselect(
    "Sentimen",
    df["sentiment"].unique(),
    default=df["sentiment"].unique()
)

rating_filter = st.sidebar.slider(
    "Rentang Rating",
    int(df["rating"].min()),
    int(df["rating"].max()),
    (int(df["rating"].min()), int(df["rating"].max()))
)

filtered_df = df[
    (df["sentiment"].isin(sentiment_filter)) &
    (df["rating"] >= rating_filter[0]) &
    (df["rating"] <= rating_filter[1])
]

# ===================== BERANDA =====================
if st.session_state.menu == "Beranda":

    col1, col2 = st.columns([1,3])
    with col1:
        st.image(logo, width=180)
    with col2:
        st.info(
            "Dashboard ini merepresentasikan **analytical layer** dalam arsitektur Big Data. "
            "Seluruh data telah melalui proses pembersihan, feature engineering, "
            "dan analisis sentimen sebelum divisualisasikan."
        )

    st.subheader("📌 Ringkasan Cepat")
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Total Review", len(filtered_df))
    c2.metric("Rating Rata-rata", round(filtered_df["rating"].mean(),2))
    c3.metric("Sentimen Positif", len(filtered_df[filtered_df["sentiment"]=="Positive"]))
    c4.metric("Sentimen Negatif", len(filtered_df[filtered_df["sentiment"]=="Negative"]))

    st.markdown("### 🧭 Navigasi Cepat")

    n1, n2, n3, n4 = st.columns(4)

    with n1:
        st.markdown("""
        <div class="nav-card-wrapper">
            <div class="nav-card">
                🏠<br><b>Beranda</b><br>Overview sistem
            </div>
        """, unsafe_allow_html=True)
        if st.button("nav_beranda", key="nav_beranda"):
            st.session_state.menu = "Beranda"
        st.markdown("</div>", unsafe_allow_html=True)

    with n2:
        st.markdown("""
        <div class="nav-card-wrapper">
            <div class="nav-card">
                📋<br><b>Dataset</b><br>Data hasil cleaning
            </div>
        """, unsafe_allow_html=True)
        if st.button("nav_dataset", key="nav_dataset"):
            st.session_state.menu = "Eksplorasi Dataset"
        st.markdown("</div>", unsafe_allow_html=True)

    with n3:
        st.markdown("""
        <div class="nav-card-wrapper">
            <div class="nav-card">
                📊<br><b>Sentimen</b><br>Analisis opini
            </div>
        """, unsafe_allow_html=True)
        if st.button("nav_sentimen", key="nav_sentimen"):
            st.session_state.menu = "Analisis Sentimen"
        st.markdown("</div>", unsafe_allow_html=True)

    with n4:
        st.markdown("""
        <div class="nav-card-wrapper">
            <div class="nav-card">
                📈<br><b>Insight</b><br>Visual lanjutan
            </div>
        """, unsafe_allow_html=True)
        if st.button("nav_insight", key="nav_insight"):
            st.session_state.menu = "Visualisasi & Insight"
        st.markdown("</div>", unsafe_allow_html=True)


# ===================== DATASET =====================
elif st.session_state.menu == "Eksplorasi Dataset":
    st.subheader("📋 Dataset Review Roblox")

    with st.expander("📖 Penjelasan Dataset"):
        st.write(
            "Dataset ini merupakan hasil pengolahan ulasan pengguna Roblox. "
            "Data telah dibersihkan dari duplikasi, dilabeli sentimen berdasarkan rating, "
            "serta ditambahkan fitur `text_length` untuk analisis panjang ulasan."
        )

    st.dataframe(filtered_df, use_container_width=True)

# ===================== ANALISIS SENTIMEN =====================
elif st.session_state.menu == "Analisis Sentimen":

    tab1, tab2 = st.tabs(["📊 Distribusi Sentimen","⭐ Distribusi Rating"])

    with tab1:
        fig,ax = plt.subplots()
        sns.countplot(
            x="sentiment",
            data=filtered_df,
            palette={"Positive":"green","Neutral":"gold","Negative":"red"},
            ax=ax
        )
        st.pyplot(fig)

        with st.expander("📌 Lihat Insight Distribusi Sentimen"):
            st.write(
                "Grafik ini menunjukkan distribusi sentimen pengguna. Dominasi sentimen positif "
                "mengindikasikan tingkat kepuasan pengguna yang tinggi, sementara sentimen negatif "
                "merepresentasikan isu teknis seperti bug dan lag."
            )

    with tab2:
        fig2,ax2 = plt.subplots(figsize=(6,4))
        ax2.hist(filtered_df["rating"], bins=5, color="skyblue", edgecolor="black")
        st.pyplot(fig2)

        with st.expander("📌 Lihat Insight Distribusi Rating"):
            st.write(
                "Distribusi rating menunjukkan mayoritas pengguna memberikan nilai tinggi (4–5). "
                "Hal ini mencerminkan persepsi positif terhadap kualitas Roblox."
            )

# ===================== VISUALISASI & INSIGHT =====================
elif st.session_state.menu == "Visualisasi & Insight":

    tab1, tab2 = st.tabs(["☁️ Word Frequency","📦 Panjang Review"])

    with tab1:
        st.image(wordcloud_img, width=700)
        with st.expander("📌 Insight Word Frequency"):
            st.write(
                "Word cloud menampilkan kata yang paling sering muncul dalam ulasan pengguna. "
                "Kata berukuran besar menandakan topik dominan dalam pengalaman bermain."
            )

    with tab2:
        fig3,ax3 = plt.subplots(figsize=(6,4))
        sns.boxplot(
            x="sentiment",
            y="text_length",
            data=filtered_df,
            palette={"Positive":"lightgreen","Neutral":"khaki","Negative":"salmon"},
            ax=ax3
        )
        st.pyplot(fig3)

        with st.expander("📌 Insight Panjang Review"):
            st.write(
                "Ulasan negatif dan netral cenderung memiliki teks lebih panjang, "
                "menunjukkan pengguna memberikan penjelasan lebih detail saat menyampaikan keluhan."
            )