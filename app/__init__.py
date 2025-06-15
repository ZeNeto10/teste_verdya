import os
from flask import Flask
from flask_pymongo import PyMongo

mongo = PyMongo()

def create_app(config_object):
    """
    Factory function que CRIA a aplicação.
    Agora, ela RECEBE um objeto de configuração como argumento.
    """
    app = Flask(__name__)
    
    # Carrega as configurações diretamente do objeto que foi passado.
    # Este é o método mais explícito e à prova de falhas.
    app.config.from_object(config_object)

    # Agora, quando esta linha for executada, a app.config JÁ TERÁ a UPLOAD_FOLDER.
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    # Inicializa o MongoDB com a aplicação.
    mongo.init_app(app)

    # Importa e registra o blueprint que contém as rotas.
    from app.main import bp as main_bp
    app.register_blueprint(main_bp)

    # Retorna a aplicação pronta para ser executada.
    return app
