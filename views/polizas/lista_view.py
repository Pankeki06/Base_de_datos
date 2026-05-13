"""Vista de catálogo de pólizas — tipos de póliza y sus beneficios base."""

from __future__ import annotations

import flet as ft
from controllers.producto_poliza_controller import ProductoPolizaController
from controllers.producto_beneficio_controller import ProductoBeneficioController
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
from views.ui_controls import pill as _pill


_TIPO_ICON = {
    "Vida":                   ft.Icons.FAVORITE_ROUNDED,
    "Gastos Medicos Mayores": ft.Icons.LOCAL_HOSPITAL_ROUNDED,
    "Accidentes Personales":  ft.Icons.EMERGENCY_ROUNDED,
    "Autos":                  ft.Icons.DIRECTIONS_CAR_ROUNDED,
    "Hogar":                  ft.Icons.HOME_ROUNDED,
}


def _money(value: float | int | None) -> str:
    return f"${float(value or 0):,.2f}"


class ListaPolizasView:
    def __init__(self, page: ft.Page, navigate) -> None:
        self._page = page
        self._navigate = navigate
        self._productos: list = []
        self._beneficios_map: dict = {}
        self._catalog_col = ft.Column(spacing=16, scroll=ft.ScrollMode.AUTO, expand=True)

    # ── Ciclo de vida ──────────────────────────────────────────────────────────

    def build(self) -> ft.Control:
        self._load_data()
        from views.dashboard_view import _sidebar
        sidebar = _sidebar(self._navigate, "/polizas")
        return ft.Container(
            content=ft.Row([sidebar, self._build_main()], spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    # ── Carga de datos ─────────────────────────────────────────────────────────

    def _load_data(self) -> None:
        prod_res = ProductoPolizaController.get_all_productos()
        self._productos = prod_res.get("data", []) if prod_res["ok"] else []
        self._beneficios_map = {}
        for p in self._productos:
            b_res = ProductoBeneficioController.get_beneficios_by_producto(p.id_producto)
            self._beneficios_map[p.id_producto] = (
                b_res.get("data", []) if b_res["ok"] else []
            )

    def _refresh(self) -> None:
        self._load_data()
        self._catalog_col.controls.clear()
        self._catalog_col.controls.extend(self._build_cards())
        self._page.update()

    # ── Panel principal ────────────────────────────────────────────────────────

    def _build_main(self) -> ft.Container:
        topbar = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Catalogo de Polizas", size=18,
                            weight=ft.FontWeight.BOLD, color=_TEXT),
                    ft.Container(expand=True),
                    ft.FilledButton(
                        content=ft.Row(
                            [ft.Icon(ft.Icons.ADD_ROUNDED, size=16),
                             ft.Text("Nuevo tipo de poliza", size=13)],
                            spacing=6,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor=_ACCENT,
                            color="#000000",
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=lambda e: self._open_create_producto_modal(),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=16,
            ),
            padding=ft.Padding.symmetric(horizontal=28, vertical=16),
            border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

        self._catalog_col.controls.extend(self._build_cards())

        body = ft.Container(
            content=self._catalog_col,
            padding=ft.Padding.symmetric(horizontal=28, vertical=20),
            expand=True,
        )

        return ft.Container(
            content=ft.Column([topbar, body], spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    # ── Tarjetas de producto ───────────────────────────────────────────────────

    def _build_cards(self) -> list:
        if not self._productos:
            return [
                ft.Container(
                    content=ft.Text(
                        "No hay tipos de poliza registrados.",
                        color=_MUTED, size=14,
                    ),
                    padding=ft.Padding.all(24),
                )
            ]
        return [self._producto_card(p) for p in self._productos]

    def _producto_card(self, p) -> ft.Container:
        tipo_norm = p.tipo_seguro.replace("\u00e9", "e").replace("\u00e1", "a")
        icon = _TIPO_ICON.get(tipo_norm, ft.Icons.SHIELD_ROUNDED)
        activo_color = _ACCENT if p.activo else _MUTED
        activo_bg    = (ft.Colors.with_opacity(0.12, _ACCENT) if p.activo
                        else ft.Colors.with_opacity(0.08, _MUTED))
        beneficios   = self._beneficios_map.get(p.id_producto, [])

        ben_rows = []
        for b in beneficios:
            incluido_color = _ACCENT if b.incluido_base else _WARN
            incluido_label = "Base" if b.incluido_base else "Opcional"
            costo_extra = float(getattr(b, "costo_extra", 0) or 0)
            ben_rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                                    size=14, color=incluido_color),
                            ft.Text(b.nombre_beneficio, size=12, color=_TEXT,
                                    expand=True),
                            ft.Text(f"${b.monto_cobertura:,.0f}",
                                    size=12, color=_MUTED,
                                    weight=ft.FontWeight.W_500),
                            _pill(incluido_label, incluido_color,
                                  ft.Colors.with_opacity(0.10, incluido_color)),
                            ft.Text(
                                f"Extra {_money(costo_extra)}/mes" if not b.incluido_base else "Sin costo extra",
                                size=11,
                                color=_WARN if not b.incluido_base else _MUTED,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED,
                                icon_color=_MUTED,
                                icon_size=13,
                                tooltip="Editar beneficio",
                                on_click=lambda e, ben=b: self._open_edit_beneficio_modal(ben),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_color=_ERROR,
                                icon_size=13,
                                tooltip="Eliminar beneficio",
                                on_click=lambda e, bid=b.id_producto_beneficio: self._confirm_delete_beneficio(bid),
                            ),
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                    border_radius=6,
                    bgcolor=_CARD2,
                )
            )

        ben_section = ft.Column(
            [
                ft.Row(
                    [
                        ft.Text("Beneficios", size=11,
                                color=_MUTED, weight=ft.FontWeight.W_600),
                        ft.Container(expand=True),
                        ft.TextButton(
                            content=ft.Row(
                                [ft.Icon(ft.Icons.ADD_ROUNDED, size=13),
                                 ft.Text("Agregar", size=12)],
                                spacing=4,
                            ),
                            style=ft.ButtonStyle(color=_ACCENT),
                            on_click=lambda e, pid=p.id_producto: self._open_create_beneficio_modal(pid),
                        ),
                    ],
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                *(ben_rows if ben_rows else [
                    ft.Text("Sin beneficios definidos.", size=12, color=_MUTED)
                ]),
            ],
            spacing=6,
        )

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Container(
                                content=ft.Icon(icon, size=20, color=_ACCENT),
                                width=42, height=42, border_radius=10,
                                bgcolor=ft.Colors.with_opacity(0.12, _ACCENT),
                                alignment=ft.Alignment.CENTER,
                            ),
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Text(p.nombre, size=15,
                                                    weight=ft.FontWeight.W_600,
                                                    color=_TEXT),
                                            _pill(
                                                "Activo" if p.activo else "Inactivo",
                                                activo_color, activo_bg,
                                            ),
                                        ],
                                        spacing=8,
                                    ),
                                    ft.Row(
                                        [
                                            ft.Text(p.tipo_seguro, size=12,
                                                    color=_MUTED),
                                            ft.Text(".", size=12, color=_BORDER),
                                            ft.Text(
                                                f"Prima base: ${p.prima_base:,.0f}/mes",
                                                size=12, color=_MUTED,
                                            ),
                                        ],
                                        spacing=6,
                                    ),
                                ],
                                spacing=3, expand=True,
                            ),
                            ft.IconButton(
                                icon=ft.Icons.EDIT_OUTLINED,
                                icon_color=_MUTED,
                                icon_size=16,
                                tooltip="Editar tipo de poliza",
                                on_click=lambda e, prod=p: self._open_edit_producto_modal(prod),
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                icon_color=_ERROR,
                                icon_size=16,
                                tooltip="Eliminar tipo de poliza",
                                on_click=lambda e, pid=p.id_producto: self._confirm_delete_producto(pid),
                            ),
                        ],
                        spacing=14,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(color=_BORDER, height=1),
                    ben_section,
                ],
                spacing=12,
            ),
            padding=ft.Padding.all(20),
            bgcolor=_CARD,
            border_radius=12,
            border=ft.Border.all(1, _BORDER),
        )

    # ── Modal: crear tipo de póliza ────────────────────────────────────────────

    def _open_create_producto_modal(self) -> None:
        nombre_f = ft.TextField(
            label="Nombre del producto",
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        tipo_f = ft.TextField(
            label="Tipo de seguro",
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        prima_f = ft.TextField(
            label="Prima base mensual", keyboard_type=ft.KeyboardType.NUMBER,
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        desc_f = ft.TextField(
            label="Descripcion", multiline=True, min_lines=2,
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        err_t = ft.Text("", color=_ERROR, size=12)

        def _save(e):
            nombre = nombre_f.value.strip()
            tipo   = tipo_f.value.strip()
            prima  = prima_f.value.strip()
            if not nombre or not tipo or not prima:
                err_t.value = "Nombre, tipo y prima son obligatorios."
                self._page.update()
                return
            try:
                prima_val = float(prima)
            except ValueError:
                err_t.value = "La prima debe ser un numero."
                self._page.update()
                return
            res = ProductoPolizaController.create_producto({
                "nombre": nombre,
                "tipo_seguro": tipo,
                "prima_base": prima_val,
                "descripcion": desc_f.value.strip(),
            })
            if res["ok"]:
                self._page.pop_dialog()
                self._refresh()
            else:
                err_t.value = res.get("error", "Error al crear el producto.")
                self._page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo tipo de poliza", color=_TEXT),
            bgcolor=_CARD,
            content=ft.Column(
                [nombre_f, tipo_f, prima_f, desc_f, err_t],
                spacing=12, tight=True, width=420,
            ),
            actions=[
                ft.TextButton("Cancelar",
                              style=ft.ButtonStyle(color=_MUTED),
                              on_click=lambda e: self._page.pop_dialog()),
                ft.FilledButton("Guardar",
                                style=ft.ButtonStyle(
                                    bgcolor=_ACCENT, color="#000000"),
                                on_click=_save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._page.show_dialog(dlg)

    # ── Modal: editar tipo de póliza ───────────────────────────────────────────

    def _open_edit_producto_modal(self, producto) -> None:
        nombre_f = ft.TextField(
            label="Nombre del producto", value=producto.nombre,
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        tipo_f = ft.TextField(
            label="Tipo de seguro", value=producto.tipo_seguro,
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        prima_f = ft.TextField(
            label="Prima base mensual", value=str(producto.prima_base),
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        desc_f = ft.TextField(
            label="Descripcion", value=producto.descripcion or "",
            multiline=True, min_lines=2,
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        activo_sw = ft.Switch(label="Activo", value=producto.activo,
                              active_color=_ACCENT)
        err_t = ft.Text("", color=_ERROR, size=12)

        def _save(e):
            nombre = nombre_f.value.strip()
            tipo   = tipo_f.value.strip()
            prima  = prima_f.value.strip()
            if not nombre or not tipo or not prima:
                err_t.value = "Nombre, tipo y prima son obligatorios."
                self._page.update()
                return
            try:
                prima_val = float(prima)
            except ValueError:
                err_t.value = "La prima debe ser un numero."
                self._page.update()
                return
            res = ProductoPolizaController.update_producto(
                producto.id_producto,
                {
                    "nombre": nombre,
                    "tipo_seguro": tipo,
                    "prima_base": prima_val,
                    "descripcion": desc_f.value.strip(),
                    "activo": activo_sw.value,
                },
            )
            if res["ok"]:
                self._page.pop_dialog()
                self._refresh()
            else:
                err_t.value = res.get("error", "Error al actualizar.")
                self._page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar tipo de poliza", color=_TEXT),
            bgcolor=_CARD,
            content=ft.Column(
                [nombre_f, tipo_f, prima_f, desc_f, activo_sw, err_t],
                spacing=12, tight=True, width=420,
            ),
            actions=[
                ft.TextButton("Cancelar",
                              style=ft.ButtonStyle(color=_MUTED),
                              on_click=lambda e: self._page.pop_dialog()),
                ft.FilledButton("Guardar",
                                style=ft.ButtonStyle(
                                    bgcolor=_ACCENT, color="#000000"),
                                on_click=_save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._page.show_dialog(dlg)

    # ── Modal: confirmar eliminación de producto ───────────────────────────────

    def _confirm_delete_producto(self, id_producto: int) -> None:
        btn_del = ft.FilledButton(
            "Eliminar",
            style=ft.ButtonStyle(bgcolor=_ERROR, color="#FFFFFF"),
        )

        def _do_delete(e):
            btn_del.disabled = True
            self._page.update()
            self._page.pop_dialog()
            res = ProductoPolizaController.delete_producto(id_producto)
            if res["ok"]:
                self._refresh()

        btn_del.on_click = _do_delete
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar tipo de poliza", color=_ERROR),
            bgcolor=_CARD,
            content=ft.Text(
                "Eliminar este tipo de poliza? Se eliminaran tambien sus beneficios base.",
                color=_TEXT, size=13,
            ),
            actions=[
                ft.TextButton("Cancelar",
                              style=ft.ButtonStyle(color=_MUTED),
                              on_click=lambda e: self._page.pop_dialog()),
                btn_del,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._page.show_dialog(dlg)

    # ── Modal: agregar beneficio al producto ───────────────────────────────────

    def _open_create_beneficio_modal(self, id_producto: int) -> None:
        nombre_f = ft.TextField(
            label="Nombre del beneficio",
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        monto_f = ft.TextField(
            label="Monto de cobertura", keyboard_type=ft.KeyboardType.NUMBER,
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        desc_f = ft.TextField(
            label="Descripcion",
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        costo_extra_f = ft.TextField(
            label="Costo extra mensual",
            disabled=True,
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=_BORDER,
            focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT),
            bgcolor=_CARD,
        )
        base_sw = ft.Switch(label="Incluido en base (sin costo extra)",
                            value=True, active_color=_ACCENT)
        err_t = ft.Text("", color=_ERROR, size=12)

        def _sync_cost_field(_event=None):
            is_base = bool(base_sw.value)
            costo_extra_f.disabled = is_base
            if is_base:
                costo_extra_f.value = ""
            self._page.update()

        base_sw.on_change = _sync_cost_field

        def _save(e):
            nombre = nombre_f.value.strip()
            monto  = monto_f.value.strip()
            descripcion = desc_f.value.strip()
            if not nombre or not monto or not descripcion:
                err_t.value = "Nombre, descripcion y monto son obligatorios."
                self._page.update()
                return
            try:
                monto_val = float(monto)
                costo_extra_val = None
                if not base_sw.value:
                    raw_costo = (costo_extra_f.value or "").strip()
                    if not raw_costo:
                        err_t.value = "Captura el costo extra cuando el beneficio sea opcional."
                        self._page.update()
                        return
                    costo_extra_val = float(raw_costo)
                    if costo_extra_val <= 0:
                        raise ValueError
            except ValueError:
                err_t.value = "Monto y costo extra deben ser numeros mayores a 0."
                self._page.update()
                return
            res = ProductoBeneficioController.create_producto_beneficio({
                "id_producto":      id_producto,
                "nombre_beneficio": nombre,
                "descripcion":      descripcion,
                "monto_cobertura":  monto_val,
                "costo_extra":      costo_extra_val,
                "incluido_base":    base_sw.value,
            })
            if res["ok"]:
                self._page.pop_dialog()
                self._refresh()
            else:
                err_t.value = res.get("error", "Error al crear el beneficio.")
                self._page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Agregar beneficio", color=_TEXT),
            bgcolor=_CARD,
            content=ft.Column(
                [nombre_f, monto_f, desc_f, base_sw, costo_extra_f, err_t],
                spacing=12, tight=True, width=420,
            ),
            actions=[
                ft.TextButton("Cancelar",
                              style=ft.ButtonStyle(color=_MUTED),
                              on_click=lambda e: self._page.pop_dialog()),
                ft.FilledButton("Guardar",
                                style=ft.ButtonStyle(
                                    bgcolor=_ACCENT, color="#000000"),
                                on_click=_save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._page.show_dialog(dlg)

    # ── Modal: editar beneficio ────────────────────────────────────────────────

    def _open_edit_beneficio_modal(self, beneficio) -> None:
        nombre_f = ft.TextField(
            label="Nombre del beneficio", value=beneficio.nombre_beneficio,
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        monto_f = ft.TextField(
            label="Monto de cobertura", value=str(beneficio.monto_cobertura),
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        desc_f = ft.TextField(
            label="Descripcion", value=beneficio.descripcion or "",
            border_color=_BORDER, focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT), bgcolor=_CARD,
        )
        costo_extra_f = ft.TextField(
            label="Costo extra mensual",
            value=(str(float(getattr(beneficio, "costo_extra", 0) or 0)) if not beneficio.incluido_base and getattr(beneficio, "costo_extra", None) is not None else ""),
            disabled=bool(beneficio.incluido_base),
            keyboard_type=ft.KeyboardType.NUMBER,
            border_color=_BORDER,
            focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT),
            bgcolor=_CARD,
        )
        base_sw = ft.Switch(
            label="Incluido en base", value=beneficio.incluido_base,
            active_color=_ACCENT,
        )
        err_t = ft.Text("", color=_ERROR, size=12)

        def _sync_cost_field(_event=None):
            is_base = bool(base_sw.value)
            costo_extra_f.disabled = is_base
            if is_base:
                costo_extra_f.value = ""
            self._page.update()

        base_sw.on_change = _sync_cost_field

        def _save(e):
            nombre = nombre_f.value.strip()
            monto  = monto_f.value.strip()
            descripcion = desc_f.value.strip()
            if not nombre or not monto or not descripcion:
                err_t.value = "Nombre, descripcion y monto son obligatorios."
                self._page.update()
                return
            try:
                monto_val = float(monto)
                costo_extra_val = None
                if not base_sw.value:
                    raw_costo = (costo_extra_f.value or "").strip()
                    if not raw_costo:
                        err_t.value = "Captura el costo extra cuando el beneficio sea opcional."
                        self._page.update()
                        return
                    costo_extra_val = float(raw_costo)
                    if costo_extra_val <= 0:
                        raise ValueError
            except ValueError:
                err_t.value = "Monto y costo extra deben ser numeros mayores a 0."
                self._page.update()
                return
            res = ProductoBeneficioController.update_producto_beneficio(
                beneficio.id_producto_beneficio,
                {
                    "nombre_beneficio": nombre,
                    "monto_cobertura":  monto_val,
                    "descripcion":      descripcion,
                    "costo_extra":      costo_extra_val,
                    "incluido_base":    base_sw.value,
                },
            )
            if res["ok"]:
                self._page.pop_dialog()
                self._refresh()
            else:
                err_t.value = res.get("error", "Error al actualizar.")
                self._page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar beneficio", color=_TEXT),
            bgcolor=_CARD,
            content=ft.Column(
                [nombre_f, monto_f, desc_f, base_sw, costo_extra_f, err_t],
                spacing=12, tight=True, width=420,
            ),
            actions=[
                ft.TextButton("Cancelar",
                              style=ft.ButtonStyle(color=_MUTED),
                              on_click=lambda e: self._page.pop_dialog()),
                ft.FilledButton("Guardar",
                                style=ft.ButtonStyle(
                                    bgcolor=_ACCENT, color="#000000"),
                                on_click=_save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._page.show_dialog(dlg)

    # ── Modal: confirmar eliminación de beneficio ──────────────────────────────

    def _confirm_delete_beneficio(self, id_beneficio: int) -> None:
        btn_del = ft.FilledButton(
            "Eliminar",
            style=ft.ButtonStyle(bgcolor=_ERROR, color="#FFFFFF"),
        )

        def _do_delete(e):
            btn_del.disabled = True
            self._page.update()
            self._page.pop_dialog()
            res = ProductoBeneficioController.delete_producto_beneficio(id_beneficio)
            if res["ok"]:
                self._refresh()

        btn_del.on_click = _do_delete
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar beneficio", color=_ERROR),
            bgcolor=_CARD,
            content=ft.Text("Eliminar este beneficio del catalogo?",
                            color=_TEXT, size=13),
            actions=[
                ft.TextButton("Cancelar",
                              style=ft.ButtonStyle(color=_MUTED),
                              on_click=lambda e: self._page.pop_dialog()),
                btn_del,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._page.show_dialog(dlg)
