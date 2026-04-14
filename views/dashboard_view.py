"""Dashboard principal con paginación básica."""
import flet as ft

from views.home_view import create_home_view
from views.asegurados_view import create_asegurados_view
from views.seguimiento_view import create_seguimiento_view


def create_dashboard_view(page: ft.Page, agente: dict | None = None) -> ft.Column:
    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(label="Inicio"),
            ft.Tab(label="Gestión de Asegurados"),
            ft.Tab(label="Seguimiento"),
            ft.Tab(label="Parte 3"),
            ft.Tab(label="Parte 4"),
        ],
        scrollable=False,
    )

    tab_view = ft.TabBarView(
        controls=[
            create_home_view(page, agente=agente),   # ← nueva primera pestaña
            create_asegurados_view(page),
            create_seguimiento_view(page),
            ft.Column([ft.Text("Parte 3", size=24)], expand=1),
            ft.Column([ft.Text("Parte 4", size=24)], expand=1),
        ],
        expand=1,
    )

    tabs = ft.Tabs(
        content=ft.Column([tab_bar, tab_view], expand=1),
        length=5,
        selected_index=0,
        animation_duration=200,
    )

    return ft.Column(
        [tabs],
        spacing=0,
        expand=True,
        alignment=ft.MainAxisAlignment.START,
    )