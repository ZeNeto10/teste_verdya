import csv
from datetime import datetime
from app import mongo
from decimal import Decimal, InvalidOperation
from bson.decimal128 import Decimal128

def processar_csv_booksy(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8-sig') as f:
            primeira_linha = f.readline()
            delimitador = ';' if primeira_linha.count(';') > primeira_linha.count(',') else ','
            f.seek(0)
            leitor = csv.DictReader(f, delimiter=delimitador)
            novas_receitas_adicionadas = 0
            for linha in leitor:
                id_transacao = linha['ID da transação']
                if mongo.db.receitas.find_one({'id_transacao_externa': id_transacao}):
                    continue
                try:
                    data_transacao = datetime.strptime(linha['Data'], '%d/%m/%Y %H:%M')
                    valor_str = linha['Valor Bruto'].replace('.', '').replace(',', '.')
                    valor_decimal = Decimal(valor_str)
                except (ValueError, InvalidOperation) as conv_error:
                    print(f"Aviso: Erro de conversão na linha {leitor.line_num}. Linha ignorada. Detalhes: {conv_error}")
                    continue
                mongo.db.receitas.insert_one({
                    'id_transacao_externa': id_transacao,
                    'data_transacao': data_transacao,
                    'cliente': linha['Cliente'],
                    'descricao': linha['Descrição'],
                    'valor': Decimal128(valor_decimal),
                    'fonte': 'Booksy',
                    'data_criacao': datetime.utcnow()
                })
                novas_receitas_adicionadas += 1
        return novas_receitas_adicionadas, None
    except KeyError as e:
        return 0, f"Erro ao processar o arquivo. A coluna esperada {e} não foi encontrada no CSV. Verifique o cabeçalho do arquivo."
    except Exception as e:
        return 0, f"Ocorreu um erro inesperado: {str(e)}"

def processar_csv_despesas(caminho_arquivo):
    try:
        with open(caminho_arquivo, mode='r', encoding='utf-8-sig') as f:
            primeira_linha = f.readline()
            delimitador = ';' if primeira_linha.count(';') > primeira_linha.count(',') else ','
            f.seek(0)
            leitor = csv.DictReader(f, delimiter=delimitador)
            novas_despesas_adicionadas = 0
            for linha in leitor:
                try:
                    data_transacao = datetime.strptime(linha['Data'], '%d/%m/%Y')
                    valor_str = linha['Valor'].replace('.', '').replace(',', '.')
                    valor_decimal = Decimal(valor_str)
                    mongo.db.despesas.insert_one({
                        'data_transacao': data_transacao,
                        'descricao': linha['Descricao'],
                        'categoria': linha['Categoria'],
                        'valor': Decimal128(valor_decimal),
                        'fonte': 'CSV Import',
                        'data_criacao': datetime.utcnow()
                    })
                    novas_despesas_adicionadas += 1
                except (ValueError, InvalidOperation, KeyError) as e:
                    print(f"Aviso: Linha ignorada por erro de formato ou coluna faltando. Erro: {e}. Linha: {linha}")
                    continue
        return novas_despesas_adicionadas, None
    except Exception as e:
        return 0, f"Ocorreu um erro inesperado: {str(e)}"
