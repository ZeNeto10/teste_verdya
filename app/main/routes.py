import os
from flask import render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
from datetime import datetime

from app import mongo
from app.main import bp
from app.main.forms import DespesaForm
from app.services import csv_processor_service, financial_service

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    # Usando nossos serviços para obter os dados do dashboard
    sumario = financial_service.obter_sumario_financeiro(periodo_dias=30)
    despesas_categoria = financial_service.obter_despesas_por_categoria(periodo_dias=30)
    
    # Aqui passaremos os dados para o template HTML renderizar
    return f"Dashboard (Em construção)<br>Sumário: {sumario}<br>Categorias: {despesas_categoria}"

@bp.route('/upload', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        if 'arquivo_csv' not in request.files:
            flash('Nenhuma parte do arquivo', 'danger')
            return redirect(request.url)
        
        arquivo = request.files['arquivo_csv']
        if arquivo.filename == '':
            flash('Nenhum arquivo selecionado', 'danger')
            return redirect(request.url)
            
        if arquivo:
            from flask import current_app
            nome_seguro = secure_filename(arquivo.filename)
            caminho_arquivo = os.path.join(current_app.config['UPLOAD_FOLDER'], nome_seguro)
            arquivo.save(caminho_arquivo)
            
            novas, erro = csv_processor_service.processar_csv_booksy(caminho_arquivo)
            
            if erro:
                flash(f'Erro ao processar o arquivo: {erro}', 'danger')
            else:
                flash(f'{novas} novas receitas foram importadas com sucesso!', 'success')
            
            return redirect(url_for('main.dashboard'))
    
    # Se for GET, apenas renderiza a página de upload (a ser criada)
    return "Página de Upload (Em construção)"

@bp.route('/despesas', methods=['GET', 'POST'])
def gerenciar_despesas():
    form = DespesaForm()
    if form.validate_on_submit():
        # Se o formulário for válido, salva a nova despesa no MongoDB
        mongo.db.despesas.insert_one({
            'descricao': form.descricao.data,
            'valor': form.valor.data,
            'categoria': form.categoria.data,
            'data_transacao': datetime.combine(form.data_transacao.data, datetime.min.time()),
            'data_criacao': datetime.utcnow()
        })
        flash('Despesa adicionada com sucesso!', 'success')
        return redirect(url_for('main.gerenciar_despesas'))
    
    # Busca todas as despesas para listar na página
    lista_despesas = mongo.db.despesas.find().sort('data_transacao', -1)
    
    # Renderiza a página de despesas (a ser criada)
    return f"Página de Despesas (Em construção) - {list(lista_despesas)}"