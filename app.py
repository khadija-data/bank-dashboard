import streamlit as st

st.set_page_config(page_title="Finance Dashboard", layout="wide")

st.title("📊 FinanceCore Dashboard")

# Sidebar filtres
st.sidebar.header("Filtres")

agence = st.sidebar.selectbox("Agence", ["Toutes", "A1", "A2"])
segment = st.sidebar.selectbox("Segment", ["Tous", "Premium", "Standard", "Risqué"])

# 
st.session_state.agence = agence
st.session_state.segment = segment

st.sidebar.markdown("---")
st.sidebar.info("Dashboard FinanceCore")

st.write("👈 Choisir une page dans le menu à gauche")