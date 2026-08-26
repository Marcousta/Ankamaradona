import streamlit as st
import numpy as np
from scipy.stats import poisson

st.set_page_config(page_title="Ankamaradona AI", page_icon="⚽")

st.title("⚽ ANKAMARADONA AI")
st.caption("İngiltere, İspanya, İtalya & Türkiye Ligi Tahmin Motoru")

LIGLER = {
    "İngiltere (Premier League)": {
        "Arsenal": {"xG": 2.10, "xGA": 0.85},
        "Manchester City": {"xG": 2.30, "xGA": 0.90},
        "Liverpool": {"xG": 2.05, "xGA": 1.00},
        "Chelsea": {"xG": 1.65, "xGA": 1.20},
        "Tottenham": {"xG": 1.80, "xGA": 1.35},
        "Manchester United": {"xG": 1.50, "xGA": 1.40},
        "Newcastle United": {"xG": 1.70, "xGA": 1.25},
        "Aston Villa": {"xG": 1.65, "xGA": 1.30},
        "Brighton": {"xG": 1.55, "xGA": 1.45},
        "West Ham": {"xG": 1.40, "xGA": 1.50},
        "Wolverhampton": {"xG": 1.20, "xGA": 1.55},
        "Fulham": {"xG": 1.30, "xGA": 1.45},
        "Bournemouth": {"xG": 1.35, "xGA": 1.60},
        "Brentford": {"xG": 1.40, "xGA": 1.50},
        "Everton": {"xG": 1.15, "xGA": 1.40},
        "Crystal Palace": {"xG": 1.25, "xGA": 1.35},
        "Nottingham Forest": {"xG": 1.20, "xGA": 1.50},
        "Leicester City": {"xG": 1.15, "xGA": 1.65},
        "Ipswich Town": {"xG": 1.05, "xGA": 1.75},
        "Southampton": {"xG": 1.00, "xGA": 1.80}
    },
    "İspanya (La Liga)": {
        "Real Madrid": {"xG": 2.15, "xGA": 0.80},
        "Barcelona": {"xG": 2.00, "xGA": 0.95},
        "Atletico Madrid": {"xG": 1.65, "xGA": 0.85},
        "Athletic Bilbao": {"xG": 1.55, "xGA": 1.10},
        "Real Sociedad": {"xG": 1.45, "xGA": 1.15},
        "Villarreal": {"xG": 1.60, "xGA": 1.40},
        "Girona": {"xG": 1.65, "xGA": 1.35},
        "Sevilla": {"xG": 1.35, "xGA": 1.40},
        "Real Betis": {"xG": 1.40, "xGA": 1.30},
        "Valencia": {"xG": 1.20, "xGA": 1.35},
        "Osasuna": {"xG": 1.25, "xGA": 1.30},
        "Getafe": {"xG": 1.05, "xGA": 1.15},
        "Celta Vigo": {"xG": 1.30, "xGA": 1.50},
        "Rayo Vallecano": {"xG": 1.15, "xGA": 1.35},
        "Mallorca": {"xG": 1.10, "xGA": 1.25},
        "Las Palmas": {"xG": 1.10, "xGA": 1.45},
        "Alaves": {"xG": 1.15, "xGA": 1.40},
        "Espanyol": {"xG": 1.05, "xGA": 1.55},
        "Leganes": {"xG": 0.95, "xGA": 1.45},
        "Valladolid": {"xG": 0.90, "xGA": 1.60}
    },
    "İtalya (Serie A)": {
        "Inter": {"xG": 2.10, "xGA": 0.80},
        "AC Milan": {"xG": 1.80, "xGA": 1.15},
        "Juventus": {"xG": 1.60, "xGA": 0.75},
        "Atalanta": {"xG": 1.90, "xGA": 1.20},
        "Napoli": {"xG": 1.70, "xGA": 1.05},
        "AS Roma": {"xG": 1.55, "xGA": 1.25},
        "Lazio": {"xG": 1.50, "xGA": 1.20},
        "Fiorentina": {"xG": 1.45, "xGA": 1.25},
        "Bologna": {"xG": 1.40, "xGA": 1.10},
        "Torino": {"xG": 1.20, "xGA": 1.20},
        "Udinese": {"xG": 1.25, "xGA": 1.35},
        "Genoa": {"xG": 1.15, "xGA": 1.30},
        "Monza": {"xG": 1.10, "xGA": 1.35},
        "Hellas Verona": {"xG": 1.10, "xGA": 1.50},
        "Cagliari": {"xG": 1.15, "xGA": 1.55},
        "Empoli": {"xG": 1.00, "xGA": 1.40},
        "Lecce": {"xG": 1.05, "xGA": 1.45},
        "Parma": {"xG": 1.20, "xGA": 1.60},
        "Como": {"xG": 1.15, "xGA": 1.65},
        "Venezia": {"xG": 1.00, "xGA": 1.70}
    },
    "Türkiye (Süper Lig)": {
        "Galatasaray": {"xG": 2.20, "xGA": 0.90},
        "Fenerbahçe": {"xG": 2.15, "xGA": 0.85},
        "Beşiktaş": {"xG": 1.80, "xGA": 1.10},
        "Trabzonspor": {"xG": 1.60, "xGA": 1.20},
        "Başakşehir": {"xG": 1.50, "xGA": 1.25},
        "Adana Demirspor": {"xG": 1.40, "xGA": 1.50},
        "Sivasspor": {"xG": 1.25, "xGA": 1.35},
        "Antalyaspor": {"xG": 1.30, "xGA": 1.40},
        "Alanyaspor": {"xG": 1.35, "xGA": 1.45},
        "Kasımpaşa": {"xG": 1.45, "xGA": 1.60},
        "Rizespor": {"xG": 1.30, "xGA": 1.50},
        "Kayserispor": {"xG": 1.20, "xGA": 1.45},
        "Göztepe": {"xG": 1.25, "xGA": 1.30},
        "Gaziantep FK": {"xG": 1.20, "xGA": 1.50},
        "Hatayspor": {"xG": 1.15, "xGA": 1.55},
        "Konyaspor": {"xG": 1.15, "xGA": 1.40},
        "Samsunspor": {"xG": 1.30, "xGA": 1.35},
        "Bodrum FK": {"xG": 1.00, "xGA": 1.45},
        "Eyüpspor": {"xG": 1.35, "xGA": 1.40}
    }
}

