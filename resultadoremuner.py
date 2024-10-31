import streamlit as st
import pandas as pd

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
            width: 95%;
            max-width: 1800px;
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
            width: 95%;
            max-width: 1800px;
        }
        
        .stApp {
            background-color: #0A192F;
        }
        
        .dataframe {
            font-size: 16px !important;
            width: 100% !important;
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
            width: 95% !important;
            margin: 0 auto;
        }
        
        div[data-testid="stVerticalBlock"] > div {
            padding: 0;
        }
        
        .block-container {
            padding-top: 2rem !important;
            padding-bottom: 0rem !important;
            max-width: 100%;
        }
        
        section[data-testid="stSidebar"] {
            display: none;
        }
        
        [data-testid="stAppViewBlockContainer"] {
            padding-left: 0;
            padding-right: 0;
        }
        
        div.stMarkdown {
            width: 100% !important;
        }
        
        div.row-widget.stSelectbox {
            padding: 0;
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
    
    # Criar um DataFrame para exibição mantendo os valores originais para ordenação
    display_df = pd.DataFrame({
        'Empresa': filtered_df['Nome_Companhia'],
        'Remuneração Total': filtered_df['Total_Remuneracao'],
        '% Market Cap': filtered_df['% da Remuneração Total sobre o Market Cap'] * 100,
        '% EBITDA': filtered_df['% da Remuneração Total sobre o EBITDA'] * 100,
        '% Net Income': filtered_df['% da Remuneração Total sobre o Net Income LTM'] * 100
    })
    
    # Exibir tabela com colunas ordenáveis
    st.dataframe(
        display_df,
        hide_index=True,
        column_config={
            'Empresa': st.column_config.TextColumn(
                'Empresa'
            ),
            'Remuneração Total': st.column_config.NumberColumn(
                'Remuneração Total',
                format="R$ %,.2f"
            ),
            '% Market Cap': st.column_config.NumberColumn(
                '% Market Cap',
                format="%.2f%%"
            ),
            '% EBITDA': st.column_config.NumberColumn(
                '% EBITDA',
                format="%.2f%%"
            ),
            '% Net Income': st.column_config.NumberColumn(
                '% Net Income',
                format="%.2f%%"
            )
        },
        height=800,
        use_container_width=True
    )

if __name__ == "__main__":
    main()
