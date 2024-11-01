import streamlit as st
import pandas as pd
import io

# Configuração da página
st.set_page_config(layout="wide", page_title="Compensation Analysis")

# Cores personalizadas
BG_COLOR = '#102F46'  # Azul escuro para o fundo
TITLE_BG_COLOR = '#DAA657'  # Dourado para o fundo do título
TITLE_TEXT_COLOR = 'white'  # Branco para o texto do título
TEXT_COLOR = '#333333'  # Cor principal do texto

# CSS personalizado com suporte a modo tela cheia
def get_css(fullscreen=False):
    base_css = f"""
    .reportview-container .main .block-container{{
        max-width: {'' if fullscreen else '1200px'};
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
        {f'display: none;' if fullscreen else ''}
    }}
    .title-container h1 {{
        color: {TITLE_TEXT_COLOR};
        font-size: 2.5rem;
        font-weight: bold;
        text-align: center;
        margin: 0;
    }}
    .controls-container {{
        {f'display: none;' if fullscreen else ''}
        margin-bottom: 1rem;
    }}
    .stDateInput>div>div>input {{
        color: {TEXT_COLOR};
        background-color: white;
        border-radius: 5px;
    }}
    .stDataFrame {{
        background-color: white;
        border-radius: {'' if fullscreen else '10px'};
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
        position: sticky;
        top: 0;
        z-index: 1;
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
        padding-top: {'' if fullscreen else '0'} !important;
        padding-bottom: {'' if fullscreen else '0'} !important;
        max-width: {'' if fullscreen else '1200px'} !important;
    }}
    header {{
        display: none !important;
    }}
    {'''
    /* Estilo para modo tela cheia */
    .element-container:has(div.stDataFrame) {
        position: fixed;
        left: 0;
        top: 0;
        width: 100vw;
        height: 100vh;
        z-index: 1000;
        background: white;
        padding: 0 !important;
    }
    .stDataFrame {
        height: 100vh !important;
    }
    ''' if fullscreen else ''}
    """
    return base_css

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
        
        # Filtrando o DataFrame
        df = df[selected_columns]
        df = df[df['% da Remuneração Total sobre o Market Cap'].notna()]  # Remove linhas com NaN em Market Cap
        df = df[df['Nome_Companhia'] != 'GAFISA S.A.']  # Remove GAFISA S.A.
        df = df[df['Nome_Companhia'] != 'MOVIDA LOCAÇÃO DE VEÍCULOS S.A.']  # Remove MOVIDA
        
        return df
    except Exception as e:
        st.error(f"Erro ao carregar dados: {str(e)}")
        return pd.DataFrame()

def convert_df_to_excel(df):
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        df.to_excel(writer, sheet_name='Dados', index=False)
    output.seek(0)
    return output.getvalue()

def main():
    # Inicializar o estado de tela cheia
    if 'fullscreen' not in st.session_state:
        st.session_state.fullscreen = False
    
    # Aplicar CSS com base no estado de tela cheia
    st.markdown(f'<style>{get_css(st.session_state.fullscreen)}</style>', unsafe_allow_html=True)
    
    # Título
    st.markdown('<div class="title-container"><h1>Compensation Analysis</h1></div>', unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data()
    
    if df.empty:
        st.warning("Não foi possível carregar os dados.")
        return
    
    # Container para controles
    with st.container():
        st.markdown('<div class="controls-container">', unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 4])
        
        with col1:
            # Filtro único de empresas
            empresas = st.selectbox(
                'Empresas',
                options=['Todas as empresas'] + sorted(df['Nome_Companhia'].unique().tolist())
            )
        
        with col2:
            # Botão de download
            excel_data = convert_df_to_excel(df)
            st.download_button(
                label="📥 Baixar dados",
                data=excel_data,
                file_name="dados_empresas.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
        
        with col3:
            # Botão de tela cheia
            if st.button("🔍 " + ("Sair da Tela Cheia" if st.session_state.fullscreen else "Tela Cheia")):
                st.session_state.fullscreen = not st.session_state.fullscreen
                st.experimental_rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Criar DataFrame para exibição
    display_df = df.copy()
    
    # Aplicar filtro se uma empresa específica for selecionada
    if empresas != 'Todas as empresas':
        display_df = display_df[display_df['Nome_Companhia'] == empresas]

    # Preparar dados para exibição
    display_df = pd.DataFrame({
        'Empresa': display_df['Nome_Companhia'],
        'Remuneração Total': display_df['Total_Remuneracao'],
        '% Market Cap': display_df['% da Remuneração Total sobre o Market Cap'] * 100,
        '% EBITDA': display_df['% da Remuneração Total sobre o EBITDA'] * 100,
        '% Net Income': display_df['% da Remuneração Total sobre o Net Income LTM'] * 100
    })

    # Altura da tabela baseada no modo de tela cheia
    table_height = None if st.session_state.fullscreen else 600

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
        height=table_height,
        use_container_width=True
    )

if __name__ == "__main__":
    main()
