from app import mongo
from datetime import datetime, timedelta
from bson.decimal128 import Decimal128
import decimal

def obter_sumario_financeiro(periodo_dias=30):
    """
    Calcula o total de receitas, despesas e o lucro usando o MongoDB Aggregation Framework.
    """
    data_inicio = datetime.utcnow() - timedelta(days=periodo_dias)

    # Pipeline de agregação para somar as receitas no período
    pipeline_receitas = [
        {'$match': {'data_transacao': {'$gte': data_inicio}}},
        {'$group': {'_id': None, 'total': {'$sum': '$valor'}}}
    ]
    resultado_receitas = list(mongo.db.receitas.aggregate(pipeline_receitas))
    total_receitas = resultado_receitas[0]['total'] if resultado_receitas else 0

    # Pipeline de agregação para somar as despesas no período
    pipeline_despesas = [
        {'$match': {'data_transacao': {'$gte': data_inicio}}},
        {'$group': {'_id': None, 'total': {'$sum': '$valor'}}}
    ]
    resultado_despesas = list(mongo.db.despesas.aggregate(pipeline_despesas))
    total_despesas = resultado_despesas[0]['total'] if resultado_despesas else 0

    lucro = total_receitas - total_despesas

    return {
        'total_receitas': total_receitas,
        'total_despesas': total_despesas,
        'lucro': lucro
    }

def obter_despesas_por_categoria(periodo_dias=30):
    """
    Agrupa as despesas por categoria para gerar um gráfico de pizza.
    """
    data_inicio = datetime.utcnow() - timedelta(days=periodo_dias)
    pipeline = [
        {'$match': {'data_transacao': {'$gte': data_inicio}}},
        {
            '$group': {
                '_id': '$categoria',
                'total': {'$sum': '$valor'}
            }
        },
        {'$sort': {'total': -1}} # Ordena do maior para o menor
    ]
    resultado = list(mongo.db.despesas.aggregate(pipeline))
    
    # Formata para ser facilmente consumido por uma biblioteca de gráficos
    # Ex: [{'categoria': 'Custos Fixos', 'total': 5000.0}, ...]
    dados_grafico = [{'categoria': item['_id'], 'total': item['total']} for item in resultado]
    
    return dados_grafico