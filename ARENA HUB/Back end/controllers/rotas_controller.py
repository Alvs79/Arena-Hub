from flask import jsonify, redirect, render_template, request, url_for
import repositories.consultas_repository as repo
import models.entidades_model as model
import services.regras_service as svc

def init_routes(app):

    # ============================================================
    # PARTE 1 — PAINEL WEB (render_template + Jinja2 + form)
    # ============================================================

    @app.route("/")
    def index():
        totais = repo.repo_contar_totais()
        return render_template(
            "index.html",
            total_usuarios=totais["total_usuarios"],
            total_arenas=totais["total_arenas"],
            total_reservas=totais["total_reservas"],
        )

    @app.route("/usuarios", methods=["GET", "POST"])
    def pagina_usuarios():
        if request.method == "POST":
            nome = request.form["nome"]
            email = request.form["email"]
            senha = request.form["senha"]
            telefone = request.form["telefone"]
            tipo_usuario = request.form["tipo_usuario"]

            model.db_inserir_usuario(nome, email, senha, telefone, tipo_usuario)
            return redirect(url_for("pagina_usuarios"))

        tipo_filtro = request.args.get("tipo")
        usuarios = repo.repo_listar_usuarios(tipo_filtro)
        return render_template("usuarios.html", usuarios=usuarios, tipo_filtro=tipo_filtro)

    @app.route("/usuarios/<int:usuario_id>/excluir", methods=["POST"])
    def excluir_usuario_web(usuario_id):
        model.db_deletar_usuario(usuario_id)
        return redirect(url_for("pagina_usuarios"))

    @app.route("/arenas", methods=["GET", "POST"])
    def pagina_arenas():
        if request.method == "POST":
            model.db_inserir_arena(
                request.form["nome"],
                request.form.get("cnpj"),
                request.form["endereco"],
                request.form["cidade"],
                request.form["dono_id"],
                request.form["taxa_saas"],
            )
            return redirect(url_for("pagina_arenas"))

        arenas = repo.repo_listar_arenas_com_dono()
        donos = repo.repo_listar_usuarios(tipo_filtro="dono")
        return render_template("arenas.html", arenas=arenas, donos=donos)

    @app.route("/arenas/<int:arena_id>/excluir", methods=["POST"])
    def excluir_arena_web(arena_id):
        model.db_deletar_arena(arena_id)
        return redirect(url_for("pagina_arenas"))

    # ============================================================
    # PARTE 2 — API JSON (verbos HTTP + get_json)
    # ============================================================

    @app.route("/api/usuarios", methods=["GET", "POST"])
    def api_usuarios():
        if request.method == "POST":
            dados = request.get_json()
            obrigatorios = ("nome", "email", "senha", "telefone", "tipo_usuario")
            if not dados or not all(dados.get(c) for c in obrigatorios):
                return jsonify({"erro": f"Campos obrigatórios: {', '.join(obrigatorios)}"}), 400

            try:
                novo_id = model.db_inserir_usuario(
                    dados["nome"], dados["email"], dados["senha"], dados["telefone"], dados["tipo_usuario"]
                )
            except Exception as e:
                return jsonify({"erro": f"Falha ao inserir: {e}"}), 400

            usuario = model.db_buscar_usuario_por_id(novo_id)
            if usuario:
                usuario.pop("senha")
            return jsonify(usuario), 201

        tipo = request.args.get("tipo")
        usuarios = [dict(u) for u in repo.repo_listar_usuarios(tipo)]
        for u in usuarios:
            u.pop("senha")
        return jsonify(usuarios), 200

    @app.route("/api/usuarios/<int:usuario_id>", methods=["GET", "PUT", "DELETE"])
    def api_usuario_por_id(usuario_id):
        usuario = model.db_buscar_usuario_por_id(usuario_id)
        if usuario is None:
            return jsonify({"erro": "Usuário não encontrado."}), 404

        if request.method == "GET":
            usuario.pop("senha")
            return jsonify(usuario), 200

        if request.method == "PUT":
            dados = request.get_json()
            if not dados:
                return jsonify({"erro": "Corpo JSON ausente."}), 400
            
            model.db_atualizar_usuario(
                usuario_id,
                dados.get("nome", usuario["nome"]),
                dados.get("email", usuario["email"]),
                dados.get("telefone", usuario["telefone"]),
                dados.get("tipo_usuario", usuario["tipo_usuario"])
            )
            resultado = model.db_buscar_usuario_por_id(usuario_id)
            if resultado:
                resultado.pop("senha")
            return jsonify(resultado), 200

        model.db_deletar_usuario(usuario_id)
        return jsonify({"mensagem": "Usuário deletado com sucesso."}), 200

    @app.route("/api/arenas", methods=["GET", "POST"])
    def api_arenas():
        if request.method == "POST":
            dados = request.get_json()
            obrigatorios = ("nome", "endereco", "cidade", "dono_id", "taxa_saas")
            if not dados or not all(str(dados.get(c, "")) != "" for c in obrigatorios):
                return jsonify({"erro": f"Campos obrigatórios: {', '.join(obrigatorios)}"}), 400

            dono = repo.repo_buscar_tipo_usuario(dados["dono_id"])
            if dono is None or dono["tipo_usuario"] != "dono":
                return jsonify({"erro": "dono_id inválido: usuário não existe ou não é do tipo 'dono'."}), 400

            novo_id = model.db_inserir_arena(
                dados["nome"], dados.get("cnpj"), dados["endereco"], dados["cidade"], dados["dono_id"], dados["taxa_saas"]
            )
            arena = model.db_buscar_arena_por_id(novo_id)
            return jsonify(arena), 201

        cidade = request.args.get("cidade")
        arenas = [dict(a) for a in repo.repo_filtrar_arenas_api(cidade)]
        return jsonify(arenas), 200

    @app.route("/api/arenas/<int:arena_id>", methods=["GET", "PUT", "DELETE"])
    def api_arena_por_id(arena_id):
        arena = model.db_buscar_arena_por_id(arena_id)
        if arena is None:
            return jsonify({"erro": "Arena não encontrada."}), 404

        if request.method == "GET":
            return jsonify(arena), 200

        if request.method == "PUT":
            dados = request.get_json()
            if not dados:
                return jsonify({"erro": "Corpo JSON ausente."}), 400
            
            model.db_atualizar_arena(
                arena_id,
                dados.get("nome", arena["nome"]),
                dados.get("cnpj", arena["cnpj"]),
                dados.get("endereco", arena["endereco"]),
                dados.get("cidade", arena["cidade"]),
                dados.get("taxa_saas", arena["taxa_saas"])
            )
            resultado = model.db_buscar_arena_por_id(arena_id)
            return jsonify(resultado), 200

        model.db_deletar_arena(arena_id)
        return jsonify({"mensagem": "Arena deletada com sucesso."}), 200

    @app.route("/api/quadras", methods=["GET", "POST"])
    def api_quadras():
        if request.method == "POST":
            dados = request.get_json()
            obrigatorios = ("arena_id", "nome", "tipo_esporte", "preco_hora")
            if not dados or not all(str(dados.get(c, "")) != "" for c in obrigatorios):
                return jsonify({"erro": f"Campos obrigatórios: {', '.join(obrigatorios)}"}), 400

            if not repo.repo_verificar_arena_existe(dados["arena_id"]):
                return jsonify({"erro": "Arena informada não existe."}), 400

            novo_id = model.db_inserir_quadra(
                dados["arena_id"], dados["nome"], dados["tipo_esporte"], dados["preco_hora"]
            )
            quadra = model.db_buscar_quadra_por_id(novo_id)
            return jsonify(quadra), 201

        arena_id = request.args.get("arena_id")
        quadras = [dict(q) for q in repo.repo_listar_quadras(arena_id)]
        return jsonify(quadras), 200

    @app.route("/api/quadras/<int:quadra_id>", methods=["GET", "PUT", "DELETE"])
    def api_quadra_por_id(quadra_id):
        quadra = model.db_buscar_quadra_por_id(quadra_id)
        if quadra is None:
            return jsonify({"erro": "Quadra não encontrada."}), 404

        if request.method == "GET":
            return jsonify(quadra), 200

        if request.method == "PUT":
            dados = request.get_json()
            if not dados:
                return jsonify({"erro": "Corpo JSON ausente."}), 400
            
            model.db_atualizar_quadra(
                quadra_id,
                dados.get("nome", quadra["nome"]),
                dados.get("tipo_esporte", quadra["tipo_esporte"]),
                dados.get("preco_hora", quadra["preco_hora"])
            )
            resultado = model.db_buscar_quadra_por_id(quadra_id)
            return jsonify(resultado), 200

        model.db_deletar_quadra(quadra_id)
        return jsonify({"mensagem": "Quadra deletada com sucesso."}), 200

    @app.route("/api/reservas", methods=["GET", "POST"])
    def api_reservas():
        if request.method == "POST":
            dados = request.get_json()
            obrigatorios = ("quadra_id", "usuario_reserva_id", "data_hora_inicio", "data_hora_fim")
            if not dados or not all(dados.get(c) for c in obrigatorios):
                return jsonify({"erro": f"Campos obrigatórios: {', '.join(obrigatorios)}"}), 400

            quadra = repo.repo_buscar_preco_quadra(dados["quadra_id"])
            if quadra is None:
                return jsonify({"erro": "Quadra informada não existe."}), 400

            if repo.repo_verificar_conflito_reserva(dados["quadra_id"], dados["data_hora_inicio"], dados["data_hora_fim"]):
                return jsonify({"erro": "Horário indisponível: já existe reserva nesse período."}), 400

            try:
                valor_total = svc.calcular_valor_reserva(dados["data_hora_inicio"], dados["data_hora_fim"], quadra["preco_hora"])
            except ValueError as e:
                return jsonify({"erro": str(e)}), 400

            novo_id = model.db_inserir_reserva(
                dados["quadra_id"], dados["usuario_reserva_id"], dados["data_hora_inicio"], dados["data_hora_fim"], valor_total
            )
            reserva = model.db_buscar_reserva_por_id(novo_id)
            return jsonify(reserva), 201

        reservas = [dict(r) for r in repo.repo_listar_reservas()]
        return jsonify(reservas), 200

    @app.route("/api/reservas/<int:reserva_id>", methods=["GET", "PUT", "DELETE"])
    def api_reserva_por_id(reserva_id):
        reserva = model.db_buscar_reserva_por_id(reserva_id)
        if reserva is None:
            return jsonify({"erro": "Reserva não encontrada."}), 404

        if request.method == "GET":
            return jsonify(reserva), 200

        if request.method == "PUT":
            dados = request.get_json()
            if not dados or dados.get("status") not in ("pendente", "confirmada"):
                return jsonify({"erro": "Informe status 'pendente' ou 'confirmada'."}), 400
            
            model.db_atualizar_status_reserva(reserva_id, dados["status"])
            resultado = model.db_buscar_reserva_por_id(reserva_id)
            return jsonify(resultado), 200

        model.db_deletar_reserva(reserva_id)
        return jsonify({"mensagem": "Reserva deletada com sucesso."}), 200