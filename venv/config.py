import os

# Caminho base do projeto para garantir que os caminhos funcionem em qualquer máquina.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """
    Classe de configurações da aplicação.
    As variáveis de configuração do Flask DEVEM estar em letras maiúsculas.
    """
    # Chave secreta obrigatória para o Flask.
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'minha-chave-secreta-forte-e-dificil'

    # String de conexão para o MongoDB.
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/clinic_db'
    
    # Pasta para uploads temporários de arquivos.
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

