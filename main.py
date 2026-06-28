import pandas as pd 
import streamlit as st

tabela = pd.read_csv("vendas.csv")

tabela ["Faturamento"] = (tabela["Quantidade"] * tabela["Valor Unitário"])

tabela ["Lucro"] = (tabela["Valor Unitário"] - tabela["Custo Unitário"]) * tabela["Quantidade"]  


#titulo do dashboard
st.title("Dashboard de Vendas")
#campo de seleção de produtos
produtos = st.multiselect("Selecione o produto", tabela["Produto"].unique())
if produtos:
    tabela_selecionada = tabela[tabela["Produto"].isin(produtos)]
else:
    tabela_selecionada = tabela

#faturamento total

st.metric("Faturamento Total", f"R$ {tabela_selecionada['Faturamento'].sum()}")

#Média de vendas 

st.metric("Média de vendas", f"R$ {tabela_selecionada['Faturamento'].mean()}")

#gráfico faturamento por produto

st.bar_chart(tabela_selecionada.groupby("Produto")["Faturamento"].sum()) 

#gráfico faturamento por categoria

st.bar_chart(tabela_selecionada.groupby("Estado")["Faturamento"].sum()) 

#gráfico faturamento por vendedor

st.bar_chart(tabela_selecionada.groupby("Vendedor")["Faturamento"].sum())