"""Vista de lista de asegurados."""

from __future__ import annotations

import flet as ft
from controllers.asegurado_controller import AseguradoController
from controllers.poliza_controller import PolizaController
from services.session_manager import obtener_agente

_BG = "#0F1117"
_CARD = "#1A1D27"
_CARD2 = "#1E2235"
_ACCENT = "#00C17C"
_TEXT = "#E8EAF0"
_MUTED = "#6B7280"
_BORDER = "#2D3148"
_ERROR = "#EF4444"
_WARN = "#F59E0B"
_SIDEBAR = "#13161F"


def _status_badge(polizas: list) -> ft.Container:
    """Returns a colored badge for the most recent policy status."""
    if not polizas:
        label, color, bg = "Sin póliza", _MUTED, ft.Colors.with_opacity(0.12, _MUTED)
    else:
        latest = max(polizas, key=lambda p: p.fecha_vencimiento)
        if latest.estatus == "activa":
            label, color, bg = "Activa", _ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)
        elif latest.estatus == "vencida":
            label, color, bg = "Vencida", _ERROR, ft.Colors.with_opacity(0.12, _ERROR)
        else:
            label = latest.estatus.capitalize()
            label, color, bg = label, _WARN, ft.Colors.with_opacity(0.12, _WARN)
    return ft.Container(
        content=ft.Text(label, size=11, color=color, weight=ft.FontWeight.W_500),
        bgcolor=bg,
        padding=ft.padding.symmetric(horizontal=10, vertical=4),
        border_radius=20,
        border=ft.border.all(1, ft.Colors.with_opacity(0.3, color)),
    )


