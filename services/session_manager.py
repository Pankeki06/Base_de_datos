"""Servicio para el manejo de sesión en memoria."""

SESSION_STATE: dict = {}


def guardar_sesion(agente) -> None:
    SESSION_STATE["agente"] = agente


def obtener_agente():
    return SESSION_STATE.get("agente")


def cerrar_sesion() -> None:
    SESSION_STATE.clear()
