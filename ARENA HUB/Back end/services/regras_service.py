# regras_service.py
from datetime import datetime

def validar_dono(cursor, dono_id):
    """Verifica se o dono existe e possui o tipo correto."""
    cursor.execute("SELECT tipo_usuario FROM usuarios WHERE usuario_id = ?", (dono_id,))
    dono = cursor.fetchone()
    if dono is None:
        return False, "dono_id inválido: usuário não existe."
    if dono["tipo_usuario"] != "dono":
        return False, "dono_id inválido: usuário não é do tipo 'dono'."
    return True, ""


def verificar_conflito_reserva(cursor, quadra_id, inicio_str, fim_str):
    """Garante que não haja sobreposição de horários na mesma quadra."""
    cursor.execute(
        """SELECT reserva_id FROM reservas
           WHERE quadra_id = ?
             AND data_hora_inicio < ?
             AND data_hora_fim > ?""",
        (quadra_id, fim_str, inicio_str),
    )
    if cursor.fetchone() is not None:
        return True, "Horário indisponível: já existe reserva nesse período."
    return False, ""


def calcular_valor_reserva(preco_hora, inicio_str, fim_str):
    """Valida as datas recebidas e calcula o valor baseado no tempo decorrido."""
    try:
        inicio = datetime.fromisoformat(inicio_str)
        fim = datetime.fromisoformat(fim_str)
    except ValueError:
        return None, "Formato de data/hora inválido. Use o padrão ISO (Ex: 2026-07-01T14:00:00)."

    if fim <= inicio:
        return None, "A data/hora de fim deve ser posterior à data/hora de início."

    horas = (fim - inicio).total_seconds() / 3600
    valor_total = round(horas * preco_hora, 2)
    return valor_total, ""