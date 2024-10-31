import streamlit as st
import pandas as pd
import numpy as np

# Configuração da página
st.set_page_config(page_title="BR Insider Analysis", layout="wide", initial_sidebar_state="collapsed")

# Funções de formatação
def format_currency(value):
    try:
        return f"R$ {float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "R$ 0,00"

def format_number(value):
    try:
        if pd.isna(value):
            return "N/A"
        return f"{float(value):.2f}%".replace(".", ",")
    except:
        return "N/A"

# Estilo CSS personalizado
st.markdown("""
    <style>
        .title-container {
            background-color: #DEB887;
            padding: 20px;
            border-radius: 10px;
            margin: 0 auto 30px auto;
            text-align: center;
            width: 90%;
            max-width: 1400px;
        }
        .title-text {
            color: white;
            font-size: 32px;
            font-weight: bold;
            margin: 0;
        }
        
        .filter-container {
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 0 auto 25px auto;
            width: 90%;
            max-width: 1400px;
        }
        
        .stApp {
            background-color: #0A192F;
        }
        
        .dataframe {
            font-size: 16px !important;
        }
        
        th {
            background-color: #f0f2f6 !important;
            font-weight: bold !important;
            font-size: 16px !important;
            padding: 15px !important;
            text-align: center !important;
        }
        
        td {
            padding: 12px !important;
            text-align: right !important;
        }
        
        td:first-child {
            text-align: left !important;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9;
        }
        
        tr:nth-child(odd) {
            background-color: white;
        }
        
        .stSelectbox {
            background-color: white;
        }
        
        [data-testid="stDataFrame"] {
            width: 90% !important;
            margin: 0 auto !important;
            max-width: 1400px !important;
        }
        
        div[data-testid="stVerticalBlock"] > div {
            padding: 0;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        
        .block-container {
            padding: 3rem 1rem !important;
            max-width: 1400px !important;
        }
        
        section[data-testid="stSidebar"] {
            display: none;
        }
    </style>
""", unsafe_allow_html=True)

def load_data():
    try:
        df = pd.read_excel('remtotal2024_novo.xlsx')
        
        selected_columns = [
            'Nome_Companhia',
            'Total_Remuneracao',
            '% da Remuneração Total sobre o Market Cap',
            '% da Remuneração Total sobre o EBITDA',
            '% da Remuneração Total sobre o Net Income LTM'
        ]
        
        df = df[selected_columns]
        
        # Converter colunas para tipo numérico
        numeric_columns = selected_columns[1:]  # Todas exceto Nome_Companhia
        for col in numeric_columns:
            df[col] = pd.to_numeric(df[col], errors='coerce')
                
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

def main():
    # Título personalizado
    st.markdown("""
        <div class="title-container">
            <h1 class="title-text">BR Insider Analysis</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data()
    
    if df.empty:
        st.warning("Não foi possível carregar os dados.")
        return
    
    # Filtro de empresas centralizado
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    empresas = st.selectbox(
        'Empresas',
        options=['Todas as empresas'] + sorted(df['Nome_Companhia'].dropna().unique().tolist())
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if empresas != 'Todas as empresas':
        filtered_df = filtered_df[filtered_df['Nome_Companhia'] == empresas]
    
    # Formatar as colunas para exibição
    display_df = filtered_df.copy()
    display_df = display_df.style.format({
        'Total_Remuneracao': lambda x: format_currency(x),
        '% da Remuneração Total sobre o Market Cap': lambda x: format_number(x),
        '% da Remuneração Total sobre o EBITDA': lambda x: format_number(x),
        '% da Remuneração Total sobre o Net Income LTM': lambda x: format_number(x)
    })
    
    # Exibir tabela
    st.dataframe(
        display_df,
        column_config={
            'Nome_Companhia': 'Empresa',
            'Total_Remuneracao': 'Remuneração Total',
            '% da Remuneração Total sobre o Market Cap': '% Market Cap',
            '% da Remuneração Total sobre o EBITDA': '% EBITDA',
            '% da Remuneração Total sobre o Net Income LTM': '% Net Income'
        },
        hide_index=True,
        height=800,
        use_container_width=False
    )

if __name__ == "__main__":
    main()
