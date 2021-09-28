# -*- coding: utf-8 -*-
"""
Created on Wed Aug  4 13:27:00 2021

@author: Arthur
"""
import os
import pandas as pd


#Preambulo
path = os.getcwd()

#le os arquivos base, devem conter uma ID qualquer e a ottocodificao
otto_base = pd.read_csv(path + '\\input\\geoft_bho_area_contribuicao__02.csv', delimiter = ',', encoding = 'latin-1')
# base = 86285193
# bases = [86285193, 86277411, 862593151, 862539963, 8623999943, 862339933, 86219953, 862111133]
bases = [862111133]

for base in bases:
    #Cria uma coluna com os valores como "string"
    otto_base['COBACIA_str'] = otto_base['cob2'].astype(str)    
        
    #Separa essa informação por lista por lista
    otto_base_lista = otto_base['COBACIA'].tolist()
    
    #separa os valores da bacia base em lista - necessario para as contas
    list_base = list(str(base))
    
    #declara a lista de resultados, a ser adicionada no dataframe base
    lista_conferencia = []
    
    for item in range(len(otto_base_lista)): #teste uma a uma as bacias do arquivo base
        confere = 0 #variavel que armazena o resultado de se é contribuinte ou não
        # print(otto_base_lista[item], base) #imprimo como teste, não é necessário
        list_item = list(str(otto_base_lista[item])) #converte o codigo da ottobacia sendo analisada em lista
        for nivel in range(1, 20, 1): #esse for faz com que a bacia seja testa de nivel a nivel, de acordo com o ottocodificao em questao. 20 é um teto qualquer
            if confere == 0: #o laço é rodado até que o nivel em que a ottobacia sendo testada difira da base
                otto_indiv_teste = int("".join(list_item[0:nivel]))
                otto_indiv_base = int("".join(list_base[0:nivel]))
                # print("confere/base - nivel ", nivel, " - ", otto_indiv_teste, otto_indiv_base) #novamente, impressao de teste, não é necessário
                if otto_indiv_teste != otto_indiv_base: #teste 1  - valor das ottobacias diferete no nivel sendo testado
                    if otto_indiv_base%2 != 0:
                        if otto_indiv_teste < otto_indiv_base: #- se a base for impar, todo teste de valor superior sera contribuinte
                            confere = 1
                        elif otto_indiv_teste > otto_indiv_base: #- se a base for impar, todo teste de valor superior sera contribuinte
                            confere = 2
                    elif otto_indiv_base%2 == 0: #se os codigos sao diferentes e a base é par, teste não é contribuinte
                        confere = 1
                elif otto_indiv_base == base: #para que a propria ottobacia seja filtrada como sua contribuinte
                    confere = 2
        lista_conferencia.append(confere)
        print(base, " ", 100*item/len(otto_base_lista), "%")
    
    otto_base['contribuinte'] = lista_conferencia
    otto_base['contribuinte'].replace({0: "N", 1: "N", 2: "S"}, inplace=True)
    
    export = otto_base #o dataframe export é criado para não bagunçar o dataframe original
    export = export.drop(['COBACIA', 'COBACIA_str'], axis = 1)
    
    export.to_csv(path + '\\output\\resumo_contribuintes_%s.csv'%base, index = True)