st.sidebar.header("🎯 Maç Seçimi")
lig = st.sidebar.selectbox("Lig Seçin", list(LIGLER.keys()))

takimlar = list(LIGLER[lig].keys())
ev_sahibi = st.sidebar.selectbox("Ev Sahibi", takimlar, index=0)

deplasman_liste = [t for t in takimlar if t != ev_sahibi]
deplasman = st.sidebar.selectbox("Deplasman", deplasman_liste, index=0)

def mac_tahmini_yap(ev, dep, lig_adi):
    ev_xg = LIGLER[lig_adi][ev]["xG"]
    ev_xga = LIGLER[lig_adi][ev]["xGA"]
    dep_xg = LIGLER[lig_adi][dep]["xG"]
    dep_xga = LIGLER[lig_adi][dep]["xGA"]
    
    ev_beklenen_gol = (ev_xg + dep_xga) / 2
    dep_beklenen_gol = (dep_xg + ev_xga) / 2
    
    max_gol = 6
    matris = np.zeros((max_gol, max_gol))
    
    for i in range(max_gol):
        for j in range(max_gol):
            matris[i, j] = poisson.pmf(i, ev_beklenen_gol) * poisson.pmf(j, dep_beklenen_gol)
            
    ev_kazanma = np.sum(np.tril(matris, -1)) * 100
    beraberlik = np.sum(np.diag(matris)) * 100
    dep_kazanma = np.sum(np.triu(matris, 1)) * 100
    
    return ev_kazanma, beraberlik, dep_kazanma, ev_beklenen_gol, dep_beklenen_gol

ev_p, ber_p, dep_p, ev_g, dep_g = mac_tahmini_yap(ev_sahibi, deplasman, lig)

st.subheader(f"📊 {ev_sahibi} vs {deplasman}")

col1, col2, col3 = st.columns(3)
col1.metric("Ev Sahibi (%)", f"{ev_p:.1f}%")
col2.metric("Beraberlik (%)", f"{ber_p:.1f}%")
col3.metric("Deplasman (%)", f"{dep_p:.1f}%")

st.markdown("---")
st.write(f"**Tahmini Gol Beklentisi (xG):** {ev_sahibi} **{ev_g:.2f}** - **{dep_g:.2f}** {deplasman}")
