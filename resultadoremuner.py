import pandas as pd

df_remuner = pd.read_excel('remtotal2024_novo.xlsx')

# filtra as colunas Nome_Companhia, Total_Remuneracao, "% da Remuneração Total sobre o Market Cap", % da Remuneracao sobre o EBITDA, % da Remuneradcao sobre o Net Income LTM

df_remuner = df_remuner[['Nome_Companhia', 'Total_Remuneracao', '% da Remuneração Total sobre o Market Cap', '% da Remuneração Total sobre o EBITDA', '% da Remuneração Total sobre o Net Income LTM']]

import streamlit as st
import pandas as pd
from datetime import datetime
import locale

# Configuração da página
st.set_page_config(page_title="BR Insider Analysis", layout="wide")

# Configuração do locale para formato brasileiro
locale.setlocale(locale.LC_ALL, 'pt_BR.UTF-8')

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
    </style>
""", unsafe_allow_html=True)

def load_data():
    # Simulação dos dados - substitua pelo seu arquivo real
    data = {
        'Data_Referencia': ['2024-07-01', '2024-07-01', '2024-07-01'],
        'Empresa': ['CIA SANEAMENTO BASICO EST SAO PAULO', 'AMERICANAS S.A. - em Recuperação Judicial', 'AMERICANAS S.A. - em Recuperação Judicial'],
        'Tipo_Cargo': ['Controlador ou Vinculado'] * 3,
        'Tipo_Movimentacao': ['Venda à vista', 'Subscrição', 'Subscrição'],
        'Tipo_Ativo': ['Ações'] * 3,
        'Caracteristica_Valor_Mobiliario': ['ON'] * 3,
        'Data_Movimentacao': ['2024-07-22', '2024-07-25', '2024-07-25'],
        'Quantidade': [220470, 5404616788, 2802465177],
        'Preco_Unitario': [67.00, 1.30, 1.30],
        'Volume_Financeiro': [14771490.00, 7026001824.40, 3643204730.10]
    }
    return pd.DataFrame(data)

def main():
    # Título personalizado
    st.markdown("""
        <div class="title-container">
            <h1 class="title-text">BR Insider Analysis</h1>
        </div>
    """, unsafe_allow_html=True)
    
    # Carregar dados
    df = load_data()
    
    # Linha de filtros
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        empresas = st.selectbox(
            'Empresas',
            options=['Choose an option'] + list(df['Empresa'].unique())
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col2:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        dates = st.date_input(
            'Período',
            value=(datetime(2024, 1, 1), datetime(2024, 9, 1)),
            format="YYYY/MM/DD"
        )
        st.markdown('</div>', unsafe_allow_html=True)
        
    with col3:
        st.markdown('<div class="filter-container">', unsafe_allow_html=True)
        tipo_mov = st.selectbox(
            'Tipo de Movimentação',
            options=['Choose an option'] + list(df['Tipo_Movimentacao'].unique())
        )
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Formatação dos dados para exibição
    df['Data_Referencia'] = pd.to_datetime(df['Data_Referencia']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df['Data_Movimentacao'] = pd.to_datetime(df['Data_Movimentacao']).dt.strftime('%Y-%m-%d')
    df['Preco_Unitario'] = df['Preco_Unitario'].apply(lambda x: f'R$ {x:.2f}')
    df['Volume_Financeiro'] = df['Volume_Financeiro'].apply(lambda x: f'R$ {x:,.2f}')
    df['Quantidade'] = df['Quantidade'].apply(lambda x: f'{x:,}')
    
    # Exibir tabela com estilo
    st.dataframe(
        df,
        hide_index=False,
        column_config={
            'Data_Referencia': 'Data Referência',
            'Tipo_Cargo': 'Tipo Cargo',
            'Tipo_Movimentacao': 'Tipo Movimentação',
            'Tipo_Ativo': 'Tipo Ativo',
            'Caracteristica_Valor_Mobiliario': 'Característica Valor Mobiliário',
            'Data_Movimentacao': 'Data Movimentação',
            'Preco_Unitario': 'Preço Unitário',
            'Volume_Financeiro': 'Volume Financeiro (R$)'
        },
        height=600
    )

if __name__ == "__main__":
    main()

print(df_remuner.head())
print(df_remuner.info())

