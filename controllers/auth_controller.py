"""Controlador de autenticación y login."""

import flet as ft
from services.auth_service import authenticate, login_agente
from views.dashboard_view import create_dashboard_view
from views.login_view import create_login_view as login_view


class AuthController:
    @staticmethod
    def login(clave_agente: str, password: str) -> dict:
        try:
            agente = login_agente(clave_agente, password)
            if not agente:
                return {"ok": False, "error": "Clave o contraseña incorrecta."}
            return {"ok": True, "data": agente}
        except Exception as e:
            return {"ok": False, "error": str(e)}


def create_login_view(page: ft.Page) -> ft.Column:
    """Crea la vista de login y gestiona la lógica de autenticación."""
    def handle_login(clave: str, pwd: str, validation_text: ft.Text, page: ft.Page) -> None:
        if not clave or not pwd:
            validation_text.value = "Debe ingresar clave y contraseña."
            page.update()
            return

        if authenticate(clave, pwd):
            page.controls.clear()
            page.add(create_dashboard_view(page))
        else:
            validation_text.value = "Clave o contraseña incorrecta."
            page.update()

    return login_view (page, handle_login)
