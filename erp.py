# -*- coding: utf-8 -*-

#Imports
import untangle
import datetime as dt
from datetime import datetime as dtm
import os
import pandas as pd
import sqlite3


#Classes relacionadas a Notas em formato xml

class notaFiscalProduto:
    def __init__(self, produto):
        self.item = produto['nItem']
        self.codigo = str(int(produto.prod.cProd.cdata))
        self.barras = produto.prod.cEAN.cdata
        self.descricao = produto.prod.xProd.cdata
        self.quantidade = float(produto.prod.qCom.cdata)
        self.valorUnitarioSemImpostos = float(produto.prod.vUnCom.cdata)
        self.valorTotalSemImpostos = float(produto.prod.vProd.cdata)
        self.pedido = produto.prod.xPed.cdata if 'xPed' in dir(produto.prod) else ''
        self.aliquotaIPI = float(produto.imposto.IPI.IPITrib.pIPI.cdata) if 'IPI' in dir(produto.imposto) and 'IPITrib' in dir(produto.imposto.IPI) else float(0)
        self.IPI = float(produto.imposto.IPI.IPITrib.vIPI.cdata) if 'IPI' in dir(produto.imposto) and 'IPITrib' in dir(produto.imposto.IPI) else float(0)
        self.aliquotaPIS = float(produto.imposto.PIS.PISAliq.pPIS.cdata) if 'PIS' in dir(produto.imposto) and 'PISAliq' in dir(produto.imposto.PIS) else float(0)
        self.PIS = float(produto.imposto.PIS.PISAliq.vPIS.cdata) if 'PIS' in dir(produto.imposto) and 'PISAliq' in dir(produto.imposto.PIS) else float(0)
        self.aliquotaCOFINS = float(produto.imposto.COFINS.COFINSAliq.pCOFINS.cdata) if 'COFINS' in dir(produto.imposto) and 'COFINSAliq' in dir(produto.imposto.COFINS) else float(0)
        self.COFINS = float(produto.imposto.COFINS.COFINSAliq.vCOFINS.cdata) if 'COFINS' in dir(produto.imposto) and 'COFINSAliq' in dir(produto.imposto.COFINS) else float(0)
        self.aliquotaICMS = float(produto.imposto.ICMS.ICMS00.pICMS.cdata) if 'ICMS00' in dir(produto.imposto.ICMS) else float(0)
        self.ICMS = float(produto.imposto.ICMS.ICMS00.vICMS.cdata) if 'ICMS00' in dir(produto.imposto.ICMS) else float(0)
        if 'ICMS10' in dir(produto.imposto.ICMS): self.aliquotaICMS = produto.imposto.ICMS.ICMS10.pICMS.cdata
        if 'ICMS10' in dir(produto.imposto.ICMS): self.ICMS = produto.imposto.ICMS.ICMS10.vICMS.cdata
        self.aliquotaICMSST = float(produto.imposto.ICMS.ICMS10.pICMS.cdata) if 'ICMS10' in dir(produto.imposto.ICMS) else float(0)
        self.ICMSST = float(produto.imposto.ICMS.ICMS10.vICMSST.cdata) if 'ICMS10' in dir(produto.imposto.ICMS) else float(0)
        self.valorTotalComImpostos = round(self.valorTotalSemImpostos + self.IPI + self.ICMSST, 2)

class notaFiscal:
    def __init__(self, file):
        n = untangle.parse(file)
        self.id = n.nfeProc.NFe.infNFe['Id']
        self.versao = n.nfeProc.NFe.infNFe['versao']
        self.serie = n.nfeProc.NFe.infNFe.ide.serie.cdata
        self.nota = n.nfeProc.NFe.infNFe.ide.nNF.cdata
        self.serieNota = self.serie + '-' + self.nota
        self.emissaoTimeStamp = int(dtm.timestamp(dtm.strptime(n.nfeProc.NFe.infNFe.ide.dhEmi.cdata[:19], '%Y-%m-%dT%H:%M:%S')))
        self.lancamentoTimeStamp = None
        self.natureza = n.nfeProc.NFe.infNFe.ide.natOp.cdata
        self.ICMS = float(n.nfeProc.NFe.infNFe.total.ICMSTot.vICMS.cdata)
        self.ICMSST = float(n.nfeProc.NFe.infNFe.total.ICMSTot.vST.cdata)
        self.valorDosProdutos = float(n.nfeProc.NFe.infNFe.total.ICMSTot.vProd.cdata)
        self.IPI = float(n.nfeProc.NFe.infNFe.total.ICMSTot.vIPI.cdata)
        self.PIS = float(n.nfeProc.NFe.infNFe.total.ICMSTot.vPIS.cdata)
        self.COFINS = float(n.nfeProc.NFe.infNFe.total.ICMSTot.vCOFINS.cdata)
        self.valorDaNota = float(n.nfeProc.NFe.infNFe.total.ICMSTot.vNF.cdata)
        self.produtos = []
        for i in n.nfeProc.NFe.infNFe.det:
            self.produtos.append(notaFiscalProduto(i))
        self.itens = len(self.produtos)
        self.quantidade = sum([x.quantidade for x in self.produtos])
        
    def toDataBase(self, db):
        conn = sqlite3.connect(db) # ou use :memory: para botá-lo na memória RAM
        c = conn.cursor()
        sqlString = "SELECT * FROM notas WHERE id=?"
        c.execute(sqlString, (self.id,))
        temp = c.fetchone()
        #print(temp)
        if temp == None:
            valuesTuple = (
                
                self.id,
                self.versao,
                self.serie,
                self.nota,
                self.serieNota,
                self.emissaoTimeStamp,
                self.natureza,
                self.ICMS,
                self.ICMSST,
                self.valorDosProdutos,
                self.IPI,
                self.PIS,
                self.COFINS,
                self.valorDaNota,
                self.itens,
                self.quantidade,
            )
    
            temp = ["?" for x in valuesTuple]
            sqlString = ','.join(temp)
            sqlString = "INSERT INTO notas VALUES (" + sqlString + ")"
            #print(valuesTuple)
            #print(sqlString)
            c.execute(sqlString,valuesTuple)
            conn.commit()
        conn.close()
        
        
        
def carregaPasta(diretorio, db):
    print('Carregando pasta de notas...')
    for root, dirs, files in os.walk(diretorio):
        for name in files:
            if name[-4:] == '.xml':
                n = notaFiscal(os.path.join(root, name))
                n.toDataBase(db)
        
        
        
        
        
        

        
        
# def criaTabela(db, tabela):
#     #Conecta a arquivo existente ou cria novo se não existir
#     conn = sqlite3.connect(db) # ou use :memory: para botá-lo na memória RAM
#     c = conn.cursor()
    
#     # Verifica se tabela já existe e retorna True or False na variável jaExiste
#     c.execute("SELECT name FROM sqlite_master WHERE type='table'")
#     temp = c.fetchall()
#     if (tabela['nome'],) in temp:
#         jaExiste = True
#         #print("Tabela já existe")
#     else:
#         jaExiste = False
#         #print("Tabela não existe")
        
#     # Se tabela não existe, cria
#     if jaExiste == False:
#         nome = tabela['nome']
#         string = ''
#         for i in tabela['campos']:
#             string = string + i['nome'] + ' ' + i['tipo'] + ', '
#         fullstring = "CREATE TABLE " + nome + " (" + string[:-2] + ")"
#         #print(fullstring)
#         c.execute(fullstring)
#         #print("Tabela foi criada")
        
#     conn.close()        
        