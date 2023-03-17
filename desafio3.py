# -*- coding: utf-8 -*-
"""
A Dual Digital Option é uma opção exótica que envolve dois ativos subjacentes e é paga quando ambos atingem as barreiras de preço. 
Especificamente, a opção paga um valor fixo se os preços dos dois ativos subjacentes estiverem dentro de um intervalo específico de
preços em um determinado momento do tempo. Para que o pagamento seja realizado, ambos os preços dos ativos subjacentes devem "tocar" 
as barreiras de preço simultaneamente durante a vigência da opção. A precificação da Dual Digital Option é um processo matemático 
complexo que envolve a modelagem da dinâmica dos preços dos dois ativos subjacentes, levando em consideração a volatilidade, tempo
até a expiração, correlação entre os preços dos ativos subjacentes e taxas de juros livres de risco. Suponha que você deseja precificar,
antes do vencimento, a opção exótica determinada acima. Escreva um código em Python para calcular o preço teórico dessa opção.
O output deve ser o preço teórico de uma determinada opção em um determinada tempo.
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
################################# VARIÁVEIS ###################################
# escolha o número de simulações
n_sim = 500

# taxa livre de risco
r = 0.05

# tempo até o vencimento da opção (anos)
T = 3
# tempo em que dejo o preço teórico (anos)
t = 2

# assumindo preços contínuos a cada m minutos
m = 1
num_samples = round((T - t) * 252 * 24 * (60/m))

# -------------------------------- ATIVO 1 ------------------------------------
# defina a barreira se preços para o ativo 1
barreira_sup1 = 5
barreira_inf1 = -5

#retorno médio/m
medio1 = 0.02/num_samples

#variância/m
var1 = 0.001/num_samples

# -------------------------------- ATIVO 2 ------------------------------------
# defina a barreira se preços para o ativo 2
barreira_sup2 = 6
barreira_inf2 = -0

#retorno médio/m
medio2 = 0.01/num_samples

#variância/m
var2 = 0.0015/num_samples

# Covariância entre ativoc/m
cov = 0.003/num_samples

###############################################################################

precos_da_opcao = list()
for i in range (100):
    
    # série de aleatória de retornos
    # The desired mean values of the sample.
    mu = np.array([medio1, medio2])
    
    # The desired covariance matrix.
    cov_matrix = np.array([
            [  var1, cov],
            [ cov,  var2],
        ])
    
    # Generate the random samples.
    rng = np.random.default_rng()
    retornos = pd.DataFrame(rng.multivariate_normal(mu, cov_matrix, size=num_samples),columns = ['ret1','ret2'])+1
    #base 100 para os preços
    precos = (retornos.cumprod()-1) * 100
    #plt.plot(precos[['ret1','ret2']])
    precos.columns = ['precos1','precos2'] 
    precos['strike1'] = np.where((precos['precos1']>barreira_sup1) | (precos['precos1']<barreira_inf1), True, False)
    precos['strike2'] = np.where((precos['precos1']>barreira_sup2) | (precos['precos2']<barreira_inf2), True, False)
    
    precos['strike1'] = np.where((precos['precos1']>barreira_sup1) | (precos['precos1']<barreira_inf1), True, False)
    precos['strike2'] = np.where((precos['precos1']>barreira_sup2) | (precos['precos2']<barreira_inf2), True, False)
    
    t_strike = precos[precos['strike1'] & precos['strike2']].reset_index()
    
    if len(t_strike) > 0:
        print('Strike')
        t_strike = t_strike['index'].min()
        #voltando t para a base anual
        t_strike = round(t_strike / (252 * 24 * (60/m)))
        valor_esperado = 1
        #preco da opção (valor presente do valor esperado)
        preco_op  = valor_esperado * np.exp(-r*(T-t)) 
    else:
        #sem strike
        print('Sem Strike')
        t_strike = False
        valor_esperado = 0
        #preco da opção (valor presente do valor esperado)
        preco_op = 0
        
    precos_da_opcao.append(preco_op)

#preco da opção
#média dos preços esperados
preco_final = sum(precos_da_opcao)/len(precos_da_opcao)

print('Preco ta Opção em t: ' + str(round(preco_final,3)))
