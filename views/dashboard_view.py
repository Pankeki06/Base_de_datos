"""Dashboard principal con sidebar, resumen de métricas y tarjetas de asegurados."""

from __future__ import annotations
from datetime import date

import flet as ft
from controllers.asegurado_controller import AseguradoController
from controllers.poliza_controller import PolizaController
from controllers.producto_poliza_controller import ProductoPolizaController
from services.session_manager import obtener_agente, cerrar_sesion
from views.theme import (
    ACCENT as _ACCENT,
    BG as _BG,
    BLUE as _BLUE,
    BORDER as _BORDER,
    CARD as _CARD,
    CARD_ALT as _CARD2,
    ERROR as _ERROR,
    MUTED as _MUTED,
    SIDEBAR as _SIDEBAR,
    TEXT as _TEXT,
    WARN as _WARN,
)
from views.ui_controls import app_sidebar as _app_sidebar, pill as _pill


# ─── Sidebar de navegación lateral (icon-only) ──────────────────────────────
def _sidebar(navigate, ruta_activa: str = "/dashboard") -> ft.Container:
    """Renderiza el sidebar lateral con las opciones de navegación."""
    return _app_sidebar(navigate, ruta_activa)
def _poliza_pills(
    polizas: list,
    producto_map: dict | None = None,
    participaciones: list[dict] | None = None,
) -> list:
    if not polizas:
        participaciones_activas = [
            p
            for p in (participaciones or [])
            if p.get("tipo_participante") != "titular"
            and p.get("estatus_poliza") == "activa"
        ]
        if participaciones_activas:
            return [_pill("Cobertura derivada", _BLUE, ft.Colors.with_opacity(0.12, _BLUE))]

        if participaciones:
            return [_pill("Cobertura derivada vencida", _WARN, ft.Colors.with_opacity(0.12, _WARN))]

        return [_pill("Sin póliza activa", _WARN, ft.Colors.with_opacity(0.12, _WARN))]
    producto_map = producto_map or {}
    pills = []
    tipo_colors = {
        "Vida": (_ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)),
        "Autos": (_BLUE, ft.Colors.with_opacity(0.12, _BLUE)),
        "Hogar": (_WARN, ft.Colors.with_opacity(0.12, _WARN)),
        "Salud": ("#06B6D4", ft.Colors.with_opacity(0.12, "#06B6D4")),
    }
    for p in polizas[:3]:
        prod = producto_map.get(p.id_producto)
        tipo = prod.tipo_seguro if prod else "Otro"
        fg, bg = tipo_colors.get(tipo, (_MUTED, _CARD2))
        label = tipo if p.estatus != "vencida" else f"{tipo} vencida"
        color = _ERROR if p.estatus == "vencida" else fg
        pill_bg = ft.Colors.with_opacity(0.12, _ERROR) if p.estatus == "vencida" else bg
        pills.append(_pill(label, color, pill_bg))
    return pills


# ─── Tarjeta asegurado ────────────────────────────────────────────────────────
def _tarjeta(
    asegurado,
    polizas: list,
    navigate,
    producto_map: dict | None = None,
    participaciones: list[dict] | None = None,
    id_agente_activo: int | None = None,
) -> ft.Container:
    nombre = (f"{asegurado.nombre} {asegurado.apellido_paterno} "
              f"{asegurado.apellido_materno}".strip())
    badges = _poliza_pills(polizas, producto_map, participaciones)
    if id_agente_activo is not None and getattr(asegurado, "id_agente_responsable", None) not in (None, id_agente_activo):
        badges = [
            _pill("Cartera externa", _BLUE, ft.Colors.with_opacity(0.12, _BLUE)),
            *badges,
        ]
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(nombre, size=14, weight=ft.FontWeight.W_600,
                        color=_TEXT, max_lines=1,
                        overflow=ft.TextOverflow.ELLIPSIS),
                ft.Text(asegurado.rfc, size=12, color=_MUTED),
                ft.Container(height=8),
                ft.Row(badges, spacing=6, wrap=True),
            ],
            spacing=3,
        ),
        padding=ft.Padding.symmetric(horizontal=16, vertical=14),
        bgcolor=_CARD,
        border_radius=10,
        border=ft.Border.all(1, _BORDER),
        on_click=lambda e, aid=asegurado.id_asegurado: navigate(
            "/asegurado/detalle", id_asegurado=aid),
        ink=True,
    )


