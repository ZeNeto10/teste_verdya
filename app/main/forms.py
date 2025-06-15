from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, DateField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, NumberRange

class DespesaForm(FlaskForm):
    """
    Formulário para o usuário registrar uma nova despesa.
    Cada atributo da classe representa um campo no formulário HTML.
    """
    descricao = StringField(
        'Descrição da Despesa', 
        validators=[
            DataRequired(message="Este campo é obrigatório."), 
            Length(min=3, max=200, message="A descrição deve ter entre 3 e 200 caracteres.")
        ]
    )
    
    valor = FloatField(
        'Valor (R$)', 
        validators=[
            DataRequired(message="Este campo é obrigatório."),
            NumberRange(min=0.01, message="O valor deve ser positivo.")
        ]
    )
    
    categoria = SelectField(
        'Categoria', 
        choices=[
            ('Custos Fixos', 'Custos Fixos (Aluguel, Salários)'),
            ('Materiais', 'Materiais e Suprimentos'),
            ('Marketing', 'Marketing e Publicidade'),
            ('Impostos', 'Impostos e Taxas'),
            ('Manutenção', 'Manutenção e Equipamentos'),
            ('Outros', 'Outros')
        ], 
        validators=[DataRequired(message="Selecione uma categoria.")]
    )
    

    data_transacao = DateField(
        'Data da Despesa', 
        format='%Y-%m-%d', 
        validators=[DataRequired(message="A data é obrigatória.")]
    )
    
    submit = SubmitField('Adicionar Despesa')