"""Vista de detalle de asegurado."""

from __future__ import annotations

import flet as ft
from controllers.asegurado_controller import AseguradoController
from controllers.beneficiario_controller import BeneficiarioController
from controllers.beneficio_controller import BeneficioController
from controllers.poliza_controller import PolizaController
from controllers.seguimiento_controller import SeguimientoController
from services.session_manager import obtener_agente, cerrar_sesion

_BG = "#0F1117"
_SIDEBAR = "#13161F"
_CARD = "#1A1D27"
_CARD2 = "#1E2235"
_ACCENT = "#00C17C"
_TEXT = "#E8EAF0"
_MUTED = "#6B7280"
_BORDER = "#2D3148"
_ERROR = "#EF4444"
_WARN = "#F59E0B"
_BLUE = "#3B82F6"


# ─── Sidebar (reutiliza misma lógica que dashboard) ──────────────────────────
def _sidebar(navigate) -> ft.Container:
    def _on_logout(e):
        cerrar_sesion()
        navigate("/login")

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(height=16),
                ft.Container(
                    content=ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=22, color=_MUTED),
                    width=48, height=48, border_radius=10,
                    bgcolor=ft.Colors.TRANSPARENT,
                    alignment=ft.Alignment.CENTER,
                    tooltip="Inicio",
                    on_click=lambda e: navigate("/dashboard"),
                ),
                ft.Container(height=4),
                ft.Container(
                    content=ft.Icon(ft.Icons.PERSON_OUTLINE_ROUNDED, size=20,
                                    color=_TEXT),
                    width=48, height=48, border_radius=10,
                    bgcolor=_CARD2,
                    alignment=ft.Alignment.CENTER,
                    tooltip="Clientes",
                ),
                ft.Container(
                    content=ft.Icon(ft.Icons.MENU_ROUNDED, size=20, color=_MUTED),
                    width=48, height=48, border_radius=10,
                    bgcolor=ft.Colors.TRANSPARENT,
                    alignment=ft.Alignment.CENTER,
                    tooltip="Pólizas",
                ),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Icon(ft.Icons.WB_SUNNY_OUTLINED, size=18, color=_MUTED),
                    width=48, height=48, border_radius=10,
                    bgcolor=ft.Colors.TRANSPARENT,
                    alignment=ft.Alignment.CENTER,
                    tooltip="Ajustes",
                ),
                ft.Container(height=4),
                ft.Container(
                    content=ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=18, color=_MUTED),
                    width=48, height=48, border_radius=10,
                    bgcolor=ft.Colors.TRANSPARENT,
                    alignment=ft.Alignment.CENTER,
                    tooltip="Cerrar sesión",
                    on_click=_on_logout,
                ),
                ft.Container(height=12),
            ],
            spacing=4,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True,
        ),
        width=64,
        bgcolor=_SIDEBAR,
        border=ft.border.only(right=ft.BorderSide(1, _BORDER)),
    )


# ─── Helpers ─────────────────────────────────────────────────────────────────
def _campo(etiqueta: str, valor: str) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(etiqueta.upper(), size=10,
                        color=_MUTED, weight=ft.FontWeight.W_600),
                ft.Container(height=2),
                ft.Text(valor or "—", size=14, color=_TEXT),
            ],
            spacing=0,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor=_CARD,
        border_radius=8,
        border=ft.border.all(1, _BORDER),
        col={"xs": 12, "sm": 6},
    )


def _campo_full(etiqueta: str, valor: str) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(etiqueta.upper(), size=10,
                        color=_MUTED, weight=ft.FontWeight.W_600),
                ft.Container(height=2),
                ft.Text(valor or "—", size=14, color=_TEXT),
            ],
            spacing=0,
        ),
        padding=ft.padding.symmetric(horizontal=16, vertical=12),
        bgcolor=_CARD,
        border_radius=8,
        border=ft.border.all(1, _BORDER),
        col={"xs": 12},
    )


def _pill(label: str, color: str, bg: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(label, size=11, color=color, weight=ft.FontWeight.W_500),
        bgcolor=bg,
        padding=ft.padding.symmetric(horizontal=8, vertical=3),
        border_radius=20,
        border=ft.border.all(1, ft.Colors.with_opacity(0.25, color)),
    )


