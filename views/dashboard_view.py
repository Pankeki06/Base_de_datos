"""Dashboard principal con paginación básica."""

import flet as ft


def create_dashboard_view(page: ft.Page) -> ft.Column:
    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(label="Parte 1"),
            ft.Tab(label="Parte 2"),
            ft.Tab(label="Parte 3"),
        ],
        scrollable=False,
    )

    tab_view = ft.TabBarView(
        controls=[
            ft.Column([ft.Text("Parte 1", size=24)], expand=1),
            ft.Column([ft.Text("Parte 2", size=24)], expand=1),
            ft.Column([ft.Text("Parte 3", size=24)], expand=1),
        ],
        expand=1,
    )

    tabs = ft.Tabs(
        content=ft.Column([tab_bar, tab_view], expand=1),
        length=3,
        selected_index=0,
        animation_duration=200,
    )

    return ft.Column(
        [
            ft.Text("Dashboard de la aplicación", size=28),
            ft.Text(
                "Navega entre las secciones usando la paginación de pestañas.",
                size=16,
            ),
            tabs,
        ],
        spacing=20,
        alignment=ft.MainAxisAlignment.START,
    )
