import pandas as pd
from datetime import datetime
from app import mongo 

def processar_csv_booksy(caminho_arquivo):
    """
    Lê um arquivo CSV da Booksy, processa os dados e salva novas receitas na coleção 'receitas' do MongoDB.
    Retorna uma tupla (novas_receitas_count, erro_msg).
    """
    try:
        try:
            df = pd.read_csv(caminho_arquivo, sep=';', dtype=str)
        except Exception:
            df = pd.read_csv(caminho_arquivo, sep=',', dtype=str)

        mapeamento_colunas = {
            'ID da Transação': 'id_transacao_externa',
            'Data de Conclusão': 'data_transacao',
            'Descrição do Item': 'descricao',
            'Valor Bruto': 'valor'
        }
        df.rename(columns=mapeamento_colunas, inplace=True)
        

        df['valor'] = df['valor'].str.replace('R$', '', regex=False).str.strip()
        df['valor'] = df['valor'].str.replace('.', '', regex=False).str.replace(',', '.', regex=False).astype(float)
        
        df['data_transacao'] = pd.to_datetime(df['data_transacao'], format='%d/%m/%Y', errors='coerce')
        df.dropna(subset=['data_transacao'], inplace=True) 

        novas_receitas = 0
        for _, linha in df.iterrows():
            id_externo = str(linha['id_transacao_externa'])
            
            existe = mongo.db.receitas.find_one({'id_transacao_externa': id_externo})
            
            if not existe:
                documento_receita = {
                    'id_transacao_externa': id_externo,
                    'data_transacao': linha['data_transacao'],
                    'descricao': linha['descricao'],
                    'valor': linha['valor'],
                    'data_importacao': datetime.utcnow()
                }
                # Insere o novo documento na coleção 'receitas'.
                mongo.db.receitas.insert_one(documento_receita)
                novas_receitas += 1
        
        return novas_receitas, None

    except Exception as e:
        error_message = f"Erro ao processar o arquivo: {e}. Verifique se os nomes das colunas e os formatos de data/valor no arquivo CSV estão corretos."
        return 0, error_message