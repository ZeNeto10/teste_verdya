from app import create_app
from config import Config

# Cria a instância da aplicação Flask, passando o objeto de configuração
# como argumento para a função, que é o que ela espera.
app = create_app(Config)

if __name__ == '__main__':
    # Executa a aplicação em modo de desenvolvimento (debug=True)
    app.run(debug=True)
