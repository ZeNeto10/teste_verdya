# Importa a função que cria nossa aplicação, do pacote 'app'
from app import create_app
# Importa a classe de configuração do arquivo 'config.py'
from config import Config

if __name__ == '__main__':
    # Diagnóstico: Vamos imprimir para ter certeza que a Config foi importada.
    print(f"Carregando aplicação com a configuração da classe: {Config}")
    print(f"O caminho para uploads será: {Config.UPLOAD_FOLDER}")

    # 1. Cria uma instância da nossa aplicação.
    # 2. Passa a classe de configuração inteira como um objeto para a função.
    app = create_app(Config)

    # 3. Executa a aplicação no modo de desenvolvimento.
    app.run(debug=True)
