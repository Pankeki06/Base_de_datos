"""Dashboard principal con paginación básica."""
import flet as ft

# Importamos la nueva vista que crearemos
from views.asegurados_view import create_asegurados_view

def create_dashboard_view(page: ft.Page) -> ft.Column:
    tab_bar = ft.TabBar(
        tabs=[
            ft.Tab(label="Gestión de Asegurados"), # Cambiamos el nombre
            ft.Tab(label="Parte 2"),
            ft.Tab(label="Parte 3"),
            ft.Tab(label="Parte 4")
        ],
        scrollable=False,
    )

    tab_view = ft.TabBarView(
        controls=[
            # Llamamos a nuestra nueva vista aquí y le pasamos la página
            create_asegurados_view(page), 
            ft.Column([ft.Text("Parte 2", size=24)], expand=1),
            ft.Column([ft.Text("Parte 3", size=24)], expand=1),
            ft.Column([ft.Text("Parte 4", size=24)], expand=1),
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