# ─── Vista Dashboard ──────────────────────────────────────────────────────────
class DashboardView:
    def __init__(self, page: ft.Page, navigate) -> None:
        self._page = page
        self._navigate = navigate
        self._agente = obtener_agente()
        self._resultados_ref = ft.Ref[ft.Column]()
        self._recientes_ref = ft.Ref[ft.Column]()

    def build(self) -> ft.Control:
        agente = self._agente
        nombre_agente = (f"{agente.nombre} {agente.apellido_paterno}"
                         if agente else "Agente")

        # Barra de búsqueda
        search_field = ft.TextField(
            hint_text="Buscar por nombre o RFC...",
            hint_style=ft.TextStyle(color=_MUTED, size=15),
            text_style=ft.TextStyle(color=_TEXT, size=15),
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            border_color=_BORDER,
            focused_border_color=_ACCENT,
            bgcolor=_CARD,
            border_radius=10,
            content_padding=ft.Padding.symmetric(horizontal=16, vertical=16),
            expand=True,
            on_change=lambda e: self._on_search_change(e.control.value),
        )

        # Sección resultados de búsqueda (oculta inicialmente)
        resultados_col = ft.Column(
            ref=self._resultados_ref,
            spacing=12,
            visible=False,
        )

        # Sección recientes
        recientes_grid = self._build_recientes()

        # KPIs
        kpis = self._build_kpis()

        # Topbar
        topbar = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Inicio", size=18,
                            weight=ft.FontWeight.BOLD, color=_TEXT),
                    ft.Container(expand=True),
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    ft.Icons.PERSON_ROUNDED,
                                    size=18,
                                    color=_TEXT,
                                ),
                                width=36, height=36, border_radius=18,
                                bgcolor=_BLUE,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Text(nombre_agente, size=14, color=_TEXT),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=28, vertical=16),
            border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

        # Cuerpo con scroll
        cuerpo = ft.Container(
            content=ft.Column(
                [
                    search_field,
                    # Resultados búsqueda
                    resultados_col,
                    # Recientes (se ocultan al buscar)
                    ft.Column(
                        ref=self._recientes_ref,
                        controls=[
                            ft.Container(height=4),
                            ft.Text("CONTACTADOS RECIENTEMENTE", size=11,
                                    weight=ft.FontWeight.W_600, color=_MUTED),
                            ft.Container(height=6),
                            recientes_grid,
                            ft.Container(height=20),
                            ft.Text("RESUMEN DEL EQUIPO", size=11,
                                    weight=ft.FontWeight.W_600, color=_MUTED),
                            ft.Container(height=6),
                            kpis,
                        ],
                        spacing=0,
                    ),
                ],
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=ft.Padding.symmetric(horizontal=28, vertical=20),
            expand=True,
        )

        main = ft.Container(
            content=ft.Column(
                [topbar, cuerpo],
                spacing=0,
                expand=True,
            ),
            expand=True,
            bgcolor=_BG,
        )

        return ft.Container(
            content=ft.Row([_sidebar(self._navigate), main],
                           spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    def _on_search_change(self, query: str) -> None:
        res_col = self._resultados_ref.current
        rec_col = self._recientes_ref.current
        if not res_col or not rec_col:
            return
        query = query.strip()
        if not query:
            res_col.visible = False
            res_col.controls.clear()
            rec_col.visible = True
            self._page.update()
            return

        res = AseguradoController.search_asegurados(query)
        asegurados = res.get("data", []) if res["ok"] else []

        res_col.controls.clear()
        res_col.controls.append(
            ft.Text("RESULTADOS", size=11, weight=ft.FontWeight.W_600, color=_MUTED)
        )
        if not asegurados:
            res_col.controls.append(
                ft.Text("Sin resultados para esa búsqueda.", color=_MUTED, size=13)
            )
        else:
            prod_res = ProductoPolizaController.get_all_productos()
            producto_map = (
                {p.id_producto: p for p in prod_res.get("data", [])}
                if prod_res["ok"] else {}
            )
            cards = []
            for a in asegurados[:20]:
                pol_res = PolizaController.get_polizas_by_asegurado(a.id_asegurado)
                pols = pol_res.get("data", []) if pol_res["ok"] else []
                part_res = PolizaController.get_participaciones_by_asegurado(a.id_asegurado)
                participaciones = part_res.get("data", []) if part_res["ok"] else []
                cards.append(
                    ft.Container(
                        content=_tarjeta(
                            a,
                            pols,
                            self._navigate,
                            producto_map,
                            participaciones,
                            self._agente.id_agente if self._agente else None,
                        ),
                        col={"xs": 12, "sm": 6, "md": 4},
                    )
                )
            res_col.controls.append(
                ft.ResponsiveRow(cards, spacing=12, run_spacing=12)
            )

        res_col.visible = True
        rec_col.visible = False
        self._page.update()

    def _build_recientes(self) -> ft.Control:
        agente = self._agente
        if not agente:
            return ft.Text("Sin sesión activa.", color=_MUTED, size=13)

        try:
            from repositories.seguimiento_contacto_repository import SeguimientoContactoRepository
            from repositories.seguimiento_repository import SeguimientoRepository
            contactos = SeguimientoContactoRepository.get_all()
            segs = {s.id_seguimiento: s for s in SeguimientoRepository.get_all()}
        except Exception:
            return ft.Text("Sin contactos recientes.", color=_MUTED, size=13)

        vistos: set[int] = set()
        ids_rec: list[int] = []
        for c in sorted(contactos, key=lambda x: x.fecha_hora, reverse=True):
            seg = segs.get(c.id_seguimiento)
            if not seg or seg.id_agente != agente.id_agente:
                continue
            if seg.id_asegurado not in vistos:
                vistos.add(seg.id_asegurado)
                ids_rec.append(seg.id_asegurado)
            if len(ids_rec) == 6:
                break

        if not ids_rec:
            return ft.Text("Sin contactos recientes.", color=_MUTED, size=13)

        cards = []
        prod_res = ProductoPolizaController.get_all_productos()
        producto_map = (
            {p.id_producto: p for p in prod_res.get("data", [])}
            if prod_res["ok"] else {}
        )
        for aid in ids_rec:
            a_res = AseguradoController.get_asegurado_by_id(aid)
            if not a_res["ok"]:
                continue
            a = a_res["data"]
            pol_res = PolizaController.get_polizas_by_asegurado(aid)
            pols = pol_res.get("data", []) if pol_res["ok"] else []
            part_res = PolizaController.get_participaciones_by_asegurado(aid)
            participaciones = part_res.get("data", []) if part_res["ok"] else []
            cards.append(
                ft.Container(
                    content=_tarjeta(
                        a,
                        pols,
                        self._navigate,
                        producto_map,
                        participaciones,
                        agente.id_agente,
                    ),
                    col={"xs": 12, "sm": 6, "md": 4},
                )
            )

        return ft.ResponsiveRow(cards, spacing=12, run_spacing=12)

    def _build_kpis(self) -> ft.Control:
        agente = self._agente
        id_agente = agente.id_agente if agente else None

        try:
            from repositories.seguimiento_repository import SeguimientoRepository
            from datetime import timedelta

            a_res = (AseguradoController.get_asegurados_by_agente(id_agente)
                     if id_agente else {"ok": False})
            asegurados = list(a_res.get("data", [])) if a_res["ok"] else []
            total_asegurados = len(asegurados)

            from repositories.seguimiento_contacto_repository import SeguimientoContactoRepository
            contactos = SeguimientoContactoRepository.get_all()
            segs = {s.id_seguimiento: s for s in SeguimientoRepository.get_all()}
            hoy = date.today()
            segs_hoy = sum(
                1 for c in contactos
                if (seg := segs.get(c.id_seguimiento))
                and seg.id_agente == id_agente
                and c.fecha_hora.date() == hoy
            )

            limite = hoy + timedelta(days=30)
            por_vencer = 0
            for asegurado in asegurados:
                pol_res = PolizaController.get_polizas_by_asegurado(asegurado.id_asegurado)
                if not pol_res["ok"]:
                    continue
                por_vencer += sum(
                    1 for poliza in pol_res.get("data", [])
                    if poliza.estatus == "activa" and poliza.fecha_vencimiento <= limite
                )
        except Exception:
            total_asegurados = segs_hoy = por_vencer = 0

        def _kpi(valor, etiqueta) -> ft.Container:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text(str(valor), size=32,
                                weight=ft.FontWeight.BOLD, color=_TEXT),
                        ft.Text(etiqueta, size=13, color=_MUTED),
                    ],
                    spacing=4,
                ),
                padding=ft.Padding.symmetric(horizontal=20, vertical=18),
                bgcolor=_CARD, border_radius=10,
                border=ft.Border.all(1, _BORDER),
                col={"xs": 12, "sm": 4},
            )

        return ft.ResponsiveRow(
            [
                _kpi(total_asegurados, "Asegurados activos"),
                _kpi(segs_hoy, "Seguimientos hoy"),
                _kpi(por_vencer, "Pólizas por vencer"),
            ],
            spacing=12, run_spacing=12,
        )

