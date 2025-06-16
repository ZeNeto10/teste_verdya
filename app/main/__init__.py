# Conteúdo para o novo arquivo: app/main/__init__.py

from flask import Blueprint

# Define o Blueprint para este pacote 'main'
bp = Blueprint('main', __name__)

# Importa as rotas no final para evitar importações circulares.
# Isso conecta as visualizações (rotas) definidas em routes.py ao blueprint.
from . import routes