"""app/dashboard.py - Tableau de bord décisionnel IRVE."""

from pathlib import Path

import pandas as pd
import seaborn as sns
import streamlit as st

from src.indicators import (
    compute_kpis,
    compute_power_distribution,
    compute_temporal_evolution,
)

# Configuration de la page
st.set_page_config(
    page_title="SDIRVE Calvados - Tableau de Bord IRVE",
    page_icon="⚡",
    layout="wide",
)

sns.set_palette("cividis")


@st.cache_data
def load_data():
    """Charge les données traitées depuis data/processed/."""
    data_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "processed"
        / "irve_calvados.parquet"
    )
    if not data_path.exists():
        return None
    return pd.read_parquet(data_path)


df = load_data()

st.title("⚡ Bornes de recharge électrique : où financer les prochaines ?")
st.caption("Département du Calvados (14) | Source : data.gouv.fr & INSEE")
if df is None:
    st.info(
        "Données en attente : le fichier "
        "`data/processed/irve_calvados.parquet` n'a pas encore été généré."
    )
    st.stop()

# Utilisation des fonctions importées (supprime les erreurs F401)
kpis = compute_kpis(df)
df_evol = compute_temporal_evolution(df)
df_dist = compute_power_distribution(df)

# Affichage des métriques clés
col1, col2, col3, col4 = st.columns(4)
col1.metric("Points de charge (PDC)", f"{kpis['total_pdc']:,}")
col2.metric("Stations", f"{kpis['total_stations']:,}")
col3.metric("Part charge rapide (≥ 50 kW)", f"{kpis['part_rapide']:.1f} %")
col4.metric("PDC / 10 000 hab.", f"{kpis['ratio_10k']:.1f}")
