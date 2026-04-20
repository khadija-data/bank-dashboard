import streamlit as st
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from queries import get_risk_data

st.title("⚠️ Analyse des Risques")

df = get_risk_data()

# Scatter plot
fig = px.scatter(
    df,
    x="score_credit_client",
    y="montant",
    color="categorie_risque",
    title="Score vs Montant"
)

st.plotly_chart(fig)

st.markdown("---")

# Heatmap
corr = df[['score_credit_client', 'montant']].corr()

fig2, ax = plt.subplots()
sns.heatmap(corr, annot=True, cmap="coolwarm", ax=ax)

st.pyplot(fig2)

st.markdown("---")

# Top 10 clients à risque
df_risk = df.sort_values(by="score_credit_client").head(10)

st.subheader("Top 10 Clients à Risque")

st.dataframe(df_risk)