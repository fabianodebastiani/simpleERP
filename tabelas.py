# -*- coding: utf-8 -*-



# Criada aqui uma lista em formato json com todas as tabelas a serem criadas
# com nomes da tabela e nome e tipo de todos os campos


notasJson = {'nome': 'notas', 'campos': [
    {'nome': 'id', 'tipo': 'text'}, 
    {'nome': 'versao', 'tipo': 'text'},
    {'nome': 'serie', 'tipo': 'text'},
    {'nome': 'nota', 'tipo': 'text'},
    {'nome': 'serieNota', 'tipo': 'text'},
    {'nome': 'emissaoTimeStamp', 'tipo': 'integer'},
    {'nome': 'lancamentoTimeStamp', 'tipo': 'integer'},
    {'nome': 'natureza', 'tipo': 'text'},
    {'nome': 'ICMS', 'tipo': 'real'},
    {'nome': 'ICMSST', 'tipo': 'real'},
    {'nome': 'valorDosProdutos', 'tipo': 'real'},
    {'nome': 'IPI', 'tipo': 'real'},
    {'nome': 'PIS', 'tipo': 'real'},
    {'nome': 'COFINS', 'tipo': 'real'},
    {'nome': 'valorDaNota', 'tipo': 'real'},
    {'nome': 'itens', 'tipo': 'integer'},
    {'nome': 'quantidade', 'tipo': 'integer'}
]}




produtosNotasJson = {'nome': 'produtosNotas', 'campos': [
    {'nome': 'id', 'tipo': 'text'},
    {'nome': 'item', 'tipo': 'text'}, 
    {'nome': 'codigo', 'tipo': 'text'},
    {'nome': 'barras', 'tipo': 'text'},
    {'nome': 'descricao', 'tipo': 'text'},
    {'nome': 'quantidade', 'tipo': 'integer'},
    {'nome': 'valorUnitarioSemImpostos', 'tipo': 'real'},
    {'nome': 'valorTotalSemImpostos', 'tipo': 'real'},
    {'nome': 'pedido', 'tipo': 'text'},
    {'nome': 'aliquotaIPI', 'tipo': 'real'},
    {'nome': 'IPI', 'tipo': 'real'},
    {'nome': 'aliquotaPIS', 'tipo': 'real'},
    {'nome': 'PIS', 'tipo': 'real'},
    {'nome': 'aliquotaCOFINS', 'tipo': 'real'},
    {'nome': 'COFINS', 'tipo': 'real'},
    {'nome': 'aliquotaICMS', 'tipo': 'real'},
    {'nome': 'ICMS', 'tipo': 'real'},
    {'nome': 'aliquotaICMSST', 'tipo': 'real'},
    {'nome': 'ICMSST', 'tipo': 'real'},
    {'nome': 'valorTotalComImpostos', 'tipo': 'real'}
]}





tabelasACriar = [notasJson, produtosNotasJson]







        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
        
    
    
    
    
    
    
    
