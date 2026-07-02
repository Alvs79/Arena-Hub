CREATE TABLE IF NOT EXISTS usuarios (
    usuario_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    nome         TEXT NOT NULL,
    email        TEXT NOT NULL UNIQUE,
    senha        TEXT NOT NULL,
    telefone     TEXT NOT NULL,
    tipo_usuario TEXT NOT NULL CHECK (tipo_usuario IN ('atleta','dono','professor')),
    data_criacao TEXT NOT NULL DEFAULT (date('now'))
);

CREATE TABLE IF NOT EXISTS arenas (
    arena_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    nome      TEXT NOT NULL,
    cnpj      TEXT,
    endereco  TEXT NOT NULL,
    cidade    TEXT NOT NULL,
    dono_id   INTEGER NOT NULL,
    taxa_saas REAL NOT NULL,
    FOREIGN KEY (dono_id) REFERENCES usuarios (usuario_id)
);

CREATE TABLE IF NOT EXISTS quadras (
    quadra_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    arena_id     INTEGER NOT NULL,
    nome         TEXT NOT NULL,
    tipo_esporte TEXT NOT NULL,
    preco_hora   REAL NOT NULL,
    FOREIGN KEY (arena_id) REFERENCES arenas (arena_id)
);

CREATE TABLE IF NOT EXISTS reservas (
    reserva_id         INTEGER PRIMARY KEY AUTOINCREMENT,
    quadra_id          INTEGER NOT NULL,
    usuario_reserva_id INTEGER NOT NULL,
    data_hora_inicio   TEXT NOT NULL,
    data_hora_fim      TEXT NOT NULL,
    valor_total        REAL NOT NULL,
    status             TEXT NOT NULL DEFAULT 'pendente',
    FOREIGN KEY (quadra_id) REFERENCES quadras (quadra_id),
    FOREIGN KEY (usuario_reserva_id) REFERENCES usuarios (usuario_id)
);