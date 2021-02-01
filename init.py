# -*- coding: utf-8 -*-

# Esse é o arquivo de inicialização do aplicativo
# A parte principal do aplicativo é uma base de dados em formato de arquivo
# Defini a base de dados como tendo o nome padrão "assistente.db"
# O arquivo de inicialização trata os seguintes passos:
#
#     - Verifica qual é o diretorio de onde o aplicativo (arquivo .exe) está sendo executado
#     - Verifica se no mesmo diretório existe a base de dados "assistente.db". Se não tem, cria.



# Imports gerais

import os
import sqlite3
import tabelas as tb


# Arquivo da base de dados
dataBase = 'assistente.db'


# Captura diretório de execução do aplicativo

diretorioDeExecucao = os.getcwd()

# Verifica ou cria arquivo de data base e fecha conexão

conn = sqlite3.connect(dataBase) # ou use :memory: para botá-lo na memória RAM
conn.close()

# Para cada tabela da base de dados, verifica existencia ou cria

for i in tb.tabelasACriar:
    tb.criaTabela(dataBase, i)