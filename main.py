# -*- coding: utf-8 -*-

#Este é o arquivo principal


import init
import erp





diretorio = 'C:/Users/fabia/OneDrive/SwarovskiCompartilhado/Notas Fiscais'

erp.carregaPasta(diretorio, 'assistente.db')



import sqlite3
conn = sqlite3.connect('assistente.db') # ou use :memory: para botá-lo na memória RAM
c = conn.cursor()

c.execute("SELECT * FROM notas")
print(c.fetchall())
conn.close()
    

    

