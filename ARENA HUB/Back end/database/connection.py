import sqlite3
import os

NOME_BANCO = "hub_arena.db"

def conectar():
    conexao = sqlite3.connect(NOME_BANCO)
    conexao.row_factory = sqlite3.Row
    conexao.execute("PRAGMA foreign_keys = ON")
    return conexao

def inicializar_banco():
    caminho_sql = os.path.join(os.path.dirname(__file__), 'create_database.sql')
    if os.path.exists(caminho_sql):
        with open(caminho_sql, 'r', encoding='utf-8') as f:
            sql = f.read()
        conexao = conectar()
        conexao.executescript(sql)
        conexao.commit()
        conexao.close()