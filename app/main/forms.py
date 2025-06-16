from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, SubmitField, SelectField, FloatField, DateField
from wtforms.validators import DataRequired, NumberRange, InputRequired
from datetime import date

class CSVUploadForm(FlaskForm):
    """Formulário para upload de arquivo CSV de Receitas."""
    arquivo_csv = FileField(
        'Selecione o arquivo CSV de Receitas', 
        validators=[
            FileRequired(message='Nenhum arquivo selecionado.'),
            FileAllowed(['csv'], 'Apenas arquivos .csv são permitidos!')
        ]
    )
    submit = SubmitField('Enviar Arquivo')

class CSVDespesaUploadForm(FlaskForm):
    """Formulário para upload de arquivo CSV de Despesas."""
    arquivo_csv = FileField(
        'Selecione o arquivo CSV de Despesas', 
        validators=[
            FileRequired(message='Nenhum arquivo selecionado.'),
            FileAllowed(['csv'], 'Apenas arquivos .csv são permitidos!')
        ]
    )
    submit = SubmitField('Enviar Arquivo')

class DespesaForm(FlaskForm):
    """Formulário para adicionar ou editar uma despesa manualmente."""
    descricao = StringField('Descrição', validators=[DataRequired(message="A descrição é obrigatória.")])
    valor = FloatField('Valor', validators=[InputRequired(message="O valor é obrigatório."), NumberRange(min=0.01, message="O valor deve ser positivo.")])
    categoria = SelectField('Categoria', choices=[
        ('Outros', 'Outros'),
        ('Alimentação', 'Alimentação'),
        ('Moradia', 'Moradia'),
        ('Transporte', 'Transporte'),
        ('Saúde', 'Saúde'),
        ('Lazer', 'Lazer'),
        ('Educação', 'Educação'),
    ], validators=[DataRequired(message="A categoria é obrigatória.")])
    data_transacao = DateField('Data da Transação', format='%Y-%m-%d', default=date.today, validators=[DataRequired(message="A data é obrigatória.")])
    submit = SubmitField('Adicionar Despesa')

class EmptyForm(FlaskForm):
    """
    Um formulário vazio usado para fornecer proteção CSRF a ações que
    não precisam de campos, como botões de exclusão.
    """
    pass
