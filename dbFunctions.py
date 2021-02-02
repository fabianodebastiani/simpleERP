# -*- coding: utf-8 -*-

import sqlite3

# Função que cria uma tabela em uma base de dados, caso ela já não exista

def criaTabela(db, tabela):
    #Conecta a arquivo existente ou cria novo se não existir
    conn = sqlite3.connect(db) # ou use :memory: para botá-lo na memória RAM
    c = conn.cursor()
    
    # Verifica se tabela já existe e retorna True or False na variável jaExiste
    c.execute("SELECT name FROM sqlite_master WHERE type='table'")
    temp = c.fetchall()
    if (tabela['nome'],) in temp:
        jaExiste = True
        #print("Tabela já existe")
    else:
        jaExiste = False
        #print("Tabela não existe")
        
    # Se tabela não existe, cria
    if jaExiste == False:
        nome = tabela['nome']
        string = ''
        for i in tabela['campos']:
            string = string + i['nome'] + ' ' + i['tipo'] + ', '
        fullstring = "CREATE TABLE " + nome + " (" + string[:-2] + ")"
        #print(fullstring)
        c.execute(fullstring)
        #print("Tabela foi criada")
        
    conn.close()
        

