from flask import Flask
from database.connection import criar_tabelas
from controllers.rotas_controller import init_routes

app = Flask(__name__)

# Garante que as tabelas existem ao subir o servidor
criar_tabelas()

# Inicializa todas as rotas originais mantendo os nomes intactos para o HTML
init_routes(app)

if __name__ == "__main__":
    app.run(debug=True)