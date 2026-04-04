"""Servicio para el manejo de sesión en memoria."""

SESSION_STATE = {}


def guardar_sesion(agente_id: str) -> None:
    SESSION_STATE["agente"] = agente_id
    print(f"Sesión guardada para agente: {agente_id}")
