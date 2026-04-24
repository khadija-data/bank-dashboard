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
#KPIs en cartes : Volume total transactions, CA total, Nombre de clients actifs, Marge moyenne

import streamlit as st
import pandas as pd
import matplotlib as plt

df = pd.read_csv('financecore_clean (3).csv')
df['date_transaction'] = pd.to_datetime(df['date_transaction'])

volume_total = df['montant_eur'].abs().sum()
ca_total = df[df['montant_eur'] > 0]['montant_eur'].sum()
clients_actifs = df['client_id'].nunique()
marge_moyenne = df['montant_eur'].abs().mean()

st.set_page_config(page_title="Executive View", layout="wide")
st.title(" Tableau de Bord : Vue Exécutive")

col1, col2, col3, col4 = st.columns(4)
col1.metric("Volume Total", f"{volume_total:,.0f} ")
col2.metric("CA Total", f"{ca_total:,.0f} ")
col3.metric("Clients Actifs", f"{clients_actifs}")
col4.metric("Marge Moyenne", f"{marge_moyenne:,.2f} ")

import plotly.graph_objects as go

df['date_transaction'] = pd.to_datetime(df['date_transaction'])

df['credit'] = df['montant_eur'].apply(lambda x: x if x > 0 else 0)
df['debit'] = df['montant_eur'].apply(lambda x: abs(x) if x < 0 else 0)

df_temp = df.copy()
df_temp['mois_annee'] = df_temp['date_transaction'].dt.to_period('M').astype(str)
df_evolution = df_temp.groupby('mois_annee')[['credit', 'debit']].sum().reset_index()

df_evolution = df_evolution.sort_values('mois_annee')


#Graphique lignes : évolution mensuelle des débits et crédits (2022–2024)
st.subheader(" Évolution mensuelle des débits et crédits (2022–2024)")

fig = go.Figure()
fig.add_trace(go.Scatter(
    x=df_evolution['mois_annee'], 
    y=df_evolution['credit'],
    mode='lines+markers',
    name='Crédits',
    line=dict(color="#a09937", width=3)
))

fig.add_trace(go.Scatter(
    x=df_evolution['mois_annee'], 
    y=df_evolution['debit'],
    mode='lines+markers',
    name='Débits',
    line=dict(color="#e73cc2", width=3)
))

fig.update_layout(
    xaxis_title="Mois",
    yaxis_title="Montant (EUR)",
    legend_title="Type Flux",
    hovermode="x unified",
    margin=dict(l=20, r=20, t=30, b=20),
    height=450
)
st.plotly_chart(fig, use_container_width=True)


#Graphique barres : CA par agence et par produit bancaire
import plotly.express as px
df['credit'] = df['montant_eur'].apply(lambda x: x if x > 0 else 0)
df_ca_agence_produit = df.groupby(['agence', 'produit'])['credit'].sum().reset_index()
df_ca_agence_produit = df_ca_agence_produit.sort_values(by='credit', ascending=False)

st.subheader(" Répartition du CA par agence et par produit bancaire")

fig_bar = px.bar(
    df_ca_agence_produit, 
    x='agence', 
    y='credit', 
    color='produit',  
    barmode='group', 
    text='credit',   
    title="CA par Agence et Produit (EUR)",
    height=500
)


fig_bar.update_traces(
    texttemplate='%{text:,.2s} €',
    textposition='outside'          
)

fig_bar.update_layout(
    xaxis_title="Agence",
    yaxis_title="CA Total (EUR)",
    legend_title="Type Produit",
    uniformtext=dict(minsize=8, mode='hide'), 
    margin=dict(l=20, r=20, t=50, b=20)
)

st.plotly_chart(fig_bar, use_container_width=True)


#Diagramme circulaire : répartition des clients par segment (Premium / Standard / Risqué)
import plotly.express as px
df_clients_segment = df.groupby('segment_client')['client_id'].nunique().reset_index()
df_clients_segment.columns = ['segment_client', 'nombre_clients']
df_clients_segment['pourcentage'] = (df_clients_segment['nombre_clients'] / df_clients_segment['nombre_clients'].sum()) * 100

