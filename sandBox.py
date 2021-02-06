import erp


diretorioVendas = 'C:/Users/fabia/OneDrive/SwarovskiCompartilhado/Vendas/'

v = erp.listaDeVendas()
v.carregaPasta(diretorioVendas)
v.toDataBase('assistente.db')