"""Vista de login."""

import flet as ft
from controllers.auth_controller import AuthController
from views.dashboard_view import create_dashboard_view


def create_login_view(page: ft.Page) -> ft.Column:
    """Crea la interfaz de login. La vista decide qué hacer según el resultado del controller."""
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    clave_agente = ft.TextField(
        label="Clave de agente",
        width=320,
        autofocus=True,
    )
    password = ft.TextField(
        label="Contraseña",
        password=True,
        can_reveal_password=True,
        width=320,
    )
    validation_text = ft.Text(color="red")

    def on_login(event: ft.ControlEvent) -> None:
        # La vista llama al controller con los datos
        result = AuthController.login(clave_agente.value, password.value)

        if result["ok"]:
            page.controls.clear()
            page.add(create_dashboard_view(page))
        else:
            validation_text.value = result["error"]
            page.update()

    return ft.Column(
        controls=[
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text("Login de agente", size=28, weight=ft.FontWeight.BOLD),
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
                    spacing=16,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                width=420,
                padding=24,
                border_radius=12,
                bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST,
            )
        ],
        expand=True,
        alignment=ft.MainAxisAlignment.CENTER,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )