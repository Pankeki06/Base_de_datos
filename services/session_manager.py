"""Servicio para el manejo de sesión en memoria."""

import threading

_lock: threading.Lock = threading.Lock()
SESSION_STATE: dict = {}


def guardar_sesion(agente) -> None:
    with _lock:
        SESSION_STATE["agente"] = agente


def obtener_agente():
    with _lock:
        return SESSION_STATE.get("agente")


def cerrar_sesion() -> None:
    with _lock:
        SESSION_STATE.clear()
