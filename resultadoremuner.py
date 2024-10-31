import pandas as pd

df_remuner = pd.read_excel('remtotal2024_novo.xlsx')

# filtra as colunas Nome_Companhia, Total_Remuneracao, "% da Remuneração Total sobre o Market Cap", % da Remuneracao sobre o EBITDA, % da Remuneradcao sobre o Net Income LTM

df_remuner = df_remuner[['Nome_Companhia', 'Total_Remuneracao', '% da Remuneração Total sobre o Market Cap', '% da Remuneração Total sobre o EBITDA', '% da Remuneração Total sobre o Net Income LTM']]

#GERA um excel com o resultado

df_remuner.to_excel('resultadoremuner.xlsx', index=False)

print(df_remuner.head())
print(df_remuner.info())

