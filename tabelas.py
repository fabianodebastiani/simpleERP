# -*- coding: utf-8 -*-

# Imports

import sqlite3


# Criada aqui uma lista em formato json com todas as tabelas a serem criadas
# com nomes da tabela e nome e tipo de todos os campos


notasJson = {'nome': 'notas', 'campos': [
    {'nome': 'id', 'tipo': 'text'}, 
    {'nome': 'versao', 'tipo': 'text'},
    {'nome': 'serie', 'tipo': 'text'},
    {'nome': 'nota', 'tipo': 'text'},
    {'nome': 'emissao', 'tipo': 'text'},
    {'nome': 'lancamento', 'tipo': 'text'},
    {'nome': 'natureza', 'tipo': 'text'},
    {'nome': 'icms', 'tipo': 'real'},
    {'nome': 'icmsst', 'tipo': 'real'},
    {'nome': 'valorDosProdutos', 'tipo': 'real'},
    {'nome': 'ipi', 'tipo': 'real'},
    {'nome': 'pis', 'tipo': 'real'},
    {'nome': 'cofins', 'tipo': 'real'},
    {'nome': 'valorDaNota', 'tipo': 'real'},
    {'nome': 'itens', 'tipo': 'integer'},
    {'nome': 'quantidade', 'tipo': 'integer'}
]}

notasLinxJson = {'nome': 'notasLinx', 'campos': [
    {'nome': 'id', 'tipo': 'text'}, 
    {'nome': 'versao', 'tipo': 'text'},
    {'nome': 'serie', 'tipo': 'text'},
    {'nome': 'nota', 'tipo': 'text'},
    {'nome': 'emissao', 'tipo': 'text'},
    {'nome': 'lancamento', 'tipo': 'text'},
    {'nome': 'natureza', 'tipo': 'text'},
    {'nome': 'icms', 'tipo': 'real'},
    {'nome': 'icmsst', 'tipo': 'real'},
    {'nome': 'valorDosProdutos', 'tipo': 'real'},
    {'nome': 'ipi', 'tipo': 'real'},
    {'nome': 'pis', 'tipo': 'real'},
    {'nome': 'cofins', 'tipo': 'real'},
    {'nome': 'valorDaNota', 'tipo': 'real'},
    {'nome': 'itens', 'tipo': 'integer'},
    {'nome': 'quantidade', 'tipo': 'integer'}
]}


tabelasACriar = [notasJson, notasLinxJson]





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
        

        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