class ListaAseguradoView:
    def __init__(self, page: ft.Page, navigate) -> None:
        self._page = page
        self._navigate = navigate
        self._agente = obtener_agente()
        self._todos: list = []
        self._polizas_map: dict = {}
        self._list_col = ft.Column(spacing=4, scroll=ft.ScrollMode.AUTO)
        self._empty_state = ft.Container(visible=False)
        self._no_results_state = ft.Container(visible=False)

    def build(self) -> ft.Control:
        self._load_data()
        from views.dashboard_view import _sidebar
        agente = self._agente
        nombre_agente = (f"{agente.nombre} {agente.apellido_paterno}"
                         if agente else "Agente")
        sidebar = _sidebar(self._navigate, "/clientes")
        main = self._build_main()
        return ft.Container(
            content=ft.Row([sidebar, main], spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    # ── Data ─────────────────────────────────────────────────────────────────

    def _load_data(self) -> None:
        agente = self._agente
        if not agente:
            return
        result = AseguradoController.get_asegurados_by_agente(agente.id_agente)
        if result["ok"]:
            self._todos = result["data"]
        for a in self._todos:
            p = PolizaController.get_polizas_by_asegurado(a.id_asegurado)
            self._polizas_map[a.id_asegurado] = p["data"] if p["ok"] else []

    # ── Main panel ────────────────────────────────────────────────────────────

    def _build_main(self) -> ft.Container:
        search_field = ft.TextField(
            hint_text="Buscar por nombre o RFC…",
            hint_style=ft.TextStyle(color=_MUTED, size=14),
            text_style=ft.TextStyle(color=_TEXT, size=14),
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            border_color=_BORDER,
            focused_border_color=_ACCENT,
            bgcolor=_CARD,
            border_radius=10,
            content_padding=ft.padding.symmetric(horizontal=16, vertical=14),
            expand=True,
            on_change=lambda e: self._filter(e.control.value),
        )

        btn_nuevo = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ADD_ROUNDED, size=16, color="#000000"),
                    ft.Text("Nuevo asegurado", size=13,
                            weight=ft.FontWeight.W_600, color="#000000"),
                ],
                spacing=6,
                tight=True,
            ),
            height=46,
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: _ACCENT,
                         ft.ControlState.HOVERED: "#00A86B"},
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.padding.symmetric(horizontal=18, vertical=0),
                elevation={"pressed": 0, "": 1},
            ),
            on_click=lambda e: self._navigate("/asegurado/nuevo"),
        )

        topbar = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Asegurados", size=18,
                            weight=ft.FontWeight.BOLD, color=_TEXT),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=28, vertical=16),
            border=ft.border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

        # Empty state — no asegurados at all
        self._empty_state = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.PERSON_OFF_OUTLINED, size=52, color=_MUTED),
                    ft.Container(height=12),
                    ft.Text("Aún no tienes asegurados registrados",
                            size=16, color=_TEXT,
                            weight=ft.FontWeight.W_500,
                            text_align=ft.TextAlign.CENTER),
                    ft.Text("Agrega tu primer asegurado con el botón de arriba.",
                            size=13, color=_MUTED,
                            text_align=ft.TextAlign.CENTER),
                    ft.Container(height=16),
                    ft.ElevatedButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.ADD_ROUNDED, size=16, color="#000000"),
                                ft.Text("Nuevo asegurado", size=13,
                                        weight=ft.FontWeight.W_600, color="#000000"),
                            ],
                            spacing=6,
                            tight=True,
                        ),
                        height=46,
                        style=ft.ButtonStyle(
                            bgcolor={ft.ControlState.DEFAULT: _ACCENT,
                                     ft.ControlState.HOVERED: "#00A86B"},
                            shape=ft.RoundedRectangleBorder(radius=10),
                            padding=ft.padding.symmetric(horizontal=18, vertical=0),
                        ),
                        on_click=lambda e: self._navigate("/asegurado/nuevo"),
                    ),
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            alignment=ft.Alignment.CENTER,
            visible=False,
        )

        # No results state — search found nothing
        self._no_results_state = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.SEARCH_OFF_ROUNDED, size=48, color=_MUTED),
                    ft.Container(height=12),
                    ft.Text("No se encontraron resultados para ese nombre o RFC",
                            size=15, color=_MUTED,
                            text_align=ft.TextAlign.CENTER),
                ],
                spacing=6,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            expand=True,
            alignment=ft.Alignment.CENTER,
            visible=False,
        )

        # Table header
        header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("NOMBRE", size=10, color=_MUTED,
                            weight=ft.FontWeight.W_600, expand=3),
                    ft.Text("RFC", size=10, color=_MUTED,
                            weight=ft.FontWeight.W_600, expand=2),
                    ft.Text("CELULAR", size=10, color=_MUTED,
                            weight=ft.FontWeight.W_600, expand=2),
                    ft.Text("PÓLIZA", size=10, color=_MUTED,
                            weight=ft.FontWeight.W_600, expand=2),
                ],
                spacing=0,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=10),
            border=ft.border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

        self._render_list(self._todos)

        body = ft.Container(
            content=ft.Stack(
                [
                    ft.Column(
                        [header, self._list_col],
                        spacing=0,
                        expand=True,
                    ),
                    self._empty_state,
                    self._no_results_state,
                ],
                expand=True,
            ),
            expand=True,
        )

        return ft.Container(
            content=ft.Column(
                [
                    topbar,
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [search_field, btn_nuevo],
                                    spacing=12,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Container(height=4),
                                body,
                            ],
                            spacing=12,
                            expand=True,
                        ),
                        padding=ft.padding.symmetric(horizontal=28, vertical=20),
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
            bgcolor=_BG,
        )

    # ── Row builder ───────────────────────────────────────────────────────────

    def _build_row(self, asegurado, polizas: list) -> ft.Container:
        nombre = (f"{asegurado.nombre} {asegurado.apellido_paterno} "
                  f"{asegurado.apellido_materno}".strip())
        celular = asegurado.celular or "—"
        badge = _status_badge(polizas)

        return ft.Container(
            content=ft.Row(
                [
                    ft.Text(nombre, size=14, color=_TEXT,
                            weight=ft.FontWeight.W_500,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            max_lines=1, expand=3),
                    ft.Text(asegurado.rfc, size=13, color=_MUTED,
                            overflow=ft.TextOverflow.ELLIPSIS,
                            max_lines=1, expand=2),
                    ft.Text(celular, size=13, color=_MUTED, expand=2),
                    ft.Row([badge], expand=2),
                ],
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.padding.symmetric(horizontal=20, vertical=14),
            bgcolor=_CARD,
            border_radius=10,
            border=ft.border.all(1, _BORDER),
            on_click=lambda e, aid=asegurado.id_asegurado: self._navigate(
                "/asegurado/detalle", id_asegurado=aid),
            ink=True,
        )

    # ── Filter ────────────────────────────────────────────────────────────────

    def _filter(self, query: str) -> None:
        q = query.strip().lower()
        if not q:
            filtered = self._todos
        else:
            filtered = [
                a for a in self._todos
                if q in f"{a.nombre} {a.apellido_paterno} {a.apellido_materno}".lower()
                or q in a.rfc.lower()
            ]
        self._render_list(filtered, searched=bool(q))
        self._page.update()

    def _render_list(self, asegurados: list, searched: bool = False) -> None:
        self._list_col.controls.clear()
        self._empty_state.visible = False
        self._no_results_state.visible = False

        if not self._todos:
            self._empty_state.visible = True
        elif not asegurados:
            self._no_results_state.visible = True
        else:
            for a in asegurados:
                polizas = self._polizas_map.get(a.id_asegurado, [])
                self._list_col.controls.append(self._build_row(a, polizas))
