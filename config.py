import os

# Determina o diretório base do projeto (onde este arquivo está)
basedir = os.path.abspath(os.path.dirname(__file__))

class Config:
    """Configurações da aplicação Flask."""
    
    # Chave secreta para proteger os formulários e a sessão contra CSRF
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'uma-chave-secreta-muito-dificil-de-adivinhar'
    
    # Configuração da URI de conexão com o MongoDB
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/verdya_db'
    
    # Pasta para salvar os arquivos de upload
    # Garante que a pasta 'uploads' seja criada na raiz do projeto
    UPLOAD_FOLDER = os.path.join(basedir, 'uploads')

