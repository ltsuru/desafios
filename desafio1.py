# -*- coding: utf-8 -*-
"""
Crie um programa em Python que receba um conjunto de dados de preços de ações e calcule o valor do beta 
cada ação em relação ao mercado. O programa deve ser capaz de lidar com grandes volumes de dados e produzir
resultados precisos e confiáveis. 
"""

import pandas as pd
import yfinance as yf

################################# VARIÁVEIS ###################################

#Escolha a data de início (YYYY-MM-DD)
inicio = '2013-03-14'

#Escolha a última data (YYYY-MM-DD)
fim = '2023-03-14'

#Escolha o índice (mercado)
#exemplos
#S&P: SPY
#Ibov: BOVA11.SA

indice = 'SPY'

#Escolha uma lista de empresas

empresas = ['MSFT','AMD','TXN','GE','C']

###############################################################################

# aqui a fonte de dados utilizada foi o yahoo finance, mas poder ser utilizadas
# outras fontes(leitura de csv, bloomberg...)
retornos = yf.download(tickers = empresas + [indice],
            start = inicio,         
            end = fim,       
            ignore_tz = True,     
            prepost = False)['Adj Close'].pct_change().dropna()       


cov = retornos.cov()[[indice]]
cov = cov[cov.index != indice]

var_mercado = retornos[indice].var()

betas = (cov/var_mercado).rename(columns={indice:'beta'})
betas['beta'] = betas['beta'].round(3)
print(betas)
