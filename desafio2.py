# -*- coding: utf-8 -*-
"""
Crie um programa em Python que utilize o modelo de precificação de opções BlackScholes para 
avaliar o preço de uma opção de compra ou venda. O programa deve ser capaz de receber informações 
sobre o preço atual do ativo subjacente, a taxa livre de risco, a volatilidade do ativo e o tempo restante até o vencimento da opção. 
"""

import numpy as np
from scipy.stats import norm

################################# VARIÁVEIS ###################################

# Tipo de opção: compra -> C ou venda -> P
tipo = 'C'

# Preço atual do ativo subjacente
S = 60

# Preço de excução da opção
K = 50

# Taxa livre de risco (a.a)
r = 0.1

# Volatilidade do ativo
V = 0.2

# Tempo para o vencimento da opção (anos)
t = 0.5

###############################################################################
d1 = (np.log(S/K) + (r + V**2/2) * t)/(V * np.sqrt(t))
d2 = d1 - V*np.sqrt(t)

# Opção de compra
if tipo == 'C':
    price = S * norm.cdf(d1) - K * np.exp(-r * t) * norm.cdf(d2)

if tipo == 'P':
    price =  K * np.exp(-r * t) * norm.cdf(-d2) - S * norm.cdf(-d1) 

print('Preço da Opção (' + tipo + '): ' + str(round(price,2)))