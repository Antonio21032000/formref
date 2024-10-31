import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(layout="wide", page_title="BR Insider Analysis")

# Cores personalizadas
BG_COLOR = '#102F46'  # Azul escuro para o fundo
TITLE_BG_COLOR = '#DAA657'  # Dourado para o fundo do título
TITLE_TEXT_COLOR = 'white'  # Branco para o texto do título
TEXT_COLOR = '#333333'  # Cor principal do texto

# CSS personalizado
st.markdown(f"""
    <style>
    .reportview-container .main .block-container{{
        max-width: 1200px;
        padding-top: 0;
        padding-bottom: 0;
        padding-left: 0;
        padding-right: 0;
    }}
    .stApp {{
        background-color: {BG_COLOR};
    }}
    .stButton>button {{
        color: {TITLE_BG_COLOR};
        background-color: white;
        border-radius: 5px;
        font-weight: bold;
        border: none;
        padding: 0.5rem 1rem;
        transition: background-color 0.3s;
    }}
    .stButton>button:hover {{
        background-color: #f0f0f0;
    }}
    .stSelectbox, .stMultiSelect {{
        background-color: white;
        border-radius: 5px;
        color: {TEXT_COLOR};
    }}
    .title-container {{
        background-color: {TITLE_BG_COLOR};
        padding: 1rem;
        border-radius: 10px;
        margin-bottom: 2rem;
    }}
    .title-container h1 {{
        color: {TITLE_TEXT_COLOR};
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 0;
    }}
    .stDateInput>div>div>input {{
        color: {TEXT_COLOR};
        background-color: white;
        border-radius: 5px;
    }}
    .stDataFrame {{
        background-color: white;
        border-radius: 10px;
        overflow: hidden;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }}
    .stDataFrame table {{
        color: {TEXT_COLOR} !important;
    }}
    .stDataFrame th {{
        background-color: {TITLE_BG_COLOR} !important;
        color: {TITLE_TEXT_COLOR} !important;
        padding: 0.5rem !important;
    }}
    .stDataFrame td {{
        background-color: white !important;
        padding: 0.5rem !important;
    }}
    .stDataFrame tr:nth-of-type(even) {{
        background-color: #f8f8f8 !important;
    }}
    [data-testid="stHeader"] {{
        display: none;
    }}
    .block-container {{
        padding-top: 0 !important;
        padding-bottom: 0 !important;
    }}
    header {{
        display: none !important;
    }}
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
        
        df['Total_Remuneracao'] = pd.to_numeric(df['Total_Remuneracao'], errors='coerce')
        
        return df[selected_columns]
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

def main():
    # Título
    st.markdown('<div class="title-container"><h1>BR Insider Analysis</h1></div>', unsafe_allow_html=True)
    
    # Filtros em 3 colunas
    col1, col2, col3 = st.columns(3)
    
    with col1:
        empresas = st.selectbox(
            'Empresas',
            options=['Choose an option'] + ['Todas as empresas']
        )
        
    with col2:
        data_range = st.text_input(
            'Período',
            value='2024/01/01 - 2024/09/01'
        )
        
    with col3:
        tipo_mov = st.selectbox(
            'Tipo de Movimentação',
            options=['Choose an option']
        )

    # Carregar dados
    df = load_data()
    
    if df.empty:
        st.warning("Não foi possível carregar os dados.")
        return
    
    # Criar DataFrame para exibição
    display_df = pd.DataFrame({
        'Empresa': df['Nome_Companhia'],
        'Remuneração Total': df['Total_Remuneracao'],
        '% Market Cap': df['% da Remuneração Total sobre o Market Cap'] * 100,
        '% EBITDA': df['% da Remuneração Total sobre o EBITDA'] * 100,
        '% Net Income': df['% da Remuneração Total sobre o Net Income LTM'] * 100
    })

    # Botão de download
    st.download_button(
        label="📥 Baixar dados",
        data=b"placeholder",
        file_name="dados_empresas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )

    # Exibir tabela
    st.dataframe(
        display_df,
        hide_index=True,
        column_config={
            'Empresa': 'Empresa',
            'Remuneração Total': st.column_config.NumberColumn(
                'Remuneração Total',
                help='Remuneração total em reais',
                format="%d"
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
        height=600,
        use_container_width=True
    )

if __name__ == "__main__":
    main()
