from database.connection import conectar

def repo_contar_totais():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT COUNT(*) AS total FROM usuarios")
    u = cursor.fetchone()["total"]
    cursor.execute("SELECT COUNT(*) AS total FROM arenas")
    a = cursor.fetchone()["total"]
    cursor.execute("SELECT COUNT(*) AS total FROM reservas")
    r = cursor.fetchone()["total"]
    conexao.close()
    return {"total_usuarios": u, "total_arenas": a, "total_reservas": r}

def repo_listar_usuarios(tipo_filtro=None):
    conexao = conectar()
    cursor = conexao.cursor()
    if tipo_filtro:
        cursor.execute("SELECT * FROM usuarios WHERE tipo_usuario = ?", (tipo_filtro,))
    else:
        cursor.execute("SELECT * FROM usuarios")
    usuarios = cursor.fetchall()
    conexao.close()
    return usuarios

def repo_listar_arenas_com_dono():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("""
        SELECT a.*, u.nome AS nome_dono
        FROM arenas a
        JOIN usuarios u ON u.usuario_id = a.dono_id
    """)
    arenas = cursor.fetchall()
    conexao.close()
    return arenas

def repo_filtrar_arenas_api(cidade_filtro=None):
    conexao = conectar()
    cursor = conexao.cursor()
    if cidade_filtro:
        cursor.execute("SELECT * FROM arenas WHERE cidade LIKE ?", (f"%{cidade_filtro}%",))
    else:
        cursor.execute("SELECT * FROM arenas")
    arenas = cursor.fetchall()
    conexao.close()
    return arenas

def repo_buscar_tipo_usuario(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT tipo_usuario FROM usuarios WHERE usuario_id = ?", (usuario_id,))
    dono = cursor.fetchone()
    conexao.close()
    return dono

def repo_verificar_arena_existe(arena_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT arena_id FROM arenas WHERE arena_id = ?", (arena_id,))
    existe = cursor.fetchone() is not None
    conexao.close()
    return existe

def repo_listar_quadras(arena_id_filtro=None):
    conexao = conectar()
    cursor = conexao.cursor()
    if arena_id_filtro:
        cursor.execute("SELECT * FROM quadras WHERE arena_id = ?", (arena_id_filtro,))
    else:
        cursor.execute("SELECT * FROM quadras")
    quadras = cursor.fetchall()
    conexao.close()
    return quadras

def repo_buscar_preco_quadra(quadra_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT preco_hora FROM quadras WHERE quadra_id = ?", (quadra_id,))
    quadra = cursor.fetchone()
    conexao.close()
    return quadra

def repo_verificar_conflito_reserva(quadra_id, inicio, fim):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """SELECT reserva_id FROM reservas 
           WHERE quadra_id = ? 
             AND data_hora_inicio < ? 
             AND data_hora_fim > ?""",
        (quadra_id, fim, inicio)
    )
    conflito = cursor.fetchone() is not None
    conexao.close()
    return conflito

def repo_listar_reservas():
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM reservas")
    reservas = cursor.fetchall()
    conexao.close()
    return reservas