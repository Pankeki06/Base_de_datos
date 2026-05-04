"""Vista de detalle de asegurado."""

from __future__ import annotations

import flet as ft
from controllers.agente_controller import AgenteController
from controllers.asegurado_controller import AseguradoController
from controllers.beneficio_controller import BeneficioController
from controllers.beneficiario_controller import BeneficiarioController
from controllers.poliza_controller import PolizaController
from controllers.producto_beneficio_controller import ProductoBeneficioController
from controllers.producto_poliza_controller import ProductoPolizaController
from controllers.seguimiento_controller import SeguimientoController
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
from views.ui_controls import app_sidebar, modal_dialog, pill as _pill, styled_dropdown as _dd, styled_text_field as _tf

_PART_STYLE = {
    "titular":    ("Titular",     _ACCENT, ft.Colors.with_opacity(0.12, _ACCENT), ft.Colors.with_opacity(0.35, _ACCENT)),
    "conyuge":    ("Conyuge",     _BLUE,   ft.Colors.with_opacity(0.14, _BLUE),   ft.Colors.with_opacity(0.25, _BLUE)),
    "hijo":       ("Hijo",        _WARN,   ft.Colors.with_opacity(0.14, _WARN),   ft.Colors.with_opacity(0.25, _WARN)),
    "dependiente":("Dependiente", _MUTED,  _CARD2,                                ft.Colors.with_opacity(0.20, _MUTED)),
}


def _sidebar(navigate) -> ft.Container:
    return app_sidebar(navigate, "/clientes")


# ─── Helpers ──────────────────────────────────────────────────────────────────
def _campo(etiqueta: str, valor: str) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(etiqueta.upper(), size=10, color=_MUTED,
                        weight=ft.FontWeight.W_600),
                ft.Container(height=2),
                ft.Text(valor or "—", size=14, color=_TEXT),
            ],
            spacing=0,
        ),
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        bgcolor=_CARD,
        border_radius=8,
        border=ft.Border.all(1, _BORDER),
        col={"xs": 12, "sm": 6},
    )


def _campo_full(etiqueta: str, valor: str) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(etiqueta.upper(), size=10, color=_MUTED,
                        weight=ft.FontWeight.W_600),
                ft.Container(height=2),
                ft.Text(valor or "—", size=14, color=_TEXT),
            ],
            spacing=0,
        ),
        padding=ft.Padding.symmetric(horizontal=16, vertical=12),
        bgcolor=_CARD,
        border_radius=8,
        border=ft.Border.all(1, _BORDER),
        col={"xs": 12},
    )
