import streamlit as st
import pandas as pd
import plotly.express as px

# Configuração da página
st.set_page_config(page_title="Dashboard PNAD Contínua", layout="wide")

# Estilo visual verde (igual ao exemplo do professor)
st.markdown("""
    <style>
    .main-title { font-size:32px !important; font-weight: bold; color: #1E5631; text-align: center; }
    .metric-box { background-color: #E8F5E9; padding: 15px; border-radius: 10px; border-left: 5px solid #2E7D32; text-align: center; }
    </style>
""", unsafe_allow_html=True)

# 1. Carregar os dados
@st.cache_data
def carregar_dados():
    df = pd.read_csv("BASE_FINAL_DIOGO_CORRIGIDA (1).csv")
    return df

try:
    df = carregar_dados()

    st.markdown("<p class='main-title'>📊 Dashboard Estatística Aplicada - PNAD Contínua</p>", unsafe_allow_html=True)
    
    # 2. Filtros na Barra Lateral
    st.sidebar.header("Filtros")
    lista_anos = sorted(df['Ano'].unique())
    ano_sel = st.sidebar.selectbox("Selecione o Ano", lista_anos)

    lista_trim = sorted(df['Trimestre'].unique())
    trim_sel = st.sidebar.selectbox("Selecione o Trimestre", lista_trim)

    # Filtrando os dados
    df_filtrado = df[(df['Ano'] == ano_sel) & (df['Trimestre'] == trim_sel)]

    # 3. Estatísticas Descritivas (Cards)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<div class='metric-box'>Total de Registros<br><h2>{len(df_filtrado):,}</h2></div>", unsafe_allow_html=True)
    with col2:
        st.markdown(f"<div class='metric-box'>Estados Pesquisados<br><h2>{df_filtrado['UF'].nunique()}</h2></div>", unsafe_allow_html=True)
    with col3:
        st.markdown(f"<div class='metric-box'>Período<br><h2>{trim_sel}º Trim / {ano_sel}</h2></div>", unsafe_allow_html=True)

    st.write("---")

    # 4. Gráfico de Barras (Distribuição por UF)
    st.subheader("Distribuição da Amostra por Código de UF")
    contagem = df_filtrado['UF'].value_counts().reset_index()
    contagem.columns = ['Código UF', 'Quantidade']
    
    fig = px.bar(contagem, x='Código UF', y='Quantidade', color_discrete_sequence=['#2E7D32'])
    st.plotly_chart(fig, use_container_width=True)

    # 5. Tabela de Dados
    st.subheader("Visualização dos Dados (Amostra)")
    st.dataframe(df_filtrado.head(50), use_container_width=True)

except Exception as e:
    st.error(f"Erro: Certifique-se de que o arquivo 'BASE_FINAL_DIOGO_CORRIGIDA (1).csv' está no GitHub.")