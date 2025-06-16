import os
from flask import render_template, request, redirect, url_for, flash, current_app
from werkzeug.utils import secure_filename
from datetime import datetime

from app import mongo
from . import bp
from app.main.forms import DespesaForm, CSVUploadForm, CSVDespesaUploadForm, EmptyForm
from app.services import csv_processor_service, financial_service

@bp.route('/')
@bp.route('/dashboard')
def dashboard():
    sumario = financial_service.obter_sumario_financeiro()
    despesas_categoria = financial_service.obter_despesas_por_categoria()
    receitas_despesas_diarias = financial_service.obter_receitas_despesas_por_dia()
    
    expenses_by_category_data = {
        "labels": [item['categoria'] for item in despesas_categoria],
        "values": [float(item['total']) for item in despesas_categoria]
    }
    
    revenue_expense_data = {
        "labels": [item['data'].strftime('%d/%m') for item in receitas_despesas_diarias],
        "revenues": [float(item['total_receitas']) for item in receitas_despesas_diarias],
        "expenses": [float(item['total_despesas']) for item in receitas_despesas_diarias]
    }
    
    return render_template(
        'dashboard.html',
        title="Dashboard",
        sumario=sumario,
        expenses_by_category_data=expenses_by_category_data,
        revenue_expense_data=revenue_expense_data
    )

@bp.route('/upload-receitas', methods=['GET', 'POST'])
def upload_receitas_csv():
    form = CSVUploadForm()
    if form.validate_on_submit():
        arquivo = form.arquivo_csv.data
        if arquivo:
            nome_seguro = secure_filename(arquivo.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            caminho_arquivo = os.path.join(upload_folder, nome_seguro)
            arquivo.save(caminho_arquivo)
            novas, erro = csv_processor_service.processar_csv_booksy(caminho_arquivo)
            if erro:
                flash(f'Erro ao processar o arquivo de receitas: {erro}', 'danger')
            else:
                flash(f'{novas} novas receitas foram importadas com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
    return render_template('upload.html', title="Upload de Receitas", form=form)

@bp.route('/upload-despesas', methods=['GET', 'POST'])
def upload_despesas_csv():
    form = CSVDespesaUploadForm()
    if form.validate_on_submit():
        arquivo = form.arquivo_csv.data
        if arquivo:
            nome_seguro = secure_filename(arquivo.filename)
            upload_folder = current_app.config['UPLOAD_FOLDER']
            if not os.path.exists(upload_folder):
                os.makedirs(upload_folder)
            caminho_arquivo = os.path.join(upload_folder, nome_seguro)
            arquivo.save(caminho_arquivo)
            novas, erro = csv_processor_service.processar_csv_despesas(caminho_arquivo)
            if erro:
                flash(f'Erro ao processar o arquivo de despesas: {erro}', 'danger')
            else:
                flash(f'{novas} novas despesas foram importadas com sucesso!', 'success')
            return redirect(url_for('main.dashboard'))
    return render_template('upload_despesas.html', title="Upload de Despesas", form=form)

@bp.route('/despesas', methods=['GET', 'POST'])
def gerenciar_despesas():
    form = DespesaForm()
    if form.validate_on_submit():
        financial_service.adicionar_despesa(
            descricao=form.descricao.data,
            valor=form.valor.data,
            categoria=form.categoria.data,
            data_transacao=form.data_transacao.data
        )
        flash('Despesa adicionada com sucesso!', 'success')
        return redirect(url_for('main.gerenciar_despesas'))
    lista_despesas = financial_service.listar_despesas()
    return render_template(
        'expenses.html', 
        title="Gerenciar Despesas", 
        form=form, 
        despesas=lista_despesas
    )

@bp.route('/configuracoes')
def configuracoes():
    """Renderiza a página de configurações."""
    form = EmptyForm() # Formulário vazio para proteção CSRF
    return render_template('configuracoes.html', title="Configurações", form=form)

@bp.route('/limpar-dados', methods=['POST'])
def limpar_dados():
    """Apaga todos os registros de receitas e despesas."""
    form = EmptyForm()
    if form.validate_on_submit():
        financial_service.limpar_todos_os_dados()
        flash('Todos os dados de receitas e despesas foram apagados com sucesso!', 'success')
    else:
        flash('Ocorreu um erro de validação. Tente novamente.', 'danger')
    return redirect(url_for('main.dashboard'))
