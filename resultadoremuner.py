import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Configuração inicial
st.set_page_config(
    page_title="BR Insider Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# CSS para o novo layout
st.markdown("""
<style>
header {display: none !important;}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
.block-container {padding: 0 !important;}
.stApp {
    background-color: #0A192F;
}

.title-container {
    background-color: #DEB887;
    padding: 20px;
    border-radius: 10px;
    margin: 0 auto 20px auto;
    text-align: center;
    width: 100%;
}

.title-text {
    color: white;
    font-size: 32px;
    font-weight: bold;
    margin: 0;
}

.filters-row {
    display: flex;
    justify-content: space-between;
    gap: 20px;
    padding: 20px;
    margin-bottom: 20px;
}

.filter-column {
    background-color: white;
    padding: 10px;
    border-radius: 5px;
    flex: 1;
}

.stSelectbox {
    width: 100%;
}

[data-testid="stDataFrame"] {
    width: 95% !important;
    margin: 0 auto;
    background-color: white !important;
    border-radius: 5px;
}

div[data-testid="stDataFrameResizable"] {
    padding: 1rem;
}

.download-button {
    padding: 1rem;
    text-align: left;
    margin-left: 2.5%;
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
    # Título
    st.markdown("""
        <div class="title-container">
            <h1 class="title-text">BR Insider Analysis</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Linha de filtros com 3 colunas
    st.markdown('<div class="filters-row">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="filter-column">', unsafe_allow_html=True)
        empresas = st.selectbox(
            'Empresas',
            options=['Choose an option'] + ['Todas as empresas']
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="filter-column">', unsafe_allow_html=True)
        data_range = st.text_input(
            'Período',
            value='2024/01/01 - 2024/09/01'
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="filter-column">', unsafe_allow_html=True)
        tipo_mov = st.selectbox(
            'Tipo de Movimentação',
            options=['Choose an option']
        )
        st.markdown('</div>', unsafe_allow_html=True)

    # Botão de download
    st.markdown('<div class="download-button">', unsafe_allow_html=True)
    st.download_button(
        label="📥 Baixar dados",
        data=b"placeholder",
        file_name="dados_empresas.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Dados da tabela
    df = pd.DataFrame({
        'Data_Referencia': ['2024-07-01 00:00:00'] * 5,
        'Empresa': ['CIA SANEAMENTO BASICO EST SAO PAULO', 'AMERICANAS S.A.', 'CIELO S.A.', 'MARFRIG GLOBAL FOODS S.A.', 'CENCOSUD BRASIL COMERCIAL S.A.'],
        'Tipo_Cargo': ['Controlador ou Vinculado'] * 5,
        'Tipo_Movimentacao': ['Venda à vista', 'Subscrição', 'Outras Entradas', 'Outras Entradas', 'Outras Entradas'],
        'Tipo_Ativo': ['Ações'] * 5,
        'Caracteristica_Valor_Mobiliario': ['ON'] * 5,
        'Data_Movimentacao': ['2024-07-22', '2024-07-25', '2024-08-14', '2024-03-10', '2024-01-30'],
        'Quantidade': [220470000, 5404616788, 525755748, 230095577, 1640826000],
        'Preco_Unitario': [67.00, 1.30, 5.82, 9.71, 1.00],
        'Volume Financeiro (R$)': [14771490000.00, 7026001824.40, 3059898453.36, 2234228052.67, 1640826000.00]
    })

    # Exibir tabela
    st.dataframe(
        df,
        hide_index=True,
        column_config={
            'Data_Referencia': 'Data_Referencia',
            'Empresa': 'Empresa',
            'Tipo_Cargo': 'Tipo_Cargo',
            'Tipo_Movimentacao': 'Tipo_Movimentacao',
            'Tipo_Ativo': 'Tipo_Ativo',
            'Caracteristica_Valor_Mobiliario': 'Caracteristica_Valor_Mobiliario',
            'Data_Movimentacao': 'Data_Movimentacao',
            'Quantidade': st.column_config.NumberColumn(
                'Quantidade',
                format="%d"
            ),
            'Preco_Unitario': st.column_config.NumberColumn(
                'Preço_Unitario',
                format="R$ %.2f"
            ),
            'Volume Financeiro (R$)': st.column_config.NumberColumn(
                'Volume Financeiro (R$)',
                format="R$ %.2f"
            )
        },
        height=800,
        use_container_width=True
    )

if __name__ == "__main__":
    main()
