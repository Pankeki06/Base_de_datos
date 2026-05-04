"""Punto de entrada de la aplicación."""

import flet as ft
from views.theme import BG


def main(page: ft.Page) -> None:
    page.title = "The Architectural Trust — Insurance Portal"
    page.window.width = 1100
    page.window.height = 720
    page.window.min_width = 900
    page.window.min_height = 650
    page.bgcolor = ft.Colors.with_opacity(1, BG)
    page.padding = 0

    def navigate(route: str, **kwargs) -> None:
        """Navega a una ruta reemplazando el contenido de la página."""
        page.controls.clear()
        if route == "/login":
            from views.login_view import LoginView
            page.add(LoginView(page, navigate).build())
        elif route == "/dashboard":
            from views.dashboard_view import DashboardView
            page.add(DashboardView(page, navigate).build())
        elif route == "/asegurado/detalle":
            from views.asegurado.detalle_view import DetalleAseguradoView
            id_asegurado = kwargs.get("id_asegurado")
            page.add(DetalleAseguradoView(page, navigate, id_asegurado).build())
        elif route == "/asegurado/asignaciones":
            from views.asegurado.asignaciones_view import AsignacionesAseguradoView
            id_asegurado = kwargs.get("id_asegurado")
            focus_poliza_id = kwargs.get("focus_poliza_id")
            focus_tab = kwargs.get("focus_tab")
            page.add(
                AsignacionesAseguradoView(
                    page,
                    navigate,
                    id_asegurado,
                    focus_poliza_id=focus_poliza_id,
                    focus_tab=focus_tab,
                ).build()
            )
        elif route == "/clientes":
            from views.asegurado.lista_view import ListaAseguradoView
            page.add(ListaAseguradoView(page, navigate).build())
        elif route == "/polizas":
            from views.polizas.lista_view import ListaPolizasView
            page.add(ListaPolizasView(page, navigate).build())
        elif route == "/agentes":
            from views.agentes.lista_view import ListaAgentesView
            page.add(ListaAgentesView(page, navigate).build())
        elif route == "/asegurado/nuevo":
            from views.asegurado.formulario_view import FormularioAseguradoView
            page.add(FormularioAseguradoView(page, navigate, asegurado=None).build())
        elif route == "/asegurado/editar":
            from views.asegurado.formulario_view import FormularioAseguradoView
            asegurado = kwargs.get("asegurado")
            page.add(FormularioAseguradoView(page, navigate, asegurado=asegurado).build())
        page.update()

    navigate("/login")


if __name__ == "__main__":
    ft.run(main)
