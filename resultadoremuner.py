import streamlit as st
import pandas as pd
from datetime import datetime, date

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
        return f"{float(value):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
    except:
        return "0,00"

def get_default_dates():
    """Retorna datas padrão seguras para o date_input"""
    start_date = date(2024, 1, 1)
    end_date = date(2024, 12, 31)
    return start_date, end_date

# Estilo CSS personalizado
st.markdown("""
    <style>
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
        
        .dataframe {
            font-size: 14px !important;
        }
        
        .filter-container {
            background-color: white;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 15px;
        }
        
        .stApp {
            background-color: #0A192F;
        }
        
        th {
            background-color: #f0f2f6;
            font-weight: bold !important;
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
        
        .stDateInput {
            background-color: white;
        }
    </style>
""", unsafe_allow_html=True)

def load_data():
    try:
        # Carregar dados do arquivo Excel
        df = pd.read_excel('remtotal2024_novo.xlsx')
        
        # Selecionar apenas as colunas desejadas
        selected_columns = [
            'Nome_Companhia',
            'Total_Remuneracao',
            '% da Remuneração Total sobre o Market Cap',
            '% da Remuneração Total sobre o EBITDA',
            '% da Remuneração Total sobre o Net Income LTM'
        ]
        
        # Verificar se todas as colunas existem no DataFrame
        for col in selected_columns:
            if col not in df.columns:
                st.error(f"Coluna {col} não encontrada no arquivo")
                return pd.DataFrame()
                
        return df[selected_columns]
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
    
    # Linha de filtros
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        empresas = st.selectbox(
            'Empresas',
            options=['Todas as empresas'] + sorted(df['Nome_Companhia'].dropna().unique().tolist())
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        default_start, default_end = get_default_dates()
        date_range = st.date_input(
            'Período',
            value=(default_start, default_end)
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Aplicar filtros
    filtered_df = df.copy()
    
    if empresas != 'Todas as empresas':
        filtered_df = filtered_df[filtered_df['Nome_Companhia'] == empresas]
    
    # Formatar as colunas
    display_df = filtered_df.copy()
    display_df['Total_Remuneracao'] = display_df['Total_Remuneracao'].apply(format_currency)
    display_df['% da Remuneração Total sobre o Market Cap'] = display_df['% da Remuneração Total sobre o Market Cap'].apply(format_number)
    display_df['% da Remuneração Total sobre o EBITDA'] = display_df['% da Remuneração Total sobre o EBITDA'].apply(format_number)
    display_df['% da Remuneração Total sobre o Net Income LTM'] = display_df['% da Remuneração Total sobre o Net Income LTM'].apply(format_number)
    
    # Exibir tabela
    st.dataframe(
        display_df,
        hide_index=True,
        column_config={
            'Nome_Companhia': 'Empresa',
            'Total_Remuneracao': 'Remuneração Total',
            '% da Remuneração Total sobre o Market Cap': '% Market Cap',
            '% da Remuneração Total sobre o EBITDA': '% EBITDA',
            '% da Remuneração Total sobre o Net Income LTM': '% Net Income'
        },
        height=600
    )

if __name__ == "__main__":
    main()
