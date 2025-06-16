from app import mongo
from datetime import datetime, timedelta
from bson.decimal128 import Decimal128
from decimal import Decimal

def _get_start_date(periodo_dias=30):
    return datetime.utcnow() - timedelta(days=periodo_dias)

def adicionar_despesa(descricao, valor, categoria, data_transacao):
    mongo.db.despesas.insert_one({
        'descricao': descricao,
        'valor': Decimal128(Decimal(str(valor))),
        'categoria': categoria,
        'data_transacao': datetime.combine(data_transacao, datetime.min.time()),
        'data_criacao': datetime.utcnow()
    })

def listar_despesas():
    return list(mongo.db.despesas.find().sort('data_transacao', -1))

def obter_sumario_financeiro(periodo_dias=30):
    data_inicio = _get_start_date(periodo_dias)
    
    pipeline_receitas = [
        {'$match': {'data_transacao': {'$gte': data_inicio}}},
        {'$group': {'_id': None, 'total': {'$sum': '$valor'}}}
    ]
    pipeline_despesas = [
        {'$match': {'data_transacao': {'$gte': data_inicio}}},
        {'$group': {'_id': None, 'total': {'$sum': '$valor'}}}
    ]
    
    receitas_result = list(mongo.db.receitas.aggregate(pipeline_receitas))
    despesas_result = list(mongo.db.despesas.aggregate(pipeline_despesas))
    
    total_receitas = receitas_result[0]['total'].to_decimal() if receitas_result else Decimal('0')
    total_despesas = despesas_result[0]['total'].to_decimal() if despesas_result else Decimal('0')
    
    lucro = total_receitas - total_despesas
    
    return {'total_receitas': total_receitas, 'total_despesas': total_despesas, 'lucro': lucro}

def obter_despesas_por_categoria(periodo_dias=30):
    data_inicio = _get_start_date(periodo_dias)
    pipeline = [
        {'$match': {'data_transacao': {'$gte': data_inicio}}},
        {'$group': {'_id': '$categoria', 'total': {'$sum': '$valor'}}},
        {'$sort': {'total': -1}},
        {'$project': {'categoria': '$_id', 'total': {'$toString': '$total'}, '_id': 0}}
    ]
    return list(mongo.db.despesas.aggregate(pipeline))

def obter_receitas_despesas_por_dia(periodo_dias=30):
    data_inicio = _get_start_date(periodo_dias)
    dados_combinados = {}

    pipeline_base = [
        {'$match': {'data_transacao': {'$gte': data_inicio}}},
        {'$group': {'_id': {'$dateToString': {'format': '%Y-%m-%d', 'date': '$data_transacao'}}, 'total': {'$sum': '$valor'}}},
        {'$sort': {'_id': 1}}
    ]

    for item in mongo.db.receitas.aggregate(pipeline_base):
        dados_combinados[item['_id']] = {'total_receitas': item['total'].to_decimal(), 'total_despesas': Decimal('0')}

    for item in mongo.db.despesas.aggregate(pipeline_base):
        if item['_id'] in dados_combinados:
            dados_combinados[item['_id']]['total_despesas'] = item['total'].to_decimal()
        else:
            dados_combinados[item['_id']] = {'total_receitas': Decimal('0'), 'total_despesas': item['total'].to_decimal()}

    resultado_final = []
    for dia_offset in range(periodo_dias + 1):
        data_atual = (data_inicio.date() + timedelta(days=dia_offset))
        data_str = data_atual.strftime('%Y-%m-%d')
        dados_do_dia = dados_combinados.get(data_str, {'total_receitas': Decimal('0'), 'total_despesas': Decimal('0')})
        resultado_final.append({
            'data': datetime.strptime(data_str, '%Y-%m-%d'),
            'total_receitas': dados_do_dia['total_receitas'],
            'total_despesas': dados_do_dia['total_despesas']
        })
    return sorted(resultado_final, key=lambda x: x['data'])

def limpar_todos_os_dados():
    """
    Remove todos os documentos das coleções de receitas e despesas.
    """
    mongo.db.receitas.delete_many({})
    mongo.db.despesas.delete_many({})
    print("Coleções de receitas e despesas foram limpas.")
