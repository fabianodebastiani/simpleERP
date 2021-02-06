# -*- coding: utf-8 -*-

#Imports
import untangle
from datetime import datetime as dtm
import os
import sqlite3
import datetime as dt
import pandas as pd


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
            
            #carrega notas
            valuesTuple = (
                
                self.id,
                self.versao,
                self.serie,
                self.nota,
                self.serieNota,
                self.emissaoTimeStamp,
                self.lancamentoTimeStamp,
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
            
            #carrega produtos das notas
            
            for i in self.produtos:
                valuesTuple = (
                    
                    self.id,
                    i.item,
                    i.codigo,
                    i.barras,
                    i.descricao,
                    i.quantidade,
                    i.valorUnitarioSemImpostos,
                    i.valorTotalSemImpostos,
                    i.pedido,
                    i.aliquotaIPI,
                    i.IPI,
                    i.aliquotaPIS,
                    i.PIS,
                    i.aliquotaCOFINS,
                    i.COFINS,
                    i.aliquotaICMS,
                    i.ICMS,
                    i.aliquotaICMSST,
                    i.ICMSST,
                    i.valorTotalComImpostos,
                    

                )
        
                temp = ["?" for x in valuesTuple]
                sqlString = ','.join(temp)
                sqlString = "INSERT INTO produtosNotas VALUES (" + sqlString + ")"
                #print(valuesTuple)
                #print(sqlString)
                c.execute(sqlString,valuesTuple) 
                conn.commit()
            
            
            
            
        conn.close()
        
        
        
def carregaPastaDeNotas(diretorio, db):
    print('Carregando pasta de notas...')
    for root, dirs, files in os.walk(diretorio):
        for name in files:
            if name[-4:] == '.xml':
                n = notaFiscal(os.path.join(root, name))
                n.toDataBase(db)
        
        
        
        
        
        
   
#Classes relacionadas a Vendas

class venda:
    
    def toDataBase(self, db):
        conn = sqlite3.connect(db) # ou use :memory: para botá-lo na memória RAM
        c = conn.cursor()
        sqlString = "SELECT * FROM vendas WHERE serieNota=?"
        c.execute(sqlString, (self.serieNota,))
        temp = c.fetchone()
        #print(temp)
        if temp == None:
            
            #carrega notas
            valuesTuple = (
                
                self.serieNota,
                self.serie,
                self.nota,
                self.dataTimeStamp,
                self.cliente,
                self.tipo,
                self.vendedor,
                self.desconto,
                self.valor,               

            )
            
           
    
            temp = ["?" for x in valuesTuple]
            sqlString = ','.join(temp)
            sqlString = "INSERT INTO vendas VALUES (" + sqlString + ")"
            #print(valuesTuple)
            #print(sqlString)
            c.execute(sqlString,valuesTuple)
            conn.commit()
            
            #carrega produtos das notas
            
            for i in self.produtos:
                valuesTuple = (
                    
                    self.serieNota,
                    i.linx,
                    i.descricao,
                    i.quantidade,
                    i.desconto,
                    i.valor,


                )
                
       
                temp = ["?" for x in valuesTuple]
                sqlString = ','.join(temp)
                sqlString = "INSERT INTO produtosVendas VALUES (" + sqlString + ")"
                #print(valuesTuple)
                #print(sqlString)
                c.execute(sqlString,valuesTuple) 
                conn.commit()
            
            
            
            
        conn.close()



class itemVenda:
    pass

class listaDeVendas:
    def __init__(self):
        self.lista = []
        self.dictSerieNota = {}
        
    def carregaArquivo(self, arquivo):
        xl = pd.ExcelFile(arquivo)
        df = xl.parse('FaturamentoVendedor')

        
        for index, row in df.iterrows():
            if '-' in str(row[0]):
                if str(row[0])[:str(row[0]).find('-')].strip().isdigit():
                    Vendedor = row[0][str(row[0]).find('-')+1:].strip().title()
                    #print(Vendedor)
            else:
                if str(row[0])[2:3] == '/' and str(row[0])[5:6] == '/':
                    Data = int(dtm.timestamp(dt.datetime(int(row[0][6:10]),int(row[0][3:5]),int(row[0][0:2]))))
                    Serie = str(row[1])
                    Nota = str(row[2])[:str(row[2]).find('/')-1]
                    Cliente = str(row[3])[str(row[3]).find('-')+1:].title()
                    Valor = float(str(row[5]).replace('.','').replace(',','.'))
                    if str(row[7]).strip() != '-':
                        DescontoNota = float(str(row[7]).replace('.','').replace(',','.'))
                    else:
                        DescontoNota = float(0)
                    if Valor >= 0:
                        Tipo = 'Venda'
                    else:
                        Tipo = 'Devolucao'
                    
                    novaVenda = venda()
                    novaVenda.dataTimeStamp = Data
                    novaVenda.serie = Serie
                    novaVenda.nota = Nota
                    novaVenda.serieNota = novaVenda.serie + '-' + novaVenda.nota
                    novaVenda.tipo = Tipo
                    novaVenda.cliente = Cliente 
                    novaVenda.valor = Valor
                    novaVenda.desconto = DescontoNota
                    novaVenda.vendedor = Vendedor
                    novaVenda.produtos = []
                    self.lista.append(novaVenda)
                    self.dictSerieNota[(novaVenda.serie, novaVenda.nota)] = novaVenda
                else:
                    if str(row[0]) == 'nan' and str(row[2]).replace('-','').isdigit():
                        Codigo = str(row[2]).replace('-','')
                        Descricao = str(row[3])
                        Quantidade = int(row[4])
                        ValorItem = float(str(row[5]).replace('.','').replace(',','.'))
                        if str(row[7]).strip() != '-':
                            DescontoItem = float(str(row[7]).replace('.','').replace(',','.'))
                        else:
                            DescontoItem = float(0)
                        novoItem = itemVenda()
                        novoItem.linx = Codigo
                        novoItem.descricao = Descricao
                        novoItem.quantidade = Quantidade
                        novoItem.valor = ValorItem
                        novoItem.desconto = DescontoItem
                        self.lista[-1].produtos.append(novoItem)
        
    def carregaPasta(self, diretorio):
        print('Carregando pasta de vendas...')
        for root, dirs, files in os.walk(diretorio):
            for name in files:
                if name[-5:] == '.xlsx':
                    path = os.path.join(root, name)
                    #print(path)
                    self.carregaArquivo(path)
                    
    def toDataBase(self, db):
        conn = sqlite3.connect(db) # ou use :memory: para botá-lo na memória RAM
        c = conn.cursor()
        
        for ven in self.lista:
        
        
            sqlString = "SELECT * FROM vendas WHERE serieNota=?"
            c.execute(sqlString, (ven.serieNota,))
            temp = c.fetchone()
            #print(temp)
            if temp == None:
                
                #carrega notas
                valuesTuple = (
                    
                    ven.serieNota,
                    ven.serie,
                    ven.nota,
                    ven.dataTimeStamp,
                    ven.cliente,
                    ven.tipo,
                    ven.vendedor,
                    ven.desconto,
                    ven.valor,               
    
                )
                
               
        
                temp = ["?" for x in valuesTuple]
                sqlString = ','.join(temp)
                sqlString = "INSERT INTO vendas VALUES (" + sqlString + ")"
                #print(valuesTuple)
                #print(sqlString)
                c.execute(sqlString,valuesTuple)
                conn.commit()
                
                #carrega produtos das notas
                
                for prod in ven.produtos:
                    valuesTuple = (
                        
                        ven.serieNota,
                        prod.linx,
                        prod.descricao,
                        prod.quantidade,
                        prod.desconto,
                        prod.valor,
    
    
                    )
                    
           
                    temp = ["?" for x in valuesTuple]
                    sqlString = ','.join(temp)
                    sqlString = "INSERT INTO produtosVendas VALUES (" + sqlString + ")"
                    #print(valuesTuple)
                    #print(sqlString)
                    c.execute(sqlString,valuesTuple) 
                    conn.commit()
            
            
            
            
        conn.close()
        
                
        

