import streamlit as st
import pandas as pd

# Configuração da página
st.set_page_config(page_title="BR Insider Analysis", layout="wide", initial_sidebar_state="collapsed")

# Remover a barra do menu e o rodapé
st.markdown('''
    <style>
        header {display: none !important;}
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        .stDeployButton {display: none;}
        div[data-testid="stToolbar"] {visibility: hidden;}
        
        /* Remover espaços em branco */
        .appview-container {margin: 0 !important; padding: 0 !important;}
        .main > .block-container {padding: 0 !important; margin: 0 !important; max-width: 100% !important;}
        [data-testid="stDecoration"] {display: none !important;}
        .block-container {padding-top: 0rem !important;}
        [data-testid="stAppViewContainer"] > section:first-child {padding: 0 !important;}
        
        /* Estilo do título */
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
        
        /* Container do filtro */
        .filter-container {
            background-color: white;
            padding: 15px;
            border-radius: 5px;
            margin: 0 auto 25px auto;
            width: 95%;
            max-width: 1800px;
        }
        
        /* Cor de fundo principal */
        .stApp {
            background-color: #0A192F;
        }
        
        /* Estilos da tabela */
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
            background-color: white !important;
        }
        
        td:first-child {
            text-align: left !important;
        }
        
        tr:nth-child(even) {
            background-color: #f9f9f9 !important;
        }
        
        tr:nth-child(odd) {
            background-color: white !important;
        }
        
        /* Estilos do select box */
        .stSelectbox {
            background-color: white;
        }
        
        [data-testid="stDataFrame"] {
            width: 95% !important;
            margin: 0 auto;
            background-color: white !important;
        }
        
        /* Ajustes de layout */
        div[data-testid="stVerticalBlock"] > div {
            padding: 0;
        }
        
        section[data-testid="stSidebar"] {
            display: none;
        }
        
        [data-testid="stAppViewBlockContainer"] {
            padding: 0 !important;
            margin: 0 !important;
        }
        
        div.stMarkdown {
            width: 100% !important;
        }
        
        div.row-widget.stSelectbox {
            padding: 0;
        }

        /* Estilo do botão de download */
        .download-button {
            text-align: right;
            padding: 1rem;
        }

        iframe {
            background-color: white;
        }
    </style>
''', unsafe_allow_html=True)

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
        
        # Converter Total_Remuneracao para float
        df['Total_Remuneracao'] = pd.to_numeric(df['Total_Remuneracao'], errors='coerce')
        
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
    
    # Criar DataFrame para exibição
    display_df = pd.DataFrame({
        'Empresa': filtered_df['Nome_Companhia'],
        'Remuneração Total': filtered_df['Total_Remuneracao'],
        '% Market Cap': filtered_df['% da Remuneração Total sobre o Market Cap'] * 100,
        '% EBITDA': filtered_df['% da Remuneração Total sobre o EBITDA'] * 100,
        '% Net Income': filtered_df['% da Remuneração Total sobre o Net Income LTM'] * 100
    })

    # Botão de download
    st.markdown('<div class="download-button">', unsafe_allow_html=True)
    excel_data = display_df.copy()
    excel_data['% Market Cap'] = excel_data['% Market Cap'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "None")
    excel_data['% EBITDA'] = excel_data['% EBITDA'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "None")
    excel_data['% Net Income'] = excel_data['% Net Income'].apply(lambda x: f"{x:.2f}%" if pd.notnull(x) else "None")
    
    def convert_df_to_excel():
        output = pd.ExcelWriter('data.xlsx', engine='xlsxwriter')
        excel_data.to_excel(output, index=False, sheet_name='Sheet1')
        output.close()
        with open('data.xlsx', 'rb') as f:
            return f.read()

    excel_file = convert_df_to_excel()
    st.download_button(
        label="📥 Baixar dados",
        data=excel_file,
        file_name="dados_empresas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.markdown('</div>', unsafe_allow_html=True)

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
        height=800,
        use_container_width=True
    )

if __name__ == "__main__":
    main()
