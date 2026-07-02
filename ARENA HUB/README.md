# 🏟️ Hub Arena — Flask + SQLite3 + Jinja2

Versão do projeto usando os métodos exigidos pelo professor.

## ✅ Onde cada conceito aparece

| Conceito | Onde está no código |
|----------|---------------------|
| Instanciação do Flask | `app = Flask(__name__)` em `app.py` |
| Decorator `@app.route` | Todas as rotas |
| Método `run` | `app.run(debug=True)` no final de `app.py` |
| `render_template` | Rotas `/`, `/usuarios`, `/arenas` |
| `redirect` + `url_for` | Após POST dos formulários (padrão POST-Redirect-GET) |
| Verbos HTTP (API) | GET, POST, PUT, DELETE em `/api/...` |
| `request.method` | Rotas que aceitam GET e POST juntas |
| `request.get_json` | Todas as rotas `/api/...` (POST/PUT) |
| `request.form` | Formulários das páginas `/usuarios` e `/arenas` |
| `request.args` | Filtros `?tipo=dono` e `?cidade=Betim` |
| sqlite3 `connect` / `cursor` | `database.py` → função `conectar()` |
| `execute` + placeholder `?` | Todos os SELECT/INSERT/UPDATE/DELETE |
| `commit` / `close` | Após toda escrita / fim de toda rota |
| `fetchall` / `fetchone` | Listagens / busca por ID e contadores |
| Jinja2 `{% %}`, `{{ }}`, `{# #}` | `templates/*.html` (herança, for, if, filtros) |

## 🚀 Como rodar

```bash
python -m venv venv
venv\Scripts\activate     # Windows
pip install flask
python app.py
```

- Painel web: http://localhost:5000 (não precisa de React nem Node!)
- API JSON: http://localhost:5000/api/usuarios (teste com Postman/curl)

O arquivo `hub_arena.db` é criado automaticamente na primeira execução.

## 🔌 Rotas da API

| Método | Rota | Descrição |
|--------|------|-----------|
| GET/POST | `/api/usuarios` | Lista (filtro `?tipo=`) / cria |
| GET/PUT/DELETE | `/api/usuarios/<id>` | Busca / atualiza / remove |
| GET/POST | `/api/arenas` | Lista (filtro `?cidade=`) / cria (valida dono) |
| GET/PUT/DELETE | `/api/arenas/<id>` | Busca / atualiza / remove |
| GET/POST | `/api/quadras` | Lista (filtro `?arena_id=`) / cria |
| GET/PUT/DELETE | `/api/quadras/<id>` | Busca / atualiza / remove |
| GET/POST | `/api/reservas` | Lista / cria (anti-overbooking + valor automático) |
| GET/PUT/DELETE | `/api/reservas/<id>` | Busca / muda status / remove |

## 🖥️ Páginas web (Jinja2)

- `/` — visão geral com contadores (fetchone)
- `/usuarios` — tabela + formulário + filtro por tipo (request.form e request.args)
- `/arenas` — tabela com JOIN mostrando o dono + formulário