st.subheader(" Répartition des clients par segment (Premium / Standard / Risqué)")

fig_pie = px.pie(
    df_clients_segment, 
    values='nombre_clients', 
    names='segment_client',
    hole=0.4,           
    title="Répartition des Clients",
    height=450
)

fig_pie.update_traces(
    textposition='outside',  
    textinfo='percent+label',            
    insidetextorientation='radial',   
    pull=[0.05, 0.05, 0.05]    
)
st.plotly_chart(fig_pie, use_container_width=True)


#Page 2 — Analyse des Risques
#Heatmap : corrélation entre score crédit, montant et taux de rejet

import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st

st.title(" Analyse des Risques et Conformité")
df_risk = df[['score_credit_client', 'montant_eur', 'is_anomaly']].copy()
df_risk['is_anomaly'] = df_risk['is_anomaly'].astype(int)
corr_matrix = df_risk.corr()
st.subheader("Heatmap : Corrélation entre Risques et Transactions")

fig, ax = plt.subplots(figsize=(8, 6))
sns.heatmap(
    corr_matrix, 
    annot=True,     
    cmap='RdYlGn',   
    fmt=".2f",      
    linewidths=0.5, 
    ax=ax
)
st.pyplot(fig)


#Scatter plot : score crédit vs montant transaction, coloré par catégorie de risque
import plotly.express as px
import streamlit as st

st.subheader("Score Crédit vs Montant (par catégorie de risque)")
fig = px.scatter(
    df,
    x="score_credit_client",
    y="montant_eur",
    color="is_anomaly",  
    hover_data=["score_credit_client", "montant_eur"],
    title="Relation entre Score Crédit et Montant"
)
st.plotly_chart(fig, use_container_width=True)


#Tableau des 10 clients les plus à risque avec indicateurs visuels colorés

st.subheader("Tableau des 10 clients les plus à risque")

df_risk = df.copy()

df_risk["risk_score"] = (
    (1 - df_risk["score_credit_client"] / df_risk["score_credit_client"].max()) * 0.5
    + df_risk["is_anomaly"] * 0.5
)

top10 = df_risk.sort_values("risk_score", ascending=False).head(10)

st.dataframe(
    top10.style.background_gradient(subset=["risk_score"], cmap="RdYlGn"),
    use_container_width=True
)


#Filtres Interactifs
#Sidebar avec filtres : Agence, Segment client, Produit, Période (slider années)

import streamlit as st
import pandas as pd

st.sidebar.title("Filtres")

agence = st.sidebar.multiselect(
    "Agence",
    options=df["agence"].unique(),
    default=df["agence"].unique()
)
segment = st.sidebar.multiselect(
    "Segment client",
    options=df["segment_client"].unique(),
    default=df["segment_client"].unique()
)
produit = st.sidebar.multiselect(
    "Produit bancaire",
    options=df["produit"].unique(),
    default=df["produit"].unique()
)
year_min = int(df["annee"].min())
year_max = int(df["annee"].max())

annees = st.sidebar.slider(
    "Période (annee)",
    min_value=year_min,
    max_value=year_max,
    value=(year_min, year_max)
)
df_filtered = df[
    (df["agence"].isin(agence)) &
    (df["segment_client"].isin(segment)) &
    (df["produit"].isin(produit)) &
    (df["annee"].between(annees[0], annees[1]))
]
st.write(f"Données filtrées : {len(df_filtered)} lignes")



st.subheader("Évolution des Transactions")

evolution = df_filtered.groupby("annee")["montant_eur"].sum().reset_index()

fig4 = px.line(
    evolution,
    x="annee",
    y="montant_eur",
    markers=True
)
st.plotly_chart(fig4, use_container_width=True)


#Bouton d'export CSV des données filtrées

import streamlit as st

st.subheader("Export des données filtrées")

csv = df_filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    label="⬇️ Télécharger CSV",
    data=csv,
    file_name="donnees_filtrees.csv",
    mime="text/csv"
)
