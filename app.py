import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
file_path = "SAGEP_PROCESSOS PAE3.xlsx"
df = pd.read_excel(file_path, sheet_name="CONTROLE_ACOPANHAMENTO")

st.title("📊 Dashboard - Controle de Acompanhamento")

# ===============================
# Visualização 1: Distribuição dos Protocolos
# ===============================
st.header("Distribuição de Protocolos")

protocolos_count = df["Protocolo"].value_counts().reset_index()
protocolos_count.columns = ["Protocolo", "Quantidade"]

fig = px.bar(protocolos_count.head(20), 
             x="Protocolo", 
             y="Quantidade",
             title="Top 20 Protocolos mais recorrentes",
             labels={"Protocolo": "Número do Protocolo", "Quantidade": "Frequência"})

st.plotly_chart(fig, use_container_width=True)

# ===============================
# Visualização 2: Protocolos por Ano
# ===============================
st.header("Protocolos por Ano")

if "Ano do protocolo" in df.columns:
    fig2 = px.histogram(df, x="Ano do protocolo",
                        title="Protocolos por Ano",
                        labels={"Ano do protocolo": "Ano", "count": "Quantidade"})
    st.plotly_chart(fig2, use_container_width=True)

# ===============================
# Tabela detalhada
# ===============================
st.header("📋 Tabela de Protocolos")
st.dataframe(df[["Ano do protocolo", "Protocolo", "Mês da Entrada", "Dt. Entrada"]])