# ─── Vista detalle ────────────────────────────────────────────────────────────
class DetalleAseguradoView:
    def __init__(self, page: ft.Page, navigate, id_asegurado: int) -> None:
        self._page = page
        self._navigate = navigate
        self._id = id_asegurado
        self._asegurado = None
        self._polizas = []
        self._beneficiarios = []
        self._seguimientos = []
        self._seg_col_ref = ft.Ref[ft.Column]()
        self._ben_col_ref = ft.Ref[ft.Column]()

    def build(self) -> ft.Control:
        res = AseguradoController.get_asegurado_by_id(self._id)
        if not res["ok"]:
            return ft.Container(
                content=ft.Text("Asegurado no encontrado.", color=_ERROR, size=14),
                expand=True, bgcolor=_BG, alignment=ft.Alignment.CENTER,
            )
        self._asegurado = res["data"]

        pol_res = PolizaController.get_polizas_by_asegurado(self._id)
        self._polizas = pol_res.get("data", []) if pol_res["ok"] else []

        ben_res = BeneficiarioController.get_beneficiarios_by_asegurado(self._id)
        self._beneficiarios = list(ben_res.get("data", []) if ben_res["ok"] else [])

        seg_res = SeguimientoController.get_seguimientos_by_asegurado(self._id)
        self._seguimientos = seg_res.get("data", []) if seg_res["ok"] else []

        return ft.Container(
            content=ft.Row(
                [_sidebar(self._navigate), self._build_main()],
                spacing=0, expand=True,
            ),
            expand=True,
            bgcolor=_BG,
        )

    def _build_main(self) -> ft.Container:
        a = self._asegurado
        nombre = f"{a.nombre} {a.apellido_paterno} {a.apellido_materno}".strip()
        iniciales = (a.nombre[0] + a.apellido_paterno[0]).upper()

        # ── Header superior (topbar)
        topbar = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(
                                    content=ft.Icon(ft.Icons.ARROW_BACK_IOS_NEW_ROUNDED,
                                                    size=14, color=_TEXT),
                                    width=32, height=32, border_radius=8,
                                    bgcolor=_CARD2,
                                    alignment=ft.Alignment.CENTER,
                                    on_click=lambda e: self._navigate("/dashboard"),
                                    tooltip="Volver",
                                ),
                                ft.Text("Detalle de asegurado", size=16,
                                        weight=ft.FontWeight.W_600, color=_TEXT),
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                    ),
                    ft.Container(expand=True),
                    ft.OutlinedButton(
                        content=ft.Row(
                            [ft.Icon(ft.Icons.ADD_ROUNDED, size=15),
                             ft.Text("+ Nuevo seguimiento", size=13)],
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
            padding=ft.padding.symmetric(horizontal=24, vertical=14),
            border=ft.border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

        # ── Tarjeta de identidad del asegurado
        avatar = ft.Container(
            content=ft.Text(iniciales, size=18,
                            weight=ft.FontWeight.BOLD, color=_TEXT),
            width=52, height=52, border_radius=26,
            bgcolor=_CARD2,
            alignment=ft.Alignment.CENTER,
        )

        info_card = ft.Container(
            content=ft.Row(
                [
                    avatar,
                    ft.Column(
                        [
                            ft.Text(nombre, size=18,
                                    weight=ft.FontWeight.BOLD, color=_TEXT),
                            ft.Text(
                                f"{a.rfc}  ·  {a.celular or 'sin teléfono'}",
                                size=13, color=_MUTED,
                            ),
                        ],
                        spacing=4,
                        expand=True,
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
            padding=ft.padding.symmetric(horizontal=20, vertical=16),
            bgcolor=_CARD,
            border_radius=10,
            border=ft.border.all(1, _BORDER),
        )

        # ── Tabs
        tab_bar = ft.TabBar(
            tabs=[
                ft.Tab(label="Datos"),
                ft.Tab(label="Pólizas"),
                ft.Tab(label="Beneficiarios"),
                ft.Tab(label="Seguimientos"),
            ],
            tab_alignment=ft.TabAlignment.START,
            indicator_color=_ACCENT,
            label_color=_TEXT,
            unselected_label_color=_MUTED,
        )

        tab_view = ft.TabBarView(
            controls=[
                self._tab_datos(),
                self._tab_polizas(),
                self._tab_beneficiarios(),
                self._tab_seguimientos(),
            ],
            expand=1,
        )

        tabs = ft.Tabs(
            content=ft.Column([tab_bar, tab_view], expand=1, spacing=0),
            length=4,
            selected_index=0,
            animation_duration=150,
        )

        return ft.Container(
            content=ft.Column(
                [
                    topbar,
                    ft.Container(
                        content=ft.Column(
                            [info_card, ft.Container(height=4), tabs],
                            spacing=12,
                            expand=True,
                        ),
                        padding=ft.padding.symmetric(horizontal=24, vertical=16),
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
            bgcolor=_BG,
        )

    # ── Tab Datos ─────────────────────────────────────────────────────────────
    def _tab_datos(self) -> ft.Container:
        a = self._asegurado
        domicilio = (f"{a.calle} {a.numero_exterior}"
                     + (f" Int.{a.numero_interior}" if a.numero_interior else "")
                     + f", Col. {a.colonia}, {a.municipio}, {a.estado}, {a.codigo_postal}")

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
            expand=True,
        )

    # ── Tab Pólizas ───────────────────────────────────────────────────────────
    def _tab_polizas(self) -> ft.Container:
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
        }

        cards = []
        for p in self._polizas:
            fg, bg = estatus_colors.get(p.estatus, (_MUTED, _CARD2))
            b_res = BeneficioController.get_beneficios_by_poliza(p.id_poliza)
            bens = b_res.get("data", []) if b_res["ok"] else []
            cards.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Icon(
                                            tipo_icons.get(p.tipo_seguro,
                                                           ft.Icons.SHIELD_ROUNDED),
                                            size=18, color=fg,
                                        ),
                                        width=36, height=36, border_radius=8,
                                        bgcolor=bg,
                                        alignment=ft.Alignment.CENTER,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Text(p.tipo_seguro, size=14,
                                                            weight=ft.FontWeight.W_600,
                                                            color=_TEXT),
                                                    _pill(p.estatus.upper(), fg, bg),
                                                ],
                                                spacing=8,
                                            ),
                                            ft.Text(p.numero_poliza, size=11,
                                                    color=_MUTED),
                                        ],
                                        spacing=2, expand=True,
                                    ),
                                    ft.Text(f"${p.prima_mensual:,.0f}/mes",
                                            size=14, weight=ft.FontWeight.BOLD,
                                            color=_TEXT),
                                ],
                                spacing=12,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            ft.Divider(color=_BORDER, height=12),
                            ft.Text(
                                f"{p.fecha_inicio}  →  {p.fecha_vencimiento}",
                                size=12, color=_MUTED,
                            ),
                            *[
                                ft.Row(
                                    [
                                        ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                                size=13, color=_ACCENT),
                                        ft.Text(b.nombre_beneficio, size=13,
                                                color=_TEXT, expand=True),
                                        ft.Text(f"${b.monto_cobertura:,.0f}",
                                                size=12, color=_MUTED),
                                    ],
                                    spacing=8,
                                )
                                for b in bens
                            ],
                        ],
                        spacing=6,
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=14),
                    bgcolor=_CARD,
                    border_radius=10,
                    border=ft.border.all(1, _BORDER),
                )
            )

        return ft.Container(
            content=ft.Column(
                cards or [ft.Text("Sin pólizas registradas.", color=_MUTED, size=13)],
                spacing=12,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            expand=True,
        )

    # ── Tab Beneficiarios ─────────────────────────────────────────────────────
    def _tab_beneficiarios(self) -> ft.Container:
        ben_col = ft.Column(ref=self._ben_col_ref, spacing=0)
        ben_col.controls.extend(self._ben_rows())

        total = sum(b.porcentaje_participacion for b in self._beneficiarios)
        pct_text = ft.Text(
            f"Total asignado: {total:.0f}%",
            size=12,
            color=_ERROR if total > 100 else _ACCENT,
        )

        def refresh():
            r = BeneficiarioController.get_beneficiarios_by_asegurado(self._id)
            self._beneficiarios = list(r.get("data", []) if r["ok"] else [])
            t = sum(b.porcentaje_participacion for b in self._beneficiarios)
            pct_text.value = f"Total asignado: {t:.0f}%"
            pct_text.color = _ERROR if t > 100 else _ACCENT
            col = self._ben_col_ref.current
            col.controls.clear()
            col.controls.extend(self._ben_rows(refresh))
            self._page.update()

        ben_col.controls.clear()
        ben_col.controls.extend(self._ben_rows(refresh))

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text("Beneficiarios", size=15,
                                    weight=ft.FontWeight.W_600, color=_TEXT),
                            ft.Container(expand=True),
                            ft.ElevatedButton(
                                content=ft.Row(
                                    [ft.Icon(ft.Icons.PERSON_ADD_ROUNDED, size=14),
                                     ft.Text("Agregar", size=13)],
                                    spacing=6,
                                ),
                                style=ft.ButtonStyle(
                                    bgcolor={ft.ControlState.DEFAULT: _ACCENT},
                                    color={ft.ControlState.DEFAULT: "#000000"},
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda e: self._open_ben_modal(refresh),
                            ),
                        ],
                    ),
                    pct_text,
                    ft.Divider(color=_BORDER, height=8),
                    # Cabecera tabla
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Text("Nombre", expand=3, size=11,
                                        color=_MUTED, weight=ft.FontWeight.W_600),
                                ft.Text("Parentesco", expand=2, size=11,
                                        color=_MUTED, weight=ft.FontWeight.W_600),
                                ft.Text("Porcentaje", expand=1, size=11,
                                        color=_MUTED, weight=ft.FontWeight.W_600),
                                ft.Container(width=40),
                            ],
                            spacing=12,
                        ),
                        padding=ft.padding.symmetric(horizontal=12, vertical=8),
                        bgcolor=_CARD2,
                        border_radius=ft.border_radius.only(top_left=8, top_right=8),
                    ),
                    ben_col,
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            expand=True,
        )

    def _ben_rows(self, refresh_cb=None) -> list:
        rows = []
        for b in self._beneficiarios:
            def on_del(e, bid=b.id_beneficiario):
                BeneficiarioController.delete_beneficiario(bid)
                if refresh_cb:
                    refresh_cb()

            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(b.nombre_completo, expand=3,
                                    size=13, color=_TEXT),
                            ft.Text(b.parentesco, expand=2,
                                    size=13, color=_MUTED),
                            ft.Text(f"{b.porcentaje_participacion:.0f}%",
                                    expand=1, size=13, color=_ACCENT,
                                    weight=ft.FontWeight.W_600),
                            ft.Container(
                                content=ft.IconButton(
                                    icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    icon_color=_ERROR,
                                    icon_size=16,
                                    on_click=on_del,
                                ),
                                width=40,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.padding.symmetric(horizontal=12, vertical=10),
                    border=ft.border.only(bottom=ft.BorderSide(1, _BORDER)),
                    bgcolor=_CARD,
                )
            )
        return rows

    def _open_ben_modal(self, refresh_cb) -> None:
        nombre_f = ft.TextField(
            label="Nombre completo",
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT),
            bgcolor=_CARD,
        )
        parentesco_f = ft.TextField(
            label="Parentesco",
            hint_text="Ej. Cónyuge, Hijo",
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT),
            bgcolor=_CARD,
        )
        porcentaje_f = ft.TextField(
            label="Porcentaje (%)",
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT),
            bgcolor=_CARD,
        )
        error_t = ft.Text("", color=_ERROR, size=12)

        def guardar(e):
            total = sum(b.porcentaje_participacion for b in self._beneficiarios)
            try:
                pct = float(porcentaje_f.value or "0")
            except ValueError:
                error_t.value = "El porcentaje debe ser numérico."
                self._page.update()
                return
            if total + pct > 100:
                error_t.value = f"Suma superaría 100% (actual: {total:.0f}%)."
                self._page.update()
                return
            r = BeneficiarioController.create_beneficiario({
                "id_asegurado": self._id,
                "nombre_completo": nombre_f.value,
                "parentesco": parentesco_f.value,
                "porcentaje_participacion": pct,
            })
            if r["ok"]:
                self._page.pop_dialog()
                refresh_cb()
            else:
                error_t.value = r["error"]
                self._page.update()

        self._page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("Agregar beneficiario", color=_TEXT),
            bgcolor=_CARD,
            content=ft.Column(
                [nombre_f, parentesco_f, porcentaje_f, error_t],
                spacing=12, tight=True, width=360,
            ),
            actions=[
                ft.TextButton("Cancelar",
                              style=ft.ButtonStyle(color=_MUTED),
                              on_click=lambda e: self._page.pop_dialog()),
                ft.ElevatedButton(
                    content=ft.Text("Guardar", size=13),
                    style=ft.ButtonStyle(
                        bgcolor={ft.ControlState.DEFAULT: _ACCENT},
                        color={ft.ControlState.DEFAULT: "#000000"},
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=guardar,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        ))

    # ── Tab Seguimientos ──────────────────────────────────────────────────────
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
                        border=ft.border.all(1, _BORDER),
                    ),
                ],
                spacing=8,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            expand=True,
        )

    def _seg_items(self) -> list:
        resultado_colors = {
            "resuelto": (_ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)),
            "pendiente": (_WARN, ft.Colors.with_opacity(0.12, _WARN)),
            "sin_respuesta": (_MUTED, _CARD2),
        }
        tipo_icons = {
            "llamada": ft.Icons.PHONE_ROUNDED,
            "visita": ft.Icons.PERSON_ROUNDED,
            "mensaje": ft.Icons.MESSAGE_ROUNDED,
        }
        items = []
        segs = sorted(self._seguimientos,
                      key=lambda x: x.fecha_hora, reverse=True)
        for s in segs:
            fg, bg = resultado_colors.get(s.resultado, (_MUTED, _CARD2))
            icon = tipo_icons.get(s.tipo_contacto, ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED)
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
                                            ft.Text(
                                                str(s.fecha_hora.date()),
                                                size=11, color=_MUTED,
                                            ),
                                            _pill(s.tipo_contacto.capitalize(),
                                                  _MUTED, _CARD2),
                                            _pill(s.resultado.replace("_", " ").upper(),
                                                  fg, bg),
                                        ],
                                        spacing=8,
                                    ),
                                    ft.Text(s.observaciones, size=13, color=_TEXT),
                                ],
                                spacing=4,
                                expand=True,
                            ),
                        ],
                        spacing=12,
                        vertical_alignment=ft.CrossAxisAlignment.START,
                    ),
                    padding=ft.padding.symmetric(horizontal=16, vertical=12),
                    border=ft.border.only(bottom=ft.BorderSide(1, _BORDER)),
                )
            )
        if not items:
            items.append(
                ft.Container(
                    content=ft.Text("Sin seguimientos registrados.",
                                    color=_MUTED, size=13),
                    padding=ft.padding.symmetric(horizontal=16, vertical=16),
                )
            )
        return items

    # ── Modal nuevo seguimiento ───────────────────────────────────────────────
    def _open_seguimiento_modal(self) -> None:
        agente = obtener_agente()
        tipo_dd = ft.Dropdown(
            label="Tipo de contacto",
            options=[
                ft.dropdown.Option(key="llamada", text="Llamada"),
                ft.dropdown.Option(key="visita", text="Visita"),
                ft.dropdown.Option(key="mensaje", text="Mensaje"),
            ],
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT),
            bgcolor=_CARD,
        )
        resultado_dd = ft.Dropdown(
            label="Resultado",
            options=[
                ft.dropdown.Option(key="resuelto", text="Resuelto"),
                ft.dropdown.Option(key="pendiente", text="Pendiente"),
                ft.dropdown.Option(key="sin_respuesta", text="Sin respuesta"),
            ],
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT),
            bgcolor=_CARD,
        )
        obs_f = ft.TextField(
            label="Observaciones",
            multiline=True, min_lines=3, max_lines=5,
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT),
            bgcolor=_CARD,
        )
        fecha_f = ft.TextField(
            label="Fecha y hora (AAAA-MM-DD HH:MM)",
            hint_text="Ej. 2026-04-07 10:00",
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            hint_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT),
            bgcolor=_CARD,
        )
        error_t = ft.Text("", color=_ERROR, size=12)

        def guardar(e):
            from datetime import datetime as dt
            try:
                fecha_hora = dt.strptime(fecha_f.value.strip(), "%Y-%m-%d %H:%M")
            except (ValueError, AttributeError):
                error_t.value = "Formato de fecha inválido. Use AAAA-MM-DD HH:MM."
                self._page.update()
                return
            r = SeguimientoController.create_seguimiento({
                "id_asegurado": self._id,
                "id_agente": agente.id_agente if agente else 1,
                "tipo_contacto": tipo_dd.value,
                "resultado": resultado_dd.value,
                "observaciones": obs_f.value,
                "fecha_hora": fecha_hora,
            })
            if r["ok"]:
                self._page.pop_dialog()
                seg_res = SeguimientoController.get_seguimientos_by_asegurado(self._id)
                self._seguimientos = (seg_res.get("data", [])
                                      if seg_res["ok"] else [])
                col = self._seg_col_ref.current
                if col is not None:
                    col.controls.clear()
                    col.controls.extend(self._seg_items())
                    self._page.update()
            else:
                error_t.value = r["error"]
                self._page.update()

        self._page.show_dialog(ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo seguimiento", color=_TEXT),
            bgcolor=_CARD,
            content=ft.Column(
                [tipo_dd, resultado_dd, obs_f, fecha_f, error_t],
                spacing=12, tight=True, width=400,
            ),
            actions=[
                ft.TextButton("Cancelar",
                              style=ft.ButtonStyle(color=_MUTED),
                              on_click=lambda e: self._page.pop_dialog()),
                ft.ElevatedButton(
                    content=ft.Text("Guardar", size=13),
                    style=ft.ButtonStyle(
                        bgcolor={ft.ControlState.DEFAULT: _ACCENT},
                        color={ft.ControlState.DEFAULT: "#000000"},
                        shape=ft.RoundedRectangleBorder(radius=8),
                    ),
                    on_click=guardar,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        ))

