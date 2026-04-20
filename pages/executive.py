import streamlit as st
import plotly.express as px
from queries import get_kpis, get_time_series
from sqlalchemy import create_engine

st.title("📊 Vue Exécutive")

# KPIs
kpis = get_kpis()

col1, col2, col3, col4 = st.columns(4)

col1.metric("Transactions", kpis['total_transactions'][0])
col2.metric("CA Total", f"{kpis['total_ca'][0]:,.0f}")
col3.metric("Clients", kpis['clients_actifs'][0])
col4.metric("Marge Moyenne", f"{kpis['marge_moyenne'][0]:.2f}")

st.markdown("---")

# Graphique lignes
df = get_time_series()

fig = px.line(df, x="mois", y=["debit", "credit"],
              title="Évolution mensuelle")

st.plotly_chart(fig, use_container_width=True)
