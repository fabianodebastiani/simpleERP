# -*- coding: utf-8 -*-

#Este é o arquivo principal


import init
import erp





diretorio = 'C:/Users/fabia/OneDrive/SwarovskiCompartilhado/Notas Fiscais/'
arquivo0 = 'C:/Users/fabia/OneDrive/SwarovskiCompartilhado/Notas Fiscais/02702284000274_122364.xml'
arquivo1 = 'C:/Users/fabia/OneDrive/SwarovskiCompartilhado/Notas Fiscais/02702284000274_122365.xml'

# n = erp.notaFiscal(arquivo0)
# n.toDataBase('assistente.db')

# n = erp.notaFiscal(arquivo1)
# n.toDataBase('assistente.db')

erp.carregaPasta(diretorio, 'assistente.db')



import sqlite3
conn = sqlite3.connect('assistente.db') # ou use :memory: para botá-lo na memória RAM
c = conn.cursor()

c.execute("SELECT * FROM notas")
print(c.fetchall())
conn.close()
    

    

