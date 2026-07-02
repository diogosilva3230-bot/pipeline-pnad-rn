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
    # Carrega a base corrigida
    df = pd.read_csv("BASE_FINAL_DIOGO_CORRIGIDA (1).csv")
    return df

try:
    df = carregar_dados()

    # Título Principal
    st.markdown('<p class="main-title">📊 Dashboard Estatística Aplicada - PNAD Contínua</p>', unsafe_allow_html=True)
    st.write("---")

    # Barra Lateral - Filtros
    st.sidebar.header("Filtros")
    
    # Filtro de Ano
    anos_disponiveis = sorted(df['Ano'].unique())
    ano_selecionado = st.sidebar.selectbox("Selecione o Ano", anos_disponiveis, index=len(anos_disponiveis)-1)

    # Filtro de Trimestre
    trimestres_disponiveis = sorted(df['Trimestre'].unique())
    trimestre_selecionado = st.sidebar.selectbox("Selecione o Trimestre", trimestres_disponiveis, index=0)

    # Aplicar filtros
    df_filtrado = df[(df['Ano'] == ano_selecionado) & (df['Trimestre'] == trimestre_selecionado)]

    # 2. Indicadores (Cards)
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'<div class="metric-box"><p style="color:#555;margin:0;">Total de Registros</p><h2 style="color:#2E7D32;margin:0;">{len(df_filtrado):,}</h2></div>', unsafe_allow_html=True)
    
    with col2:
        total_ufs = df_filtrado['V0102'].nunique() if 'V0102' in df_filtrado.columns else 1
        st.markdown(f'<div class="metric-box"><p style="color:#555;margin:0;">Estados Pesquisados</p><h2 style="color:#2E7D32;margin:0;">{total_ufs}</h2></div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown(f'<div class="metric-box"><p style="color:#555;margin:0;">Período</p><h2 style="color:#2E7D32;margin:0;">{trimestre_selecionado}º Trim / {ano_selecionado}</h2></div>', unsafe_allow_html=True)

    st.write("---")

    # 3. Gráfico de Barras Ajustado (Mais Fino e Bonito)
    st.subheader("Distribuição da Amostra por Código de UF")
    
    # Contagem por UF
    df_uf = df_filtrado['V0102'].value_counts().reset_index()
    df_uf.columns = ['Código UF', 'Quantidade']
    df_uf['Código UF'] = df_uf['Código UF'].astype(str)

    # Criar o gráfico com largura definida para não esticar
    fig = px.bar(
        df_uf, 
        x='Código UF', 
        y='Quantidade',
        color_discrete_sequence=['#2E7D32'],
        width=350,  # Mantém a barra fina como no exemplo do IF!
        height=450
    )
    
    fig.update_layout(
        xaxis_title="Código UF",
        yaxis_title="Quantidade",
        bargap=0.2,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color="white")
    )
    
    # Centralizar o gráfico na tela usando colunas
    g_col1, g_col2, g_col3 = st.columns([1, 2, 1])
    with g_col2:
        st.plotly_chart(fig, use_container_width=False)

    st.write("---")

    # 4. Tabela de Amostra
    st.subheader("Visualização dos Dados (Amostra)")
    st.dataframe(df_filtrado.head(100), use_container_width=True)

except Exception as e:
    st.error(f"Erro ao carregar o dashboard: {e}")
