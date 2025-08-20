import streamlit as st
import pandas as pd
import plotly.express as px

# Carregar os dados
df = pd.read_excel("SAGEP_PROCESSOS PAE3.xlsx", sheet_name="CONTROLE_ACOPANHAMENTO")

# 🔹 Limpeza básica
df["Dt. Entrada"] = pd.to_datetime(df["Dt. Entrada"], errors="coerce")
df["Ano"] = df["Dt. Entrada"].dt.year
df["Mês"] = df["Dt. Entrada"].dt.month_name()

# -------------------------------
# Sidebar (Filtros)
# -------------------------------
st.sidebar.title("Filtros")
anos = st.sidebar.multiselect("Selecione o Ano", options=df["Ano"].dropna().unique(), default=df["Ano"].dropna().unique())
status = st.sidebar.multiselect("Selecione o Status", options=df["STATUS"].dropna().unique(), default=df["STATUS"].dropna().unique())
municipios = st.sidebar.multiselect("Selecione o Município", options=df["MUNICÍPIO"].dropna().unique())

# Aplicar filtros
df_filtrado = df[df["Ano"].isin(anos)]
if status:
    df_filtrado = df_filtrado[df_filtrado["STATUS"].isin(status)]
if municipios:
    df_filtrado = df_filtrado[df_filtrado["MUNICÍPIO"].isin(municipios)]

# -------------------------------
# KPIs (indicadores principais)
# -------------------------------
st.title("📊 Dashboard de Acompanhamento de Processos")

col1, col2, col3 = st.columns(3)
col1.metric("Total de Processos", df_filtrado["Protocolo"].nunique())
col2.metric("Municípios Atendidos", df_filtrado["MUNICÍPIO"].nunique())
col3.metric("Assuntos Diferentes", df_filtrado["Assunto"].nunique())

# -------------------------------
# Gráficos
# -------------------------------

# 1. Evolução mensal
processos_mes = df_filtrado.groupby("Mês")["Protocolo"].count().reset_index()
fig1 = px.bar(processos_mes, x="Mês", y="Protocolo", title="Processos por Mês")
st.plotly_chart(fig1)

# 2. Status
fig2 = px.pie(df_filtrado, names="STATUS", title="Distribuição por Status")
st.plotly_chart(fig2)

# 3. Municípios
top_municipios = df_filtrado["MUNICÍPIO"].value_counts().nlargest(10).reset_index()
top_municipios.columns = ["Município", "Total"]
fig3 = px.bar(top_municipios, x="Município", y="Total", title="Top 10 Municípios")
st.plotly_chart(fig3)

# 4. Assuntos
top_assuntos = df_filtrado["Assunto"].value_counts().nlargest(10).reset_index()
top_assuntos.columns = ["Assunto", "Total"]
fig4 = px.bar(top_assuntos, x="Assunto", y="Total", title="Top 10 Assuntos")
st.plotly_chart(fig4)
