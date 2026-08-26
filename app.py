import streamlit as st
import numpy as np
from scipy.stats import poisson

st.set_page_config(page_title="Ankamaradona AI", page_icon="⚽", layout="centered")

st.title("⚽ ANKAMARADONA AI")
st.caption("İngiltere, İspanya, İtalya & Türkiye Ligi Tahmin Motoru")

LIGLER = {
    "İngiltere (Premier League)": {
        "Arsenal": {"xG": 2.10, "xGA": 0.85},
        "Manchester City": {"xG": 2.30, "xGA": 0.90},
        "Liverpool": {"xG": 2.05, "xGA": 1.00},
        "Chelsea": {"xG": 1.65, "xGA": 1.25}
    },
    "İspanya (La Liga)": {
        "Real Madrid": {"xG": 2.15, "xGA": 0.80},
        "Barcelona": {"xG": 2.00, "xGA": 0.95},
        "Atletico Madrid": {"xG": 1.60, "xGA": 0.75}
    },
    "İtalya (Serie A)": {
        "Inter": {"xG": 1.95, "xGA": 0.70},
        "Juventus": {"xG": 1.55, "xGA": 0.80},
        "AC Milan": {"xG": 1.70, "xGA": 1.10}
    },
    "Türkiye (Süper Lig)": {
        "Galatasaray": {"xG": 2.20, "xGA": 0.90},
        "Fenerbahçe": {"xG": 2.10, "xGA": 0.85},
        "Beşiktaş": {"xG": 1.75, "xGA": 1.15}
    }
}

st.sidebar.header("🎯 Maç Seçimi")
secilen_lig = st.sidebar.selectbox("Lig Seçin", list(LIGLER.keys()))

takimlar = list(LIGLER[secilen_lig].keys())
ev_takim = st.sidebar.selectbox("Ev Sahibi", takimlar, index=0)
dep_takim = st.sidebar.selectbox("Deplasman", takimlar, index=1 if len(takimlar) > 1 else 0)

def hesapla_olasiliklar(ev_xg, dep_xg):
    max_gol = 6
    matris = np.zeros((max_gol, max_gol))
    for i in range(max_gol):
        for j in range(max_gol):
            matris[i, j] = poisson.pmf(i, ev_xg) * poisson.pmf(j, dep_xg)
            
    ev_win = np.sum(np.tril(matris, -1)) * 100
    draw = np.sum(np.diag(matris)) * 100
    dep_win = np.sum(np.triu(matris, 1)) * 100
    return round(ev_win, 1), round(draw, 1), round(dep_win, 1), matris

if ev_takim == dep_takim:
    st.warning("Lütfen farklı iki takım seçin kanka!")
else:
    ev_data = LIGLER[secilen_lig][ev_takim]
    dep_data = LIGLER[secilen_lig][dep_takim]
    
    ev_beklenen = (ev_data["xG"] + dep_data["xGA"]) / 2
    dep_beklenen = (dep_data["xG"] + ev_data["xGA"]) / 2
    
    ev_p, draw_p, dep_p, matris = hesapla_olasiliklar(ev_beklenen, dep_beklenen)
    
    st.subheader(f"📊 {ev_takim} vs {dep_takim}")
    
    col1, col2, col3 = st.columns(3)
    col1.metric("Ev Sahibi (%)", f"{ev_p}%")
    col2.metric("Beraberlik (%)", f"{draw_p}%")
    col3.metric("Deplasman (%)", f"{dep_p}%")
    
    st.markdown("---")
    st.subheader("🎯 En Olası Skorlar")
    
    skorlar = []
    for i in range(4):
        for j in range(4):
            skorlar.append((i, j, round(matris[i, j] * 100, 1)))
            
    skorlar.sort(key=lambda x: x[2], reverse=True)
    
    for s in skorlar[:3]:
        st.write(f"• **Skor {s[0]} - {s[1]}** :  %{s[2]} ihtimal")
