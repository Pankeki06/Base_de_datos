"""Punto de entrada de la aplicación."""

import flet as ft
from views.login_view import create_login_view


def main(page: ft.Page) -> None:
    page.title = "Gestión de seguros"
    page.window_width = 900
    page.window_height = 650
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.add(create_login_view(page))


if __name__ == "__main__":
    try:
        ft.run(main)
    except KeyboardInterrupt:
        print("Aplicación cerrada correctamente")