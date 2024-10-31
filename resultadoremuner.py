import streamlit as st
import pandas as pd
from datetime import datetime
import numpy as np

# Configuração da página
st.set_page_config(page_title="BR Insider Analysis", layout="wide")

# Funções de formatação
def format_currency(value):
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def format_number(value):
    try:
        return f"{float(value):,.0f}".replace(",", ".")
    except:
        return "0"

# Estilo CSS personalizado
st.markdown("""
    <style>
        /* Título principal */
        .title-container {
            background-color: #DEB887;
            padding: 20px;
            border-radius: 10px;
            margin-bottom: 20px;
            text-align: center;
        }
        .title-text {
            color: white;
            font-size: 32px;
            font-weight: bold;
            margin: 0;
        }
        
        /* Estilização da tabela */
        .dataframe {
            font-size: 14px !important;
        }
        
        /* Containers dos filtros */
        .filter-container {
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        
        /* Estilo do fundo da página */
        .stApp {
            background-color: #0A192F;
        }
        
        /* Estilização dos headers da tabela */
        th {
            background-color: #f0f2f6;
            font-weight: bold !important;
        }
        
        /* Alternar cores das linhas */
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        tr:nth-child(odd) {
            background-color: white;
        }
        
        /* Ajustes nos selects */
        .stSelectbox {
            background-color: white;
        }
        
        /* Ajustes na data */
        .stDateInput {
            background-color: white;
        }
    </style>
""", unsafe_allow_html=True)

def load_data():
    try:
        # Carregar dados do arquivo Excel
        df = pd.read_excel('remtotal2024_novo.xlsx')
        required_columns = [
            'Data_Referencia', 'Empresa', 'Tipo_Cargo', 'Tipo_Movimentacao',
            'Tipo_Ativo', 'Caracteristica_Valor_Mobiliario', 'Data_Movimentacao',
            'Quantidade', 'Preco_Unitario', 'Volume_Financeiro'
        ]
        
        # Verificar se todas as colunas necessárias existem
        for col in required_columns:
            if col not in df.columns:
                df[col] = None
                
        return df[required_columns]
    
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        # Retornar DataFrame vazio com as colunas necessárias
        return pd.DataFrame(columns=required_columns)

def main():
    # Título personalizado
    st.markdown("""
        <div class="title-container">
            <h1 class="title-text">BR Insider Analysis</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data()
    
    # Converter colunas de data
    date_columns = ['Data_Referencia', 'Data_Movimentacao']
    for col in date_columns:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Linha de filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        empresas = st.selectbox(
            'Empresas',
            options=['Todas as empresas'] + sorted(df['Empresa'].unique().tolist())
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        date_range = st.date_input(
            'Período',
            value=(
                df['Data_Movimentacao'].min().date() if not df['Data_Movimentacao'].empty else datetime.now().date(),
                df['Data_Movimentacao'].max().date() if not df['Data_Movimentacao'].empty else datetime.now().date()
            )
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        tipo_mov = st.selectbox(
            'Tipo de Movimentação',
            options=['Todos os tipos'] + sorted(df['Tipo_Movimentacao'].unique().tolist())
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if empresas != 'Todas as empresas':
        filtered_df = filtered_df[filtered_df['Empresa'] == empresas]
    
    if tipo_mov != 'Todos os tipos':
        filtered_df = filtered_df[filtered_df['Tipo_Movimentacao'] == tipo_mov]
    
    filtered_df = filtered_df[
        (filtered_df['Data_Movimentacao'].dt.date >= date_range[0]) &
        (filtered_df['Data_Movimentacao'].dt.date <= date_range[1])
    ]
    
    # Formatar dados para exibição
    display_df = filtered_df.copy()
    display_df['Data_Referencia'] = display_df['Data_Referencia'].dt.strftime('%Y-%m-%d')
    display_df['Data_Movimentacao'] = display_df['Data_Movimentacao'].dt.strftime('%Y-%m-%d')
    display_df['Quantidade'] = display_df['Quantidade'].apply(format_number)
    display_df['Preco_Unitario'] = display_df['Preco_Unitario'].apply(format_currency)
    display_df['Volume_Financeiro'] = display_df['Volume_Financeiro'].apply(format_currency)
    
    # Exibir tabela com estilo
    st.dataframe(
        display_df,
        hide_index=True,
        column_config={
            'Data_Referencia': 'Data Referência',
            'Empresa': 'Empresa',
            'Tipo_Cargo': 'Tipo Cargo',
            'Tipo_Movimentacao': 'Tipo Movimentação',
            'Tipo_Ativo': 'Tipo Ativo',
            'Caracteristica_Valor_Mobiliario': 'Característica Valor Mobiliário',
            'Data_Movimentacao': 'Data Movimentação',
            'Quantidade': 'Quantidade',
            'Preco_Unitario': 'Preço Unitário',
            'Volume_Financeiro': 'Volume Financeiro (R$)'
        },
        height=600
    )

if __name__ == "__main__":
    main()
