import pandas as pd 
import streamlit as st
st.set_page_config(layout="wide")
@st.cache_data
def carregar_dados():
    try:
        dados = pd.read_csv("vendas.csv")
    except FileNotFoundError:
        st.error("Arquivo 'vendas.csv' não encontrado. Por favor, verifique o caminho do arquivo e tente novamente.")
        st.stop()

    colunas_necessarias = ["Produto", "Quantidade", "Valor Unitário", "Custo Unitário", "Estado", "Vendedor"]
    colunas_faltando = [col for col in colunas_necessarias if col not in dados.columns]

    if colunas_faltando:
        st.error(f"As seguintes colunas estão faltando no arquivo CSV: {', '.join(colunas_faltando)}. Por favor, verifique o arquivo e tente novamente.")
        st.stop()

    return dados

tabela = carregar_dados()

def formatar_moeda(valor):
    if valor >= 1_000_000:
        return f"R$ {valor/1_000_000:.1f}M"
    elif valor >= 1_000:
        return f"R$ {valor/1_000:.1f}K"  
    else:
        return f"R$ {valor:,.0f}" 

tabela ["Faturamento"] = (tabela["Quantidade"] * tabela["Valor Unitário"])

tabela ["Lucro"] = (tabela["Valor Unitário"] - tabela["Custo Unitário"]) * tabela["Quantidade"]  


#titulo do dashboard

st.title("Dashboard de Vendas")

#campo de seleção de produtos

produtos = st.sidebar.multiselect("Selecione os produtos", tabela["Produto"].unique())
estados = st.sidebar.multiselect("Selecione os estados", tabela["Estado"].unique())
vendedores = st.sidebar.multiselect("Selecione os vendedores", tabela["Vendedor"].unique())

tabela_selecionada = tabela

if produtos:
    tabela_selecionada = tabela_selecionada[tabela_selecionada["Produto"].isin(produtos)]

if estados:
    tabela_selecionada = tabela_selecionada[tabela_selecionada["Estado"].isin(estados)]

if vendedores:
    tabela_selecionada = tabela_selecionada[tabela_selecionada["Vendedor"].isin(vendedores)]

#botão de download dos dados filtrados

csv = tabela_selecionada.to_csv(index=False).encode("utf-8")

st.sidebar.download_button(
    label="Baixar dados filtrados (CSV)",
    data=csv,
    file_name="vendas_filtradas.csv",
    mime="text/csv"
)

#KPIs lado a lado

col1, col2, col3, col4 = st.columns(4)

#faturamento total
with col1:
    st.metric("Faturamento Total", formatar_moeda(tabela_selecionada['Faturamento'].sum()))

#Média de vendas 
with col2:
    st.metric("Média de Vendas", formatar_moeda(tabela_selecionada['Faturamento'].mean()))
#Lucro de total
with col3:
    st.metric("Lucro Total", formatar_moeda(tabela_selecionada['Lucro'].sum()))

#Margem de lucro

with col4:
    faturamento_total = tabela_selecionada['Faturamento'].sum()
    lucro_total = tabela_selecionada['Lucro'].sum()
    margem = (lucro_total / faturamento_total) * 100 if faturamento_total != 0 else 0
    st.metric("Margem de Lucro", f"{margem:.1f}%"
              )


#graficos organizados em abas

aba_produto, aba_estado, aba_vendedor = st.tabs(["Produto", "Estado", "Vendedor"])

#grafico de lucro por produto
with aba_produto:
    st.subheader("Lucro por Produto")
    st.bar_chart(tabela_selecionada.groupby("Produto")["Lucro"].sum())

#gráfico faturamento por produto
    st.subheader("Faturamento por Produto")
    st.bar_chart(tabela_selecionada.groupby("Produto")["Faturamento"].sum()) 

##gráfico faturamento por estado
with aba_estado:
    st.subheader("Faturamento por Estado")
    st.bar_chart(tabela_selecionada.groupby("Estado")["Faturamento"].sum()) 

#gráfico faturamento por vendedor
with aba_vendedor:
    st.subheader("Faturamento por Vendedor")
    st.bar_chart(tabela_selecionada.groupby("Vendedor")["Faturamento"].sum())

#tabela de dados detalhada

with st.expander("Ver dados detalhados"):
    st.dataframe(tabela_selecionada)
    