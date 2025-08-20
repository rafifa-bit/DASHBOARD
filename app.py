import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
file_path = "SAGEP_PROCESSOS PAE3.xlsx"
df = pd.read_excel(file_path, sheet_name="CONTROLE_ACOPANHAMENTO")

st.title("📊 Dashboard - Controle de Acompanhamento")

# ===============================
# Filtros interativos
# ===============================
st.sidebar.header("Filtros")

anos = df["Ano do protocolo"].dropna().unique()
ano_selecionado = st.sidebar.multiselect("Selecione o(s) Ano(s):", sorted(anos), default=sorted(anos))

status_unicos = df["Status Processo"].dropna().unique()
status_selecionado = st.sidebar.multiselect("Selecione o(s) Status:", sorted(status_unicos), default=sorted(status_unicos))

df_filtrado = df[
    (df["Ano do protocolo"].isin(ano_selecionado)) &
    (df["Status Processo"].isin(status_selecionado))
]

# ===============================
# KPIs principais
# ===============================
st.subheader("📌 Indicadores Gerais")
col1, col2, col3 = st.columns(3)

col1.metric("Total de Processos", len(df_filtrado))
col2.metric("Anos Selecionados", ", ".join(map(str, ano_selecionado)))
col3.metric("Status Selecionados", len(status_selecionado))

# ===============================
# Visualização 1: Protocolos por Ano
# ===============================
st.header("📈 Protocolos por Ano")

fig1 = px.histogram(df_filtrado, x="Ano do protocolo",
                    title="Distribuição de Protocolos por Ano",
                    labels={"Ano do protocolo": "Ano", "count": "Quantidade"})
st.plotly_chart(fig1, use_container_width=True)

# ===============================
# Visualização 2: Status dos Processos
# ===============================
st.header("📊 Status dos Processos")

status_count = df_filtrado["Status Processo"].value_counts().reset_index()
status_count.columns = ["Status", "Quantidade"]

fig2 = px.bar(status_count, x="Status", y="Quantidade", 
              title="Distribuição dos Status",
              labels={"Status": "Status do Processo", "Quantidade": "Nº de Processos"})
st.plotly_chart(fig2, use_container_width=True)

# ===============================
# NOVA VISUALIZAÇÃO - Protocolos
# ===============================
st.header("🔎 Análise de Protocolos")

protocolos_count = df_filtrado["Protocolo"].value_counts().reset_index()
protocolos_count.columns = ["Protocolo", "Quantidade"]

fig3 = px.bar(protocolos_count.head(20), 
             x="Protocolo", 
             y="Quantidade",
             title="Top 20 Protocolos mais recorrentes",
             labels={"Protocolo": "Número do Protocolo", "Quantidade": "Frequência"})

st.plotly_chart(fig3, use_container_width=True)

# ===============================
# Tabela detalhada
# ===============================
st.header("📋 Tabela de Processos Filtrados")
st.dataframe(df_filtrado[["Ano do protocolo", "Protocolo", "Mês da Entrada", "Dt. Entrada", "Status Processo"]])
