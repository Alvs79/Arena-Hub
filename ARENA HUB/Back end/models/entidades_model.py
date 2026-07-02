from database.connection import conectar

def db_inserir_usuario(nome, email, senha, telefone, tipo_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO usuarios (nome, email, senha, telefone, tipo_usuario) VALUES (?, ?, ?, ?, ?)",
        (nome, email, senha, telefone, tipo_usuario),
    )
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    return novo_id

def db_buscar_usuario_por_id(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE usuario_id = ?", (usuario_id,))
    row = cursor.fetchone()
    conexao.close()
    return dict(row) if row else None

def db_atualizar_usuario(usuario_id, nome, email, telefone, tipo_usuario):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """UPDATE usuarios
           SET nome = ?, email = ?, telefone = ?, tipo_usuario = ?
           WHERE usuario_id = ?""",
        (nome, email, telefone, tipo_usuario, usuario_id),
    )
    conexao.commit()
    conexao.close()

def db_deletar_usuario(usuario_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM usuarios WHERE usuario_id = ?", (usuario_id,))
    conexao.commit()
    conexao.close()

def db_inserir_arena(nome, cnpj, endereco, cidade, dono_id, taxa_saas):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO arenas (nome, cnpj, endereco, cidade, dono_id, taxa_saas) VALUES (?, ?, ?, ?, ?, ?)",
        (nome, cnpj, endereco, cidade, dono_id, taxa_saas),
    )
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    return novo_id

def db_buscar_arena_por_id(arena_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM arenas WHERE arena_id = ?", (arena_id,))
    row = cursor.fetchone()
    conexao.close()
    return dict(row) if row else None

def db_atualizar_arena(arena_id, nome, cnpj, endereco, cidade, taxa_saas):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """UPDATE arenas
           SET nome = ?, cnpj = ?, endereco = ?, cidade = ?, taxa_saas = ?
           WHERE arena_id = ?""",
        (nome, cnpj, endereco, cidade, taxa_saas, arena_id),
    )
    conexao.commit()
    conexao.close()

def db_deletar_arena(arena_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM arenas WHERE arena_id = ?", (arena_id,))
    conexao.commit()
    conexao.close()

def db_inserir_quadra(arena_id, nome, tipo_esporte, preco_hora):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "INSERT INTO quadras (arena_id, nome, tipo_esporte, preco_hora) VALUES (?, ?, ?, ?)",
        (arena_id, nome, tipo_esporte, preco_hora),
    )
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    return novo_id

def db_buscar_quadra_por_id(quadra_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM quadras WHERE quadra_id = ?", (quadra_id,))
    row = cursor.fetchone()
    conexao.close()
    return dict(row) if row else None

def db_atualizar_quadra(quadra_id, nome, tipo_esporte, preco_hora):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        "UPDATE quadras SET nome = ?, tipo_esporte = ?, preco_hora = ? WHERE quadra_id = ?",
        (nome, tipo_esporte, preco_hora, quadra_id),
    )
    conexao.commit()
    conexao.close()

def db_deletar_quadra(quadra_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM quadras WHERE quadra_id = ?", (quadra_id,))
    conexao.commit()
    conexao.close()

def db_inserir_reserva(quadra_id, usuario_reserva_id, data_hora_inicio, data_hora_fim, valor_total):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute(
        """INSERT INTO reservas (quadra_id, usuario_reserva_id, data_hora_inicio, data_hora_fim, valor_total, status)
           VALUES (?, ?, ?, ?, ?, 'pendente')""",
        (quadra_id, usuario_reserva_id, data_hora_inicio, data_hora_fim, valor_total),
    )
    conexao.commit()
    novo_id = cursor.lastrowid
    conexao.close()
    return novo_id

def db_buscar_reserva_por_id(reserva_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("SELECT * FROM reservas WHERE reserva_id = ?", (reserva_id,))
    row = cursor.fetchone()
    conexao.close()
    return dict(row) if row else None

def db_atualizar_status_reserva(reserva_id, status):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("UPDATE reservas SET status = ? WHERE reserva_id = ?", (status, reserva_id))
    conexao.commit()
    conexao.close()

def db_deletar_reserva(reserva_id):
    conexao = conectar()
    cursor = conexao.cursor()
    cursor.execute("DELETE FROM reservas WHERE reserva_id = ?", (reserva_id,))
    conexao.commit()
    conexao.close()