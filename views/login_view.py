"""Vista de login."""

import flet as ft


def create_login_view(page: ft.Page, on_login_callback) -> ft.Column:
    """Crea la interfaz de login con campos de entrada y validación."""
    clave_agente = ft.TextField(
        label="Clave de agente",
        width=320,
    )
    password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=320,
    )
    validation_text = ft.Text(color="red")

    def on_login(event: ft.ControlEvent) -> None:
        on_login_callback(clave_agente.value, password.value, validation_text, page)

    return ft.Column(
        [
            ft.Text("Login de agente", size=28, weight="bold"),
            ft.Divider(),
            clave_agente,
            password,
            ft.ElevatedButton(
                content=ft.Text("Entrar"),
                on_click=on_login,
                width=320,
            ),
            validation_text,
        ],
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        spacing=16,
    )
