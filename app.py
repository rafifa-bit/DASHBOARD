import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide") # Deixa o dashboard usar a largura total da página

# --- FUNÇÃO DE CARREGAMENTO COM CACHE ---
# Isso faz com que o Excel seja lido apenas uma vez, deixando o app muito mais rápido.
@st.cache_data
def load_data():
    df = pd.read_excel("SAGEP_PROCESSOS PAE3.xlsx", sheet_name="CONTROLE_ACOPANHAMENTO")
    
    # Limpeza básica de datas (apenas data de entrada)
    df["Dt. Entrada"] = pd.to_datetime(df["Dt. Entrada"], errors='coerce')
    df.dropna(subset=["Dt. Entrada"], inplace=True) # Remove linhas onde a data de entrada é inválida
    
    # Criação das colunas de Ano e Mês para os filtros
    df["Ano"] = df["Dt. Entrada"].dt.year
    df["Mês"] = df["Dt. Entrada"].dt.month_name() # ex: 'January', 'February'
    df["Ano"] = df["Ano"].astype(int)
    
    return df

df = load_data()

# -------------------------------
# Sidebar (Filtros)
# -------------------------------
st.sidebar.title("Filtros")
anos = st.sidebar.multiselect("Selecione o Ano", options=sorted(df["Ano"].unique()), default=sorted(df["Ano"].unique()))
status = st.sidebar.multiselect("Selecione o Status", options=df["STATUS"].unique(), default=df["STATUS"].unique())
municipios = st.sidebar.multiselect("Selecione o Município", options=df["MUNICÍPIO"].unique())

# --- LÓGICA DE FILTRO MELHORADA ---
df_filtrado = df.copy()
if anos:
    df_filtrado = df_filtrado[df_filtrado["Ano"].isin(anos)]
if status:
    df_filtrado = df_filtrado[df_filtrado["STATUS"].isin(status)]
if municipios:
    df_filtrado = df_filtrado[df_filtrado["MUNICÍPIO"].isin(municipios)]

# --- VERIFICAÇÃO DE DATAFRAME VAZIO ---
if df_filtrado.empty:
    st.warning("Nenhum processo encontrado para os filtros selecionados.")
    st.stop()

# -------------------------------
# KPIs (indicadores principais)
# -------------------------------
st.title("📊 Dashboard de Acompanhamento de Processos")

col1, col2, col3 = st.columns(3)
col1.metric("Total de Processos", df_filtrado["Protocolo"].nunique())
col2.metric("Municípios Atendidos", df_filtrado["MUNICÍPIO"].nunique())
col3.metric("Assuntos Diferentes", df_filtrado["Assunto"].nunique())

st.markdown("---") 

# -------------------------------
# Gráficos Gerais
# -------------------------------
st.header("📈 Visão Geral dos Processos")
col_graf1, col_graf2 = st.columns(2)

with col_graf1:
    # 1. Status
    fig2 = px.pie(df_filtrado, names="STATUS", title="Distribuição por Status", hole=.3)
    st.plotly_chart(fig2, use_container_width=True)

    # 2. Municípios
    top_municipios = df_filtrado["MUNICÍPIO"].value_counts().nlargest(10).reset_index()
    top_municipios.columns = ["Município", "Total"]
    fig3 = px.bar(top_municipios, x="Total", y="Município", title="Top 10 Municípios", orientation='h')
    st.plotly_chart(fig3, use_container_width=True)

with col_graf2:
    # 3. Evolução mensal (ORDENADO CORRETAMENTE)
    meses_ordenados = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
    df_filtrado['Mês'] = pd.Categorical(df_filtrado['Mês'], categories=meses_ordenados, ordered=True)
    processos_mes = df_filtrado.groupby("Mês")["Protocolo"].count().reset_index().sort_values("Mês")
    fig1 = px.line(processos_mes, x="Mês", y="Protocolo", title="Evolução Mensal de Processos", markers=True, labels={'Protocolo': 'Quantidade'})
    st.plotly_chart(fig1, use_container_width=True)

    # 4. Assuntos
    top_assuntos = df_filtrado["Assunto"].value_counts().nlargest(10).reset_index()
    top_assuntos.columns = ["Assunto", "Total"]
    fig4 = px.bar(top_assuntos, x="Total", y="Assunto", title="Top 10 Assuntos", orientation='h')
    st.plotly_chart(fig4, use_container_width=True)

st.markdown("---")
st.dataframe(df_filtrado) # Para ver a tabela de dados filtrados