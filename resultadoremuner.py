import streamlit as st
import pandas as pd

# Configuração inicial
st.set_page_config(
    page_title="BR Insider Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS simplificado focando na remoção da barra branca
st.markdown("""
<style>
[data-testid="stHeader"] {
    display: none;
}

.stDeployButton {
    display: none;
}

.block-container {
    padding-top: 0 !important;
    padding-bottom: 0 !important;
}

[data-testid="stToolbar"] {
    display: none;
}

.stApp > header {
    display: none;
}

.stApp {
    margin-top: -4rem;
    background-color: #0A192F;
}

div[data-testid="stDecoration"] {
    display: none;
}

section[data-testid="stSidebar"] {
    margin-top: -4rem;
}

.title-container {
    background-color: #DEB887;
    padding: 20px;
    border-radius: 10px;
    margin-bottom: 20px;
    text-align: center;
    width: 95%;
    max-width: 1800px;
    margin-left: auto;
    margin-right: auto;
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
    margin: 20px auto;
    width: 95%;
    max-width: 1800px;
}

.download-button {
    text-align: right;
    padding: 1rem;
}

section.main > div:has(~ footer ) {
    padding-top: 0;
}

footer {
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
    
    df = load_data()
    
    if df.empty:
        st.warning("Não foi possível carregar os dados.")
        return
    
    # Filtro de empresas
    st.markdown('<div class="filter-container">', unsafe_allow_html=True)
    empresas = st.selectbox(
        'Empresas',
        options=['Todas as empresas'] + sorted(df['Nome_Companhia'].dropna().unique().tolist())
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    filtered_df = df.copy()
    if empresas != 'Todas as empresas':
        filtered_df = filtered_df[filtered_df['Nome_Companhia'] == empresas]
    
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