# ─── Vista detalle ─────────────────────────────────────────────────────────────
class DetalleAseguradoView:
    def __init__(self, page: ft.Page, navigate, id_asegurado: int) -> None:
        self._page     = page
        self._navigate = navigate
        self._id       = id_asegurado

        self._asegurado    = None
        self._agente       = None
        self._polizas      = []
        self._participaciones_poliza: list[dict] = []
        self._poliza_rol_map: dict[int, str] = {}
        self._beneficiarios = []
        self._beneficiarios_map: dict[int | None, list] = {}
        self._beneficios_map: dict[int, list] = {}
        self._producto_beneficios_map: dict[int, list] = {}
        self._seguimientos = []
        self._producto_map: dict = {}
        self._productos_activos = []
        self._seg_col_ref = ft.Ref[ft.Column]()

    def _show_dialog(self, dialog: ft.AlertDialog) -> None:
        self._page.show_dialog(dialog)

    def _close_dialog(self, dialog: ft.AlertDialog | None = None) -> None:
        self._page.pop_dialog()

    def _go_to_asignaciones(
        self,
        *,
        focus_poliza_id: int | None = None,
        focus_tab: str | None = None,
    ) -> None:
        kwargs = {"id_asegurado": self._id}
        if focus_poliza_id is not None:
            kwargs["focus_poliza_id"] = focus_poliza_id
        if focus_tab is not None:
            kwargs["focus_tab"] = focus_tab
        self._navigate("/asegurado/asignaciones", **kwargs)

    # ── Carga de datos ────────────────────────────────────────────────────────

    def _load_data(self) -> None:
        res = AseguradoController.get_asegurado_by_id(self._id)
        if not res["ok"]:
            return
        self._asegurado = res["data"]

        if self._asegurado.id_agente_responsable:
            ag_res = AgenteController.get_agente_by_id(
                self._asegurado.id_agente_responsable)
            self._agente = ag_res.get("data") if ag_res["ok"] else None
        else:
            self._agente = None

        self._load_polizas_relacionadas()

        prod_res = ProductoPolizaController.get_all_productos()
        self._producto_map = (
            {p.id_producto: p for p in prod_res.get("data", [])}
            if prod_res["ok"] else {}
        )
        activos_res = ProductoPolizaController.get_productos_activos()
        self._productos_activos = (
            list(activos_res.get("data", []))
            if activos_res["ok"]
            else list(self._producto_map.values())
        )

        self._producto_beneficios_map = {}
        for producto in self._producto_map.values():
            beneficios_catalogo_res = ProductoBeneficioController.get_beneficios_by_producto(producto.id_producto)
            self._producto_beneficios_map[producto.id_producto] = list(
                beneficios_catalogo_res.get("data", []) if beneficios_catalogo_res["ok"] else []
            )

        self._beneficios_map = {}
        for poliza in self._polizas:
            beneficios_res = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
            self._beneficios_map[poliza.id_poliza] = list(
                beneficios_res.get("data", []) if beneficios_res["ok"] else []
            )

        ben_res = BeneficiarioController.get_beneficiarios_by_asegurado(self._id)
        self._beneficiarios = list(ben_res.get("data", []) if ben_res["ok"] else [])
        self._beneficiarios_map = {}
        for beneficiario in self._beneficiarios:
            self._beneficiarios_map.setdefault(getattr(beneficiario, "id_poliza", None), []).append(beneficiario)

        seg_res = SeguimientoController.get_seguimientos_by_asegurado(self._id)
        self._seguimientos = seg_res.get("data", []) if seg_res["ok"] else []

    def _load_polizas_relacionadas(self) -> None:
        """Carga polizas del asegurado como titular y como participante."""
        pol_res = PolizaController.get_polizas_by_asegurado(self._id)
        polizas_titular = pol_res.get("data", []) if pol_res["ok"] else []

        part_res = PolizaController.get_participaciones_by_asegurado(self._id)
        self._participaciones_poliza = part_res.get("data", []) if part_res["ok"] else []

        poliza_map: dict[int, object] = {p.id_poliza: p for p in polizas_titular}
        self._poliza_rol_map = {p.id_poliza: "titular" for p in polizas_titular}

        for part in self._participaciones_poliza:
            pid = part.get("id_poliza")
            if not pid:
                continue
            role = part.get("tipo_participante") or "titular"
            self._poliza_rol_map[pid] = role
            if pid not in poliza_map:
                p_res = PolizaController.get_poliza_by_id(pid)
                if p_res.get("ok") and p_res.get("data") is not None:
                    poliza_map[pid] = p_res["data"]

        self._polizas = sorted(
            poliza_map.values(),
            key=lambda p: str(getattr(p, "fecha_vencimiento", "")),
            reverse=True,
        )

    def build(self) -> ft.Control:
        self._load_data()
        if self._asegurado is None:
            return ft.Container(
                content=ft.Text("Asegurado no encontrado.", color=_ERROR, size=14),
                expand=True, bgcolor=_BG,
                alignment=ft.Alignment.CENTER,
            )
        return ft.Container(
            content=ft.Row(
                [_sidebar(self._navigate), self._build_main()],
                spacing=0, expand=True,
            ),
            expand=True,
            bgcolor=_BG,
        )

    # ── Panel principal ───────────────────────────────────────────────────────

    def _build_main(self) -> ft.Container:
        a      = self._asegurado
        nombre = f"{a.nombre} {a.apellido_paterno} {a.apellido_materno}".strip()
        iniciales = (a.nombre[0] + a.apellido_paterno[0]).upper()

        topbar = ft.Container(
            content=ft.Row(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                                                size=14, color=_TEXT),
                                width=32, height=32, border_radius=8,
                                bgcolor=_CARD2, alignment=ft.Alignment.CENTER,
                                on_click=lambda e: self._navigate("/clientes"),
                                tooltip="Volver",
                            ),
                            ft.Text("Detalle de asegurado", size=16,
                                    weight=ft.FontWeight.W_600, color=_TEXT),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(expand=True),
                    ft.OutlinedButton(
                        content=ft.Row(
                            [ft.Icon(ft.Icons.TUNE_ROUNDED, size=15),
                             ft.Text("Asignaciones", size=13)],
                            spacing=6,
                        ),
                        style=ft.ButtonStyle(
                            color=_TEXT,
                            side={ft.ControlState.DEFAULT: ft.BorderSide(1, _BORDER)},
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=lambda e: self._navigate(
                            "/asegurado/asignaciones", id_asegurado=self._id),
                    ),
                    ft.OutlinedButton(
                        content=ft.Row(
                            [ft.Icon(ft.Icons.ADD_ROUNDED, size=15),
                             ft.Text("Nuevo seguimiento", size=13)],
                            spacing=6,
                        ),
                        style=ft.ButtonStyle(
                            color=_TEXT,
                            side={ft.ControlState.DEFAULT: ft.BorderSide(1, _BORDER)},
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=lambda e: self._open_seguimiento_modal(),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=24, vertical=14),
            border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

        info_card = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Text(iniciales, size=18,
                                        weight=ft.FontWeight.BOLD, color=_TEXT),
                        width=52, height=52, border_radius=26,
                        bgcolor=_CARD2, alignment=ft.Alignment.CENTER,
                    ),
                    ft.Column(
                        [
                            ft.Text(nombre, size=18,
                                    weight=ft.FontWeight.BOLD, color=_TEXT),
                            ft.Text(
                                f"{a.rfc}  ·  {a.celular or 'sin telefono'}",
                                size=13, color=_MUTED,
                            ),
                            ft.Row(
                                [
                                    ft.Icon(ft.Icons.BADGE_OUTLINED,
                                            size=13, color=_MUTED),
                                    ft.Text(
                                        (
                                            f"{self._agente.nombre} "
                                            f"{self._agente.apellido_paterno}"
                                            if self._agente
                                            else "Sin agente asignado"
                                        ),
                                        size=12, color=_MUTED,
                                    ),
                                ],
                                spacing=4,
                            ),
                        ],
                        spacing=3, expand=True,
                    ),
                    ft.OutlinedButton(
                        content=ft.Text("Editar", size=13, color=_TEXT),
                        style=ft.ButtonStyle(
                            side={ft.ControlState.DEFAULT: ft.BorderSide(1, _BORDER)},
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=lambda e: self._navigate(
                            "/asegurado/editar", asegurado=self._asegurado),
                    ),
                ],
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=20, vertical=16),
            bgcolor=_CARD, border_radius=10,
            border=ft.Border.all(1, _BORDER),
        )

        tab_views = [
            self._tab_datos(),
            self._tab_polizas(),
            self._tab_beneficiarios(),
            self._tab_seguimientos(),
        ]
        tabs = ft.Tabs(
            selected_index=0,
            animation_duration=150,
            expand=True,
            length=len(tab_views),
            content=ft.Column(
                [
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Datos"),
                            ft.Tab(label="Polizas"),
                            ft.Tab(label="Beneficiarios"),
                            ft.Tab(label="Seguimientos"),
                        ],
                        tab_alignment=ft.TabAlignment.START,
                        indicator_color=_ACCENT,
                        label_color=_TEXT,
                        unselected_label_color=_MUTED,
                    ),
                    ft.TabBarView(
                        controls=tab_views,
                        expand=True,
                    ),
                ],
                expand=True,
            ),
        )

        return ft.Container(
            content=ft.Column(
                [
                    topbar,
                    ft.Container(
                        content=ft.Column(
                            [info_card, ft.Container(height=4), tabs],
                            spacing=12, expand=True,
                        ),
                        padding=ft.Padding.symmetric(horizontal=24, vertical=16),
                        expand=True,
                    ),
                ],
                spacing=0, expand=True,
            ),
            expand=True,
            bgcolor=_BG,
        )

    # ── Tab: Datos ────────────────────────────────────────────────────────────

    def _tab_datos(self) -> ft.Container:
        a = self._asegurado
        domicilio = (
            f"{a.calle} {a.numero_exterior}"
            + (f" Int.{a.numero_interior}" if a.numero_interior else "")
            + f", Col. {a.colonia}, {a.municipio}, {a.estado}, C.P. {a.codigo_postal}"
        )
        fn = str(getattr(a, "fecha_nacimiento", None) or "")
        return ft.Container(
            content=ft.Column(
                [
                    ft.ResponsiveRow(
                        [
                            _campo("Correo", a.correo),
                            _campo("Celular", a.celular),
                            _campo("RFC", a.rfc),
                            _campo("Fecha de nacimiento", fn),
                            _campo_full("Domicilio", domicilio),
                        ],
                        spacing=10, run_spacing=10,
                    ),
                ],
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=ft.Padding.only(top=16),
            expand=True,
        )

    # ── Tab: Polizas ──────────────────────────────────────────────────────────

    def _tab_polizas(self) -> ft.Container:
        if not self._polizas:
            polizas_content = ft.Column(self._pol_cards(), spacing=10)
        else:
            selected_poliza_id = self._polizas[0].id_poliza
            selected_poliza_state = {"id": selected_poliza_id}
            poliza_selector_buttons: list[tuple[int, ft.FilledButton]] = []
            active_poliza_content = ft.Container()

            def _poliza_selector_style(*, active: bool) -> ft.ButtonStyle:
                return ft.ButtonStyle(
                    bgcolor=_ACCENT if active else _CARD2,
                    color="#000000" if active else _TEXT,
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(1, _ACCENT if active else _BORDER)
                    },
                    shape=ft.RoundedRectangleBorder(radius=10),
                )

            def _sync_selected_poliza(selected_value: int | None = None, *, update_page: bool = True) -> None:
                if selected_value is None:
                    selected_value = selected_poliza_state["id"]
                selected_poliza_state["id"] = int(selected_value)

                poliza = next(
                    (item for item in self._polizas if item.id_poliza == selected_poliza_state["id"]),
                    None,
                )
                active_poliza_content.content = self._build_poliza_card(poliza) if poliza is not None else None
                for poliza_id, button in poliza_selector_buttons:
                    button.style = _poliza_selector_style(active=poliza_id == selected_poliza_state["id"])

                if update_page:
                    self._page.update()

            selector_row = ft.Row(spacing=12, wrap=True)
            for poliza in self._polizas:
                button = ft.FilledButton(
                    poliza.numero_poliza,
                    style=_poliza_selector_style(active=poliza.id_poliza == selected_poliza_id),
                    on_click=lambda e, poliza_id=poliza.id_poliza: _sync_selected_poliza(poliza_id),
                )
                poliza_selector_buttons.append((poliza.id_poliza, button))
                selector_row.controls.append(button)

            _sync_selected_poliza(update_page=False)
            polizas_content = ft.Column(
                [
                    ft.Text("Poliza en trabajo", size=12, color=_MUTED),
                    selector_row,
                    active_poliza_content,
                ],
                spacing=10,
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Polizas", size=15,
                                    weight=ft.FontWeight.W_600, color=_TEXT),
                            ft.Container(expand=True),
                        ],
                    ),
                    ft.Divider(color=_BORDER, height=8),
                    ft.Text(
                        "Las altas, cambios y bajas de pólizas se gestionan desde Asignaciones para evitar duplicar formularios.",
                        size=12,
                        color=_MUTED,
                    ),
                    polizas_content,
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=ft.Padding.only(top=16),
            expand=True,
        )

    def _pol_cards(self) -> list:
        return [self._build_poliza_card(poliza) for poliza in self._polizas] or [
            ft.Container(
                content=ft.Text(
                    "Sin pólizas registradas o vinculadas.",
                    color=_MUTED,
                    size=13,
                ),
                padding=ft.Padding.symmetric(horizontal=16, vertical=16),
                bgcolor=_CARD,
                border_radius=10,
                border=ft.Border.all(1, _BORDER),
            )
        ]

    def _build_poliza_card(self, poliza) -> ft.Container:
        estatus_colors = {
            "activa": (_ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)),
            "vencida": (_ERROR, ft.Colors.with_opacity(0.12, _ERROR)),
            "cancelada": (_MUTED, _CARD2),
        }
        tipo_icons = {
            "Vida": ft.Icons.FAVORITE_ROUNDED,
            "Autos": ft.Icons.DIRECTIONS_CAR_ROUNDED,
            "Hogar": ft.Icons.HOME_ROUNDED,
            "Salud": ft.Icons.LOCAL_HOSPITAL_ROUNDED,
            "Gastos Medicos Mayores": ft.Icons.LOCAL_HOSPITAL_ROUNDED,
            "Accidentes Personales": ft.Icons.EMERGENCY_ROUNDED,
        }
        fg, bg = estatus_colors.get(poliza.estatus, (_MUTED, _CARD2))
        producto = self._producto_map.get(poliza.id_producto)
        tipo_seguro = producto.tipo_seguro if producto else "Otro"
        nombre_producto = producto.nombre if producto else poliza.numero_poliza
        role = self._poliza_rol_map.get(poliza.id_poliza, "titular")
        role_label, role_fg, role_bg, _ = _PART_STYLE.get(role, _PART_STYLE["dependiente"])

        prima_mensual = getattr(poliza, "prima_mensual", None)
        if isinstance(prima_mensual, (int, float)):
            prima_text = f"${prima_mensual:,.2f}"
        else:
            prima_text = str(prima_mensual or "—")

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(
                                    tipo_icons.get(tipo_seguro, ft.Icons.SHIELD_ROUNDED),
                                    size=18,
                                    color=fg,
                                ),
                                width=36,
                                height=36,
                                border_radius=8,
                                bgcolor=bg,
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    ft.Text(nombre_producto, size=15,
                                            weight=ft.FontWeight.W_600, color=_TEXT),
                                    ft.Row(
                                        [
                                            ft.Text(poliza.numero_poliza, size=12, color=_MUTED),
                                            _pill(role_label, role_fg, role_bg),
                                            _pill(poliza.estatus.capitalize(), fg, bg),
                                        ],
                                        spacing=8,
                                        wrap=True,
                                    ),
                                ],
                                spacing=6,
                                expand=True,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    ft.ResponsiveRow(
                        [
                            _campo("Inicio", str(getattr(poliza, "fecha_inicio", "") or "—")),
                            _campo("Vencimiento", str(getattr(poliza, "fecha_vencimiento", "") or "—")),
                            _campo("Prima mensual", prima_text),
                            _campo("Relacion", "Titular" if role == "titular" else role_label),
                        ],
                        spacing=10,
                        run_spacing=10,
                    ),
                    ft.Divider(color=_BORDER, height=8),
                    ft.Text(
                        "Beneficios incluidos (solo lectura)",
                        size=12,
                        color=_MUTED,
                        weight=ft.FontWeight.W_600,
                    ),
                    *self._beneficio_rows(poliza),
                    ft.Text(
                        "La administración operativa de esta póliza se realiza desde Asignaciones.",
                        size=12,
                        color=_MUTED,
                    ),
                ],
                spacing=12,
            ),
            padding=ft.Padding.symmetric(horizontal=16, vertical=14),
            bgcolor=_CARD,
            border_radius=10,
            border=ft.Border.all(1, _BORDER),
        )

    def _beneficio_rows(self, poliza) -> list[ft.Control]:
        emitidos = list(self._beneficios_map.get(poliza.id_poliza, []))
        if emitidos:
            rows = []
            for beneficio in emitidos:
                monto = float(getattr(beneficio, "monto_cobertura", 0) or 0)
                rows.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(beneficio.nombre_beneficio, size=13, color=_TEXT, weight=ft.FontWeight.W_600),
                                        ft.Text(beneficio.descripcion or "Sin descripcion", size=12, color=_MUTED),
                                    ],
                                    spacing=3,
                                    expand=True,
                                ),
                                ft.Column(
                                    [
                                        ft.Text(f"${monto:,.2f}", size=13, color=_ACCENT, weight=ft.FontWeight.W_600),
                                        _pill(
                                            "Vigente" if getattr(beneficio, "vigente", True) else "No vigente",
                                            _ACCENT if getattr(beneficio, "vigente", True) else _MUTED,
                                            ft.Colors.with_opacity(0.12, _ACCENT if getattr(beneficio, "vigente", True) else _MUTED),
                                        ),
                                    ],
                                    spacing=4,
                                    horizontal_alignment=ft.CrossAxisAlignment.END,
                                ),
                            ],
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                        padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                        border=ft.Border.all(1, _BORDER),
                        border_radius=8,
                        bgcolor=_CARD2,
                    )
                )
            return rows

        beneficios_catalogo = [
            beneficio
            for beneficio in self._producto_beneficios_map.get(poliza.id_producto, [])
            if getattr(beneficio, "incluido_base", False) and getattr(beneficio, "activo", True)
        ]
        if beneficios_catalogo:
            rows = []
            for beneficio in beneficios_catalogo:
                monto = float(getattr(beneficio, "monto_cobertura", 0) or 0)
                rows.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Column(
                                    [
                                        ft.Text(beneficio.nombre_beneficio, size=13, color=_TEXT, weight=ft.FontWeight.W_600),
                                        ft.Text(beneficio.descripcion or "Sin descripcion", size=12, color=_MUTED),
                                    ],
                                    spacing=3,
                                    expand=True,
                                ),
                                ft.Column(
                                    [
                                        ft.Text(f"${monto:,.2f}", size=13, color=_ACCENT, weight=ft.FontWeight.W_600),
                                        _pill("Base", _BLUE, ft.Colors.with_opacity(0.12, _BLUE)),
                                    ],
                                    spacing=4,
                                    horizontal_alignment=ft.CrossAxisAlignment.END,
                                ),
                            ],
                            spacing=10,
                            vertical_alignment=ft.CrossAxisAlignment.START,
                        ),
                        padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                        border=ft.Border.all(1, _BORDER),
                        border_radius=8,
                        bgcolor=_CARD2,
                    )
                )
            return rows

        return [
            ft.Container(
                content=ft.Text(
                    "Sin beneficios registrados para esta póliza.",
                    size=12,
                    color=_MUTED,
                ),
                padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                bgcolor=_CARD2,
                border_radius=8,
                border=ft.Border.all(1, _BORDER),
            )
        ]

    # ── Tab: Beneficiarios ────────────────────────────────────────────────────

    def _tab_beneficiarios(self) -> ft.Container:
        polizas_con_beneficiarios = sum(
            1 for poliza in self._polizas if self._beneficiarios_map.get(poliza.id_poliza)
        )
        resumen_t = ft.Text(
            f"Beneficiarios cargados: {len(self._beneficiarios)} · Polizas con beneficiarios: {polizas_con_beneficiarios}",
            size=12,
            color=_MUTED,
        )

        poliza_cards: list[ft.Control] = []
        if self._polizas:
            selected_poliza_id = self._polizas[0].id_poliza
            selected_poliza_state = {"id": selected_poliza_id}
            poliza_selector_buttons: list[tuple[int, ft.FilledButton]] = []
            active_poliza_content = ft.Container()

            def _poliza_selector_style(*, active: bool) -> ft.ButtonStyle:
                return ft.ButtonStyle(
                    bgcolor=_ACCENT if active else _CARD2,
                    color="#000000" if active else _TEXT,
                    side={
                        ft.ControlState.DEFAULT: ft.BorderSide(1, _ACCENT if active else _BORDER)
                    },
                    shape=ft.RoundedRectangleBorder(radius=10),
                )

            def _sync_selected_poliza(selected_value: int | None = None, *, update_page: bool = True) -> None:
                if selected_value is None:
                    selected_value = selected_poliza_state["id"]
                selected_poliza_state["id"] = int(selected_value)

                poliza = next(
                    (item for item in self._polizas if item.id_poliza == selected_poliza_state["id"]),
                    None,
                )
                active_poliza_content.content = (
                    self._beneficiario_poliza_card(poliza) if poliza is not None else None
                )
                for poliza_id, button in poliza_selector_buttons:
                    button.style = _poliza_selector_style(active=poliza_id == selected_poliza_state["id"])

                if update_page:
                    self._page.update()

            selector_row = ft.Row(spacing=12, wrap=True)
            for poliza in self._polizas:
                button = ft.FilledButton(
                    poliza.numero_poliza,
                    style=_poliza_selector_style(active=poliza.id_poliza == selected_poliza_id),
                    on_click=lambda e, poliza_id=poliza.id_poliza: _sync_selected_poliza(poliza_id),
                )
                poliza_selector_buttons.append((poliza.id_poliza, button))
                selector_row.controls.append(button)

            _sync_selected_poliza(update_page=False)
            poliza_cards.extend(
                [
                    ft.Text("Poliza en trabajo", size=12, color=_MUTED),
                    selector_row,
                    active_poliza_content,
                ]
            )

        legacy_beneficiarios = self._beneficiarios_map.get(None, [])
        if legacy_beneficiarios:
            poliza_cards.append(self._beneficiario_legacy_card(legacy_beneficiarios))
        if not poliza_cards:
            poliza_cards.append(
                ft.Container(
                    content=ft.Text(
                        "Sin beneficiarios registrados.",
                        color=_MUTED,
                        size=13,
                    ),
                    padding=ft.Padding.symmetric(horizontal=14, vertical=16),
                    bgcolor=_CARD2,
                    border_radius=10,
                    border=ft.Border.all(1, _BORDER),
                )
            )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Beneficiarios", size=15,
                                    weight=ft.FontWeight.W_600, color=_TEXT),
                            ft.Container(expand=True),
                        ],
                    ),
                    resumen_t,
                    ft.Divider(color=_BORDER, height=8),
                    ft.Text(
                        "Los beneficiarios ahora se consultan separados por póliza. La edición se mantiene en Asignaciones para conservar una sola superficie operativa.",
                        size=12,
                        color=_MUTED,
                    ),
                    *poliza_cards,
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=ft.Padding.only(top=16),
            expand=True,
        )

    def _beneficiario_poliza_card(self, poliza) -> ft.Container:
        beneficiarios = self._beneficiarios_map.get(poliza.id_poliza, [])
        total = sum(beneficiario.porcentaje_participacion for beneficiario in beneficiarios)
        producto = self._producto_map.get(poliza.id_producto)
        role = self._poliza_rol_map.get(poliza.id_poliza, "titular")
        role_label = _PART_STYLE.get(role, _PART_STYLE["dependiente"])[0]
        rows = self._ben_rows(beneficiarios, focus_poliza_id=poliza.id_poliza)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(
                                                f"Poliza {poliza.numero_poliza}",
                                                size=14,
                                                weight=ft.FontWeight.W_600,
                                                color=_TEXT,
                                            ),
                                            _pill(
                                                producto.nombre if producto else poliza.numero_poliza,
                                                _ACCENT,
                                                ft.Colors.with_opacity(0.12, _ACCENT),
                                            ),
                                            _pill(
                                                role_label,
                                                _BLUE,
                                                ft.Colors.with_opacity(0.12, _BLUE),
                                            ),
                                        ],
                                        spacing=8,
                                        wrap=True,
                                    ),
                                    ft.Text(
                                        f"{poliza.fecha_inicio} -> {poliza.fecha_vencimiento}",
                                        size=12,
                                        color=_MUTED,
                                    ),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.Text(
                                        f"Total asignado en esta poliza: {total:.0f}%",
                                        size=12,
                                        color=_ERROR if total > 100 else _ACCENT,
                                        text_align=ft.TextAlign.RIGHT,
                                    ),
                                ],
                                spacing=2,
                                horizontal_alignment=ft.CrossAxisAlignment.END,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    ft.Divider(color=_BORDER, height=10),
                    *rows,
                ],
                spacing=8,
            ),
            padding=ft.Padding.symmetric(horizontal=14, vertical=14),
            bgcolor=_CARD2,
            border_radius=10,
            border=ft.Border.all(1, _BORDER),
        )

    def _beneficiario_legacy_card(self, beneficiarios: list) -> ft.Container:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                "Beneficiarios sin póliza asignada",
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=_TEXT,
                            ),
                            ft.Container(expand=True),
                        ],
                        spacing=12,
                    ),
                    ft.Text(
                        "Estos registros permanecen visibles hasta que les asignes una póliza desde Asignaciones.",
                        size=12,
                        color=_MUTED,
                    ),
                    ft.Divider(color=_BORDER, height=10),
                    *self._ben_rows(beneficiarios, focus_poliza_id=None),
                ],
                spacing=8,
            ),
            padding=ft.Padding.symmetric(horizontal=14, vertical=14),
            bgcolor=_CARD2,
            border_radius=10,
            border=ft.Border.all(1, _BORDER),
        )

    def _ben_rows(self, beneficiarios: list, *, focus_poliza_id: int | None) -> list:
        rows = []
        for beneficiario in beneficiarios:
            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text(beneficiario.nombre_completo, size=13, color=_TEXT, weight=ft.FontWeight.W_600),
                                    ft.Text(
                                        f"{beneficiario.parentesco} | {beneficiario.telefono or 'Sin telefono'}",
                                        size=12,
                                        color=_MUTED,
                                    ),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                            ft.Text(
                                f"{beneficiario.porcentaje_participacion:.0f}%",
                                size=13,
                                color=_ACCENT,
                                weight=ft.FontWeight.W_600,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=10),
                    border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
                    bgcolor=_CARD,
                )
            )

        if not rows:
            rows.append(
                ft.Container(
                    content=ft.Text("Sin beneficiarios registrados.",
                                    color=_MUTED, size=13),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=16),
                    bgcolor=_CARD,
                )
            )
        return rows

    # ── Tab: Seguimientos ─────────────────────────────────────────────────────

    def _tab_seguimientos(self) -> ft.Container:
        seg_col = ft.Column(ref=self._seg_col_ref, spacing=0)
        seg_col.controls.extend(self._seg_items())

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Historial", size=15,
                                    weight=ft.FontWeight.W_600, color=_TEXT),
                        ],
                    ),
                    ft.Divider(color=_BORDER, height=8),
                    ft.Container(
                        content=seg_col,
                        bgcolor=_CARD,
                        border_radius=10,
                        border=ft.Border.all(1, _BORDER),
                    ),
                ],
                spacing=8, scroll=ft.ScrollMode.AUTO, expand=True,
            ),
            padding=ft.Padding.only(top=16),
            expand=True,
        )

    def _seg_items(self) -> list:
        resultado_colors = {
            "resuelto":     (_ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)),
            "pendiente":    (_WARN,   ft.Colors.with_opacity(0.12, _WARN)),
            "sin_respuesta": (_MUTED, _CARD2),
        }
        tipo_icons = {
            "llamada": ft.Icons.PHONE_ROUNDED,
            "visita":  ft.Icons.PERSON_ROUNDED,
            "mensaje": ft.Icons.MESSAGE_ROUNDED,
        }
        items = []
        for s in sorted(self._seguimientos, key=lambda x: x.fecha_hora, reverse=True):
            fg, bg = resultado_colors.get(s.resultado, (_MUTED, _CARD2))
            icon   = tipo_icons.get(s.tipo_contacto, ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED)
            items.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(icon, size=15, color=_ACCENT),
                                width=34, height=34, border_radius=8,
                                bgcolor=ft.Colors.with_opacity(0.12, _ACCENT),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(str(s.fecha_hora.date()),
                                                    size=11, color=_MUTED),
                                            _pill(s.tipo_contacto.capitalize(),
                                                  _MUTED, _CARD2),
                                            _pill(s.resultado.replace("_", " ").upper(),
                                                  fg, bg),
                                        ],
                                        spacing=8,
                                    ),
                                    ft.Text(s.observaciones, size=13, color=_TEXT),
                                ],
                                spacing=4, expand=True,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                    border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
                )
            )
        if not items:
            items.append(
                ft.Container(
                    content=ft.Text("Sin seguimientos registrados.",
                                    color=_MUTED, size=13),
                    padding=ft.Padding.symmetric(horizontal=16, vertical=16),
                )
            )
        return items

    # ── Modal: nuevo seguimiento ──────────────────────────────────────────────

    def _open_seguimiento_modal(self) -> None:
        agente    = obtener_agente()
        tipo_dd   = _dd("Tipo de contacto", [
            ft.dropdown.Option(key="llamada", text="Llamada"),
            ft.dropdown.Option(key="visita",  text="Visita"),
            ft.dropdown.Option(key="mensaje", text="Mensaje"),
        ])
        res_dd    = _dd("Resultado", [
            ft.dropdown.Option(key="resuelto",     text="Resuelto"),
            ft.dropdown.Option(key="pendiente",    text="Pendiente"),
            ft.dropdown.Option(key="sin_respuesta", text="Sin respuesta"),
        ])
        obs_f     = _tf("Observaciones", multiline=True, min_lines=2, max_lines=4)
        fecha_f   = _tf("Fecha y hora", hint_text="AAAA-MM-DD HH:MM")
        err_t     = ft.Text("", color=_ERROR, size=12)

        def _save(e):
            from datetime import datetime as dt
            try:
                fecha_hora = dt.strptime(fecha_f.value.strip(), "%Y-%m-%d %H:%M")
            except (ValueError, AttributeError):
                err_t.value = "Formato invalido. Use AAAA-MM-DD HH:MM."
                self._page.update(); return
            if not tipo_dd.value or not res_dd.value:
                err_t.value = "Selecciona tipo y resultado."
                self._page.update(); return
            if agente is None:
                err_t.value = "No hay una sesión activa. No se puede registrar el seguimiento."
                self._page.update()
                return
            r = SeguimientoController.create_seguimiento({
                "id_asegurado": self._id,
                "id_agente":    agente.id_agente,
                "tipo_contacto": tipo_dd.value,
                "resultado":    res_dd.value,
                "observaciones": obs_f.value,
                "fecha_hora":   fecha_hora,
            })
            if r["ok"]:
                self._close_dialog(dlg)
                seg_res = SeguimientoController.get_seguimientos_by_asegurado(self._id)
                self._seguimientos = (
                    seg_res.get("data", []) if seg_res["ok"] else []
                )
                col = self._seg_col_ref.current
                if col is not None:
                    col.controls.clear()
                    col.controls.extend(self._seg_items())
                    self._page.update()
            else:
                err_t.value = r.get("error", "Error al guardar.")
                self._page.update()

        dlg = modal_dialog(
            "Nuevo seguimiento",
            ft.Column(
                [
                    tipo_dd,
                    res_dd,
                    obs_f,
                    fecha_f,
                    ft.Text("Usa el formato AAAA-MM-DD HH:MM.", size=11, color=_MUTED),
                    err_t,
                ],
                spacing=12,
                tight=True,
            ),
            [
                ft.TextButton(
                    "Cancelar",
                    style=ft.ButtonStyle(color=_MUTED),
                    on_click=lambda e: self._close_dialog(dlg),
                ),
                ft.FilledButton(
                    "Guardar",
                    style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"),
                    on_click=_save,
                ),
            ],
            width=440,
        )
        self._show_dialog(dlg)
