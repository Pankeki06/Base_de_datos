"""Vista dedicada para asignar polizas, beneficiarios y beneficios a un asegurado."""

from __future__ import annotations

from datetime import date as dt_date, datetime as dt_datetime

import flet as ft
from controllers.agente_controller import AgenteController
from controllers.asegurado_controller import AseguradoController
from controllers.beneficiario_controller import BeneficiarioController
from controllers.beneficio_controller import BeneficioController
from controllers.poliza_controller import PolizaController
from controllers.producto_beneficio_controller import ProductoBeneficioController
from controllers.producto_poliza_controller import ProductoPolizaController
from views.theme import (
    ACCENT as _ACCENT,
    BG as _BG,
    BLUE as _BLUE,
    BORDER as _BORDER,
    CARD as _CARD,
    CARD_ALT as _CARD2,
    ERROR as _ERROR,
    MUTED as _MUTED,
    TEXT as _TEXT,
    WARN as _WARN,
)
from views.asegurado.asignaciones_components import (
    assignment_dropdown as _dropdown,
    assignment_field as _field,
    panel_card as _panel,
    section_card as _section,
)
from views.ui_controls import app_sidebar, pill as _pill

_PART_LABELS = {
    "titular": "Titular",
    "conyuge": "Conyuge",
    "hijo": "Hijo",
    "dependiente": "Dependiente",
}

_PARENTESCO_OPCIONES = [
    ft.dropdown.Option(key="Esposo/a", text="Esposo/a"),
    ft.dropdown.Option(key="Hijo/a", text="Hijo/a"),
    ft.dropdown.Option(key="Padre", text="Padre"),
    ft.dropdown.Option(key="Madre", text="Madre"),
    ft.dropdown.Option(key="Hermano/a", text="Hermano/a"),
    ft.dropdown.Option(key="Abuelo/a", text="Abuelo/a"),
    ft.dropdown.Option(key="Nieto/a", text="Nieto/a"),
    ft.dropdown.Option(key="Tutor legal", text="Tutor legal"),
    ft.dropdown.Option(key="Otro", text="Otro"),
]


class AsignacionesAseguradoView:
    def __init__(
        self,
        page: ft.Page,
        navigate,
        id_asegurado: int,
        *,
        focus_poliza_id: int | None = None,
        focus_tab: str | None = None,
    ) -> None:
        self._page = page
        self._navigate = navigate
        self._id = id_asegurado
        self._focus_poliza_id = int(focus_poliza_id) if focus_poliza_id is not None else None
        self._focus_tab = focus_tab if focus_tab in {"beneficiarios", "beneficios"} else None

        self._asegurado = None
        self._agente = None
        self._polizas: list = []
        self._poliza_rol_map: dict[int, str] = {}
        self._participaciones_poliza: list[dict] = []
        self._producto_map: dict[int, object] = {}
        self._producto_beneficios_map: dict[int, list] = {}
        self._productos_activos: list = []
        self._available_polizas: list = []
        self._beneficiarios: list = []
        self._beneficios_map: dict[int, list] = {}
        self._participantes_map: dict[int, list[dict]] = {}
        self._selected_tab_index = self._resolve_initial_tab_index()

    def _show_dialog(self, dialog: ft.AlertDialog) -> None:
        self._page.show_dialog(dialog)

    def _close_dialog(self) -> None:
        self._page.pop_dialog()

    def _resolve_initial_tab_index(self) -> int:
        if self._focus_tab == "beneficiarios":
            return 1
        if self._focus_tab == "beneficios" or self._focus_poliza_id is not None:
            return 2
        return 0

    def _reload(
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

    def _build_tab_content(self, content: ft.Control) -> ft.Container:
        return ft.Container(
            content=content,
            padding=ft.Padding.only(top=4),
        )

    def _get_producto_beneficios(self, id_producto: int | None, *, only_base: bool = False) -> list:
        if not id_producto:
            return []
        beneficios = list(self._producto_beneficios_map.get(id_producto, []))
        if only_base:
            beneficios = [
                beneficio for beneficio in beneficios if getattr(beneficio, "incluido_base", False)
            ]
        return beneficios

    def _load_polizas_relacionadas(self) -> None:
        pol_res = PolizaController.get_polizas_by_asegurado(self._id)
        polizas_titular = pol_res.get("data", []) if pol_res["ok"] else []

        part_res = PolizaController.get_participaciones_by_asegurado(self._id)
        self._participaciones_poliza = part_res.get("data", []) if part_res["ok"] else []

        poliza_map: dict[int, object] = {p.id_poliza: p for p in polizas_titular}
        self._poliza_rol_map = {p.id_poliza: "titular" for p in polizas_titular}

        for part in self._participaciones_poliza:
            id_poliza = part.get("id_poliza")
            if not id_poliza:
                continue
            self._poliza_rol_map[id_poliza] = part.get("tipo_participante") or "titular"
            if id_poliza not in poliza_map:
                poliza_res = PolizaController.get_poliza_by_id(id_poliza)
                if poliza_res.get("ok") and poliza_res.get("data") is not None:
                    poliza_map[id_poliza] = poliza_res["data"]

        self._polizas = sorted(
            poliza_map.values(),
            key=lambda poliza: str(getattr(poliza, "fecha_vencimiento", "")),
            reverse=True,
        )

    def _load_data(self) -> None:
        asegurado_res = AseguradoController.get_asegurado_by_id(self._id)
        if not asegurado_res["ok"]:
            return

        self._asegurado = asegurado_res["data"]
        if self._asegurado.id_agente_responsable:
            agente_res = AgenteController.get_agente_by_id(self._asegurado.id_agente_responsable)
            self._agente = agente_res.get("data") if agente_res["ok"] else None
        else:
            self._agente = None

        self._load_polizas_relacionadas()

        productos_res = ProductoPolizaController.get_all_productos()
        self._producto_map = (
            {producto.id_producto: producto for producto in productos_res.get("data", [])}
            if productos_res["ok"]
            else {}
        )

        activos_res = ProductoPolizaController.get_productos_activos()
        self._productos_activos = list(activos_res.get("data", [])) if activos_res["ok"] else []

        self._producto_beneficios_map = {}
        for producto in self._producto_map.values():
            beneficios_catalogo_res = ProductoBeneficioController.get_beneficios_by_producto(producto.id_producto)
            self._producto_beneficios_map[producto.id_producto] = list(
                beneficios_catalogo_res.get("data", []) if beneficios_catalogo_res["ok"] else []
            )

        disponibles_res = PolizaController.get_available_polizas_for_participante(self._id)
        self._available_polizas = list(disponibles_res.get("data", [])) if disponibles_res["ok"] else []

        beneficiarios_res = BeneficiarioController.get_beneficiarios_by_asegurado(self._id)
        self._beneficiarios = list(beneficiarios_res.get("data", []) if beneficiarios_res["ok"] else [])

        self._beneficios_map = {}
        self._participantes_map = {}
        for poliza in self._polizas:
            beneficios_res = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
            self._beneficios_map[poliza.id_poliza] = list(
                beneficios_res.get("data", []) if beneficios_res["ok"] else []
            )

            participantes_res = PolizaController.get_participantes_by_poliza(poliza.id_poliza)
            self._participantes_map[poliza.id_poliza] = list(
                participantes_res.get("data", []) if participantes_res["ok"] else []
            )

    def build(self) -> ft.Control:
        self._load_data()
        if self._asegurado is None:
            return ft.Container(
                content=ft.Text("Asegurado no encontrado.", color=_ERROR, size=14),
                expand=True,
                bgcolor=_BG,
                alignment=ft.Alignment.CENTER,
            )

        sidebar = app_sidebar(self._navigate, "/clientes")
        return ft.Container(
            content=ft.Row([sidebar, self._build_main()], spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    def _build_main(self) -> ft.Container:
        asegurado = self._asegurado
        nombre = f"{asegurado.nombre} {asegurado.apellido_paterno} {asegurado.apellido_materno}".strip()

        topbar = ft.Container(
            content=ft.Row(
                [
                    ft.TextButton(
                        content=ft.Row(
                            [
                                ft.Icon(ft.Icons.ARROW_BACK_ROUNDED, size=20, color=_MUTED),
                                ft.Text("Clientes", size=15, color=_MUTED),
                            ],
                            spacing=6,
                            tight=True,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        style=ft.ButtonStyle(color=_MUTED),
                        on_click=lambda e: self._navigate("/clientes"),
                    ),
                    ft.Text(
                        f"Asignaciones de {nombre}",
                        size=20,
                        weight=ft.FontWeight.BOLD,
                        color=_TEXT,
                    ),
                    ft.Container(expand=True),
                    ft.OutlinedButton(
                        content=ft.Text("Ver detalle", size=13, color=_TEXT),
                        style=ft.ButtonStyle(
                            color=_TEXT,
                            side={ft.ControlState.DEFAULT: ft.BorderSide(1, _BORDER)},
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        on_click=lambda e: self._navigate("/asegurado/detalle", id_asegurado=self._id),
                    ),
                ],
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=28, vertical=20),
            border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

        tab_views = [
            self._build_tab_content(self._build_polizas_section()),
            self._build_tab_content(self._build_beneficiarios_section()),
            self._build_tab_content(self._build_beneficios_section()),
        ]
        active_tab_content = ft.Container(content=tab_views[self._selected_tab_index])

        def _handle_tab_change(event) -> None:
            self._selected_tab_index = event.control.selected_index
            active_tab_content.content = tab_views[self._selected_tab_index]
            self._page.update()

        tabs = ft.Tabs(
            selected_index=self._selected_tab_index,
            animation_duration=150,
            length=len(tab_views),
            on_change=_handle_tab_change,
            content=ft.Column(
                [
                    ft.TabBar(
                        tabs=[
                            ft.Tab(label="Polizas"),
                            ft.Tab(label="Beneficiarios"),
                            ft.Tab(label="Beneficios"),
                        ],
                        tab_alignment=ft.TabAlignment.START,
                        indicator_color=_ACCENT,
                        label_color=_TEXT,
                        unselected_label_color=_MUTED,
                    ),
                    active_tab_content,
                ],
                spacing=0,
            ),
        )

        body = ft.Container(
            content=ft.Column(
                [
                    self._build_summary_card(),
                    tabs,
                ],
                spacing=16,
                scroll=ft.ScrollMode.AUTO,
            ),
            padding=ft.Padding.symmetric(horizontal=28, vertical=20),
            expand=True,
        )

        return ft.Container(
            content=ft.Column([topbar, body], spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    def _build_summary_card(self) -> ft.Container:
        asegurado = self._asegurado
        agente_label = (
            f"{self._agente.nombre} {self._agente.apellido_paterno}"
            if self._agente
            else "Sin agente asignado"
        )
        return _section(
            "Resumen del asegurado",
            [
                ft.Text(f"RFC: {asegurado.rfc}", size=13, color=_TEXT),
                ft.Text(f"Correo: {asegurado.correo or 'Sin correo'}", size=13, color=_MUTED),
                ft.Text(f"Celular: {asegurado.celular or 'Sin celular'}", size=13, color=_MUTED),
                ft.Text(f"Agente responsable: {agente_label}", size=13, color=_MUTED),
                ft.Row(
                    [
                        _pill(f"Polizas vinculadas: {len(self._polizas)}", _ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)),
                        _pill(f"Beneficiarios: {len(self._beneficiarios)}", _BLUE, ft.Colors.with_opacity(0.12, _BLUE)),
                    ],
                    spacing=8,
                    wrap=True,
                ),
            ],
        )

    def _build_polizas_section(self) -> ft.Container:
        default_producto_value = (
            str(self._productos_activos[0].id_producto)
            if self._productos_activos
            else None
        )
        default_operacion_value = "crear" if self._productos_activos else "vincular"
        default_poliza_vinculo_value = (
            str(self._available_polizas[0].id_poliza)
            if self._available_polizas
            else None
        )
        producto_dd = _dropdown(
            "Producto activo",
            [
                ft.dropdown.Option(key=str(producto.id_producto), text=producto.nombre)
                for producto in self._productos_activos
            ],
            value=default_producto_value,
        )
        numero_f = _field("Numero de poliza", hint="Ej. PZ-2026-001")
        inicio_f = _field("Fecha inicio (AAAA-MM-DD)", expand=1)
        vencimiento_f = _field("Fecha vencimiento (AAAA-MM-DD)", expand=1)
        prima_f = _field(
            "Prima mensual",
            hint="Se llenara con la prima base del producto",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        estatus_dd = _dropdown(
            "Estatus",
            [
                ft.dropdown.Option(key="activa", text="Activa"),
                ft.dropdown.Option(key="vencida", text="Vencida"),
                ft.dropdown.Option(key="cancelada", text="Cancelada"),
            ],
            value="activa",
        )
        create_err = ft.Text("", color=_ERROR, size=12)
        producto_tipo_t = ft.Text(
            "Selecciona un producto para tomar defaults del catalogo.",
            size=12,
            color=_MUTED,
        )
        producto_prima_t = ft.Text(
            "La prima mensual se puede ajustar antes de guardar la poliza.",
            size=12,
            color=_MUTED,
        )
        producto_beneficios_t = ft.Text(
            "Los beneficios base se marcan automáticamente; puedes activar o desactivar cualquiera antes de emitir la póliza.",
            size=12,
            color=_MUTED,
        )
        beneficios_resumen_t = ft.Text(
            "Selecciona un producto para definir qué beneficios se emitirán con la póliza.",
            size=12,
            color=_MUTED,
        )
        producto_beneficios_col = ft.Column(
            [
                ft.Text(
                    "Los beneficios del producto apareceran aqui.",
                    size=12,
                    color=_MUTED,
                )
            ],
            spacing=8,
        )
        beneficios_seleccionables: list[tuple[object, ft.Checkbox]] = []
        current_operacion = {"value": default_operacion_value}

        def _replace_column_controls(column: ft.Column, controls: list[ft.Control]) -> None:
            column.controls.clear()
            column.controls.extend(controls)

        def _operation_button_style(*, active: bool) -> ft.ButtonStyle:
            return ft.ButtonStyle(
                bgcolor=_ACCENT if active else _CARD2,
                color="#000000" if active else _TEXT,
                side={
                    ft.ControlState.DEFAULT: ft.BorderSide(1, _ACCENT if active else _BORDER)
                },
                shape=ft.RoundedRectangleBorder(radius=10),
            )

        operation_help_t = ft.Text(
            "Elige el flujo a trabajar. Al crear una poliza te enviaremos directo a la pestaña Beneficios para ajustarlos despues.",
            size=12,
            color=_MUTED,
        )
        crear_mode_btn = ft.FilledButton(
            "Crear nueva poliza",
            style=_operation_button_style(active=default_operacion_value == "crear"),
        )
        vincular_mode_btn = ft.FilledButton(
            "Vincular poliza existente",
            style=_operation_button_style(active=default_operacion_value == "vincular"),
        )

        def _sync_beneficios_resumen(*, update_page: bool = True) -> None:
            if not beneficios_seleccionables:
                beneficios_resumen_t.value = "Este producto no tiene beneficios activos para seleccionar."
            else:
                total = len(beneficios_seleccionables)
                seleccionados = sum(
                    1
                    for _, checkbox in beneficios_seleccionables
                    if checkbox.value
                )
                costo_total = sum(
                    float(getattr(beneficio, "costo_extra", 0) or 0)
                    for beneficio, checkbox in beneficios_seleccionables
                    if checkbox.value
                )
                producto = self._producto_map.get(int(producto_dd.value)) if producto_dd.value else None
                prima_base = float(getattr(producto, "prima_base", 0) or 0)
                prima_sugerida = prima_base + costo_total
                prima_f.value = f"{prima_sugerida:.2f}"
                beneficios_resumen_t.value = (
                    f"Se emitirán {seleccionados} de {total} beneficio(s) al crear la póliza. "
                    f"Costo adicional seleccionado: ${costo_total:,.2f}. Prima sugerida: ${prima_sugerida:,.2f}."
                )
            if update_page:
                self._page.update()

        def _catalog_beneficio_rows(beneficios: list) -> list[ft.Control]:
            nonlocal beneficios_seleccionables
            beneficios_seleccionables = []
            if not beneficios:
                return [
                    ft.Text(
                        "Este producto no tiene beneficios activos en el catalogo.",
                        size=12,
                        color=_MUTED,
                    )
                ]

            rows: list[ft.Control] = []
            for beneficio in beneficios:
                is_base = getattr(beneficio, "incluido_base", False)
                badge_color = _ACCENT if is_base else _BLUE
                checkbox = ft.Checkbox(
                    label=beneficio.nombre_beneficio,
                    value=is_base,
                    active_color=badge_color,
                    check_color="#000000",
                    label_style=ft.TextStyle(color=_TEXT, weight=ft.FontWeight.W_600),
                    on_change=lambda e: _sync_beneficios_resumen(),
                )
                beneficios_seleccionables.append((beneficio, checkbox))
                rows.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Container(content=checkbox, expand=True),
                                        _pill(
                                            "Base" if is_base else "Opcional",
                                            badge_color,
                                            ft.Colors.with_opacity(0.12, badge_color),
                                        ),
                                        ft.Text(
                                            f"${beneficio.monto_cobertura:,.0f}",
                                            size=12,
                                            color=_MUTED,
                                        ),
                                        ft.Text(
                                            (
                                                f"Extra ${float(getattr(beneficio, 'costo_extra', 0) or 0):,.2f}/mes"
                                                if not is_base
                                                else "Sin costo extra"
                                            ),
                                            size=11,
                                            color=_BLUE if not is_base else _MUTED,
                                        ),
                                    ],
                                    spacing=8,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Text(
                                    beneficio.descripcion,
                                    size=11,
                                    color=_MUTED,
                                ),
                            ],
                            spacing=4,
                        ),
                        padding=ft.Padding.all(12),
                        bgcolor=_CARD,
                        border_radius=10,
                        border=ft.Border.all(1, _BORDER),
                    )
                )
            return rows

        def _sync_producto_defaults(_event=None, *, update_page: bool = True) -> None:
            selected_value = getattr(getattr(_event, "control", None), "value", None)
            if selected_value is None:
                selected_value = producto_dd.value
            if selected_value in (None, ""):
                producto_tipo_t.value = "Selecciona un producto para tomar defaults del catalogo."
                producto_prima_t.value = "La prima mensual se puede ajustar antes de guardar la poliza."
                _replace_column_controls(producto_beneficios_col, _catalog_beneficio_rows([]))
                _sync_beneficios_resumen(update_page=False)
                if update_page:
                    self._page.update()
                return

            producto_dd.value = str(selected_value)

            producto = self._producto_map.get(int(producto_dd.value))
            if producto is None:
                producto_tipo_t.value = "Producto no disponible."
                producto_prima_t.value = ""
                _replace_column_controls(producto_beneficios_col, _catalog_beneficio_rows([]))
                _sync_beneficios_resumen(update_page=False)
                if update_page:
                    self._page.update()
                return

            prima_f.value = f"{float(getattr(producto, 'prima_base', 0) or 0):.2f}"
            producto_tipo_t.value = f"{producto.nombre} · {getattr(producto, 'tipo_seguro', 'Sin tipo')}"
            producto_prima_t.value = (
                f"Prima base del catalogo: ${float(getattr(producto, 'prima_base', 0) or 0):,.2f} al mes."
            )
            _replace_column_controls(
                producto_beneficios_col,
                _catalog_beneficio_rows(self._get_producto_beneficios(producto.id_producto)),
            )
            _sync_beneficios_resumen(update_page=False)
            if update_page:
                self._page.update()

        producto_dd.on_select = _sync_producto_defaults
        producto_dd.on_change = _sync_producto_defaults

        def _parse_date_value(raw_value: str) -> dt_date:
            raw_value = (raw_value or "").strip()
            if not raw_value:
                raise ValueError

            normalized = raw_value.split("T", 1)[0].split(" ", 1)[0]
            return dt_date.fromisoformat(normalized)

        def _open_date_picker(target: ft.TextField, label: str) -> None:
            initial_value = dt_date.today()
            raw_value = (target.value or "").strip()
            if raw_value:
                try:
                    initial_value = _parse_date_value(raw_value)
                except ValueError:
                    initial_value = dt_date.today()

            def _apply_date(event) -> None:
                selected = event.control.value
                if selected is None:
                    return
                if isinstance(selected, dt_datetime):
                    selected = selected.date()
                elif not isinstance(selected, dt_date):
                    try:
                        selected = _parse_date_value(str(selected))
                    except ValueError:
                        return
                target.value = selected.strftime("%Y-%m-%d")
                self._page.update()

            self._show_dialog(
                ft.DatePicker(
                    open=True,
                    modal=True,
                    value=initial_value,
                    first_date=dt_date(2000, 1, 1),
                    last_date=dt_date(2100, 12, 31),
                    help_text=label,
                    field_label_text=label,
                    cancel_text="Cancelar",
                    confirm_text="Seleccionar",
                    on_change=_apply_date,
                )
            )

        def _crear_poliza(e):
            if not producto_dd.value:
                create_err.value = "Selecciona un producto activo."
                self._page.update()
                return

            if not (prima_f.value or "").strip() and producto_dd.value:
                producto = self._producto_map.get(int(producto_dd.value))
                if producto is not None:
                    prima_f.value = f"{float(getattr(producto, 'prima_base', 0) or 0):.2f}"

            try:
                fecha_inicio = _parse_date_value(inicio_f.value)
                fecha_vencimiento = _parse_date_value(vencimiento_f.value)
                prima = float(prima_f.value or "0")
                if prima <= 0:
                    raise ValueError
            except ValueError:
                create_err.value = "Revisa fechas y prima; deben tener formato valido y monto positivo."
                self._page.update()
                return

            response = PolizaController.create_poliza(
                {
                    "id_asegurado": self._id,
                    "id_producto": int(producto_dd.value),
                    "numero_poliza": numero_f.value.strip(),
                    "fecha_inicio": fecha_inicio,
                    "fecha_vencimiento": fecha_vencimiento,
                    "estatus": estatus_dd.value or "activa",
                    "prima_mensual": prima,
                }
            )
            if response["ok"]:
                poliza_creada = response.get("data")
                id_poliza = getattr(poliza_creada, "id_poliza", None)
                if id_poliza is not None:
                    self._navigate(
                        "/asegurado/asignaciones",
                        id_asegurado=self._id,
                        focus_poliza_id=int(id_poliza),
                    )
                else:
                    self._reload()
            else:
                create_err.value = response.get("error", "No fue posible crear la poliza.")
                self._page.update()

        link_err = ft.Text("", color=_ERROR, size=12)
        poliza_vinculo_dd = _dropdown(
            "Poliza activa existente",
            [
                ft.dropdown.Option(key=str(poliza.id_poliza), text=poliza.numero_poliza)
                for poliza in self._available_polizas
            ],
            value=default_poliza_vinculo_value,
        )
        tipo_vinculo_dd = _dropdown(
            "Tipo de participante",
            [
                ft.dropdown.Option(key="conyuge", text="Conyuge"),
                ft.dropdown.Option(key="hijo", text="Hijo"),
                ft.dropdown.Option(key="dependiente", text="Dependiente"),
            ],
            value="dependiente",
        )
        vinculo_poliza_t = ft.Text(
            "Selecciona una poliza activa para revisar sus beneficios vigentes.",
            size=12,
            color=_MUTED,
        )
        vinculo_resumen_t = ft.Text(
            "Al elegir una poliza veras los beneficios que ya estan emitidos para esa cobertura.",
            size=12,
            color=_MUTED,
        )
        vinculo_beneficios_col = ft.Column(
            [
                ft.Text(
                    "Los beneficios de la poliza seleccionada apareceran aqui.",
                    size=12,
                    color=_MUTED,
                )
            ],
            spacing=8,
        )

        def _get_beneficios_vinculo(id_poliza: int | None) -> list:
            if not id_poliza:
                return []

            if id_poliza not in self._beneficios_map:
                beneficios_res = BeneficioController.get_beneficios_by_poliza(id_poliza)
                self._beneficios_map[id_poliza] = list(
                    beneficios_res.get("data", []) if beneficios_res["ok"] else []
                )

            return list(self._beneficios_map.get(id_poliza, []))

        def _vinculo_beneficio_rows(beneficios: list) -> list[ft.Control]:
            if not beneficios:
                return [
                    ft.Text(
                        "La poliza seleccionada no tiene beneficios emitidos aun.",
                        size=12,
                        color=_MUTED,
                    )
                ]

            rows: list[ft.Control] = []
            for beneficio in beneficios:
                vigente = getattr(beneficio, "vigente", True)
                badge_color = _ACCENT if vigente else _WARN
                rows.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Text(
                                            beneficio.nombre_beneficio,
                                            size=13,
                                            color=_TEXT,
                                            weight=ft.FontWeight.W_600,
                                        ),
                                        _pill(
                                            "Vigente" if vigente else "Inactivo",
                                            badge_color,
                                            ft.Colors.with_opacity(0.12, badge_color),
                                        ),
                                        ft.Text(
                                            f"${beneficio.monto_cobertura:,.0f}",
                                            size=12,
                                            color=_MUTED,
                                        ),
                                    ],
                                    spacing=8,
                                    wrap=True,
                                ),
                                ft.Text(
                                    beneficio.descripcion,
                                    size=11,
                                    color=_MUTED,
                                ),
                            ],
                            spacing=4,
                        ),
                        padding=ft.Padding.all(12),
                        bgcolor=_CARD,
                        border_radius=10,
                        border=ft.Border.all(1, _BORDER),
                    )
                )
            return rows

        def _sync_vinculo_defaults(_event=None, *, update_page: bool = True) -> None:
            selected_value = getattr(getattr(_event, "control", None), "value", None)
            if selected_value is None:
                selected_value = poliza_vinculo_dd.value

            if selected_value in (None, ""):
                vinculo_poliza_t.value = "Selecciona una poliza activa para revisar sus beneficios vigentes."
                vinculo_resumen_t.value = "Al elegir una poliza veras los beneficios que ya estan emitidos para esa cobertura."
                _replace_column_controls(vinculo_beneficios_col, _vinculo_beneficio_rows([]))
                if update_page:
                    self._page.update()
                return

            poliza_vinculo_dd.value = str(selected_value)
            poliza = next(
                (
                    item
                    for item in self._available_polizas
                    if str(getattr(item, "id_poliza", "")) == poliza_vinculo_dd.value
                ),
                None,
            )
            producto = self._producto_map.get(getattr(poliza, "id_producto", None)) if poliza else None
            beneficios = _get_beneficios_vinculo(int(poliza_vinculo_dd.value))

            vinculo_poliza_t.value = (
                f"{getattr(poliza, 'numero_poliza', 'Poliza activa')}"
                + (f" · {producto.nombre}" if producto else "")
            )
            if beneficios:
                vinculo_resumen_t.value = (
                    f"La poliza seleccionada tiene {len(beneficios)} beneficio(s) emitidos actualmente."
                )
            else:
                vinculo_resumen_t.value = "La poliza seleccionada no tiene beneficios emitidos aun."
            _replace_column_controls(vinculo_beneficios_col, _vinculo_beneficio_rows(beneficios))
            if update_page:
                self._page.update()

        poliza_vinculo_dd.on_select = _sync_vinculo_defaults
        poliza_vinculo_dd.on_change = _sync_vinculo_defaults

        def _vincular_poliza(e):
            if not poliza_vinculo_dd.value:
                link_err.value = "Selecciona una poliza disponible."
                self._page.update()
                return

            response = PolizaController.add_participante_to_poliza(
                {
                    "id_poliza": int(poliza_vinculo_dd.value),
                    "id_asegurado": self._id,
                    "tipo_participante": tipo_vinculo_dd.value or "dependiente",
                }
            )
            if response["ok"]:
                self._navigate(
                    "/asegurado/asignaciones",
                    id_asegurado=self._id,
                    focus_poliza_id=int(poliza_vinculo_dd.value),
                )
            else:
                link_err.value = response.get("error", "No fue posible vincular la poliza.")
                self._page.update()

        poliza_rows = []
        for poliza in self._polizas:
            producto = self._producto_map.get(poliza.id_producto)
            role = self._poliza_rol_map.get(poliza.id_poliza, "titular")
            role_label = _PART_LABELS.get(role, role.capitalize())
            poliza_rows.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Text(
                                        f"Poliza {poliza.numero_poliza}",
                                        size=14,
                                        weight=ft.FontWeight.W_600,
                                        color=_TEXT,
                                    ),
                                    _pill(poliza.estatus.upper(), _ACCENT if poliza.estatus == "activa" else _WARN, _CARD2),
                                    _pill(f"Rol: {role_label}", _BLUE, ft.Colors.with_opacity(0.12, _BLUE)),
                                ],
                                spacing=8,
                                wrap=True,
                            ),
                            ft.Text(
                                f"Producto: {producto.nombre if producto else poliza.numero_poliza}",
                                size=12,
                                color=_MUTED,
                            ),
                            ft.Text(
                                f"Vigencia: {poliza.fecha_inicio} -> {poliza.fecha_vencimiento} | Prima: ${poliza.prima_mensual:,.2f}",
                                size=12,
                                color=_MUTED,
                            ),
                        ],
                        spacing=4,
                    ),
                    padding=ft.Padding.all(14),
                    bgcolor=_CARD2,
                    border_radius=10,
                    border=ft.Border.all(1, _BORDER),
                )
            )
        if not poliza_rows:
            poliza_rows.append(ft.Text("Sin polizas vinculadas aun.", size=13, color=_MUTED))

        new_poliza_panel = _panel(
            "Nueva poliza",
            [
                ft.Text(
                    "Selecciona el producto y completa la poliza. Despues de crearla podras ajustar sus beneficios en la pestaña Beneficios.",
                    size=12,
                    color=_MUTED,
                ),
                producto_dd,
                numero_f,
                ft.ResponsiveRow(
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    inicio_f,
                                    ft.IconButton(
                                        icon=ft.Icons.CALENDAR_MONTH_ROUNDED,
                                        icon_color=_ACCENT,
                                        tooltip="Abrir calendario de inicio",
                                        on_click=lambda e: _open_date_picker(inicio_f, "Fecha inicio"),
                                    ),
                                ],
                                spacing=8,
                                vertical_alignment=ft.CrossAxisAlignment.END,
                            ),
                            col={"xs": 12, "md": 6},
                        ),
                        ft.Container(
                            content=ft.Row(
                                [
                                    vencimiento_f,
                                    ft.IconButton(
                                        icon=ft.Icons.CALENDAR_MONTH_ROUNDED,
                                        icon_color=_ACCENT,
                                        tooltip="Abrir calendario de vencimiento",
                                        on_click=lambda e: _open_date_picker(vencimiento_f, "Fecha vencimiento"),
                                    ),
                                ],
                                spacing=8,
                                vertical_alignment=ft.CrossAxisAlignment.END,
                            ),
                            col={"xs": 12, "md": 6},
                        ),
                    ],
                    spacing=12,
                    run_spacing=12,
                ),
                ft.ResponsiveRow(
                    [
                        ft.Container(content=estatus_dd, col={"xs": 12, "md": 6}),
                        ft.Container(content=prima_f, col={"xs": 12, "md": 6}),
                    ],
                    spacing=12,
                    run_spacing=12,
                ),
                create_err,
                ft.FilledButton(
                    "Crear poliza",
                    style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"),
                    on_click=_crear_poliza,
                ),
            ],
        )

        vinculo_panel = _panel(
            "Vincular a poliza existente",
            [
                ft.Text(
                    "Utiliza este bloque cuando el asegurado deba entrar como conyuge, hijo o dependiente en una poliza ya activa.",
                    size=12,
                    color=_MUTED,
                ),
                (
                    ft.Column(
                        [
                            poliza_vinculo_dd,
                            tipo_vinculo_dd,
                            link_err,
                            ft.FilledButton(
                                "Vincular poliza",
                                style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"),
                                on_click=_vincular_poliza,
                            ),
                        ],
                        spacing=12,
                    )
                    if self._available_polizas
                    else ft.Text(
                        "No hay polizas activas disponibles para vincular a este asegurado.",
                        size=13,
                        color=_MUTED,
                    )
                ),
            ],
        )

        create_mode_content = ft.Column([new_poliza_panel], spacing=16)
        link_mode_content = ft.Column(
            [vinculo_panel],
            spacing=16,
        )
        create_mode_container = ft.Container(content=create_mode_content, visible=False)
        link_mode_container = ft.Container(content=link_mode_content, visible=False)
        operacion_content = ft.Column(
            [create_mode_container, link_mode_container],
            spacing=16,
        )

        def _sync_operacion_panel(selected_value: str | None = None, *, update_page: bool = True) -> None:
            if selected_value is None:
                selected_value = current_operacion["value"] or default_operacion_value
            current_operacion["value"] = "vincular" if selected_value == "vincular" else "crear"

            is_vincular = current_operacion["value"] == "vincular"
            create_mode_container.visible = not is_vincular
            link_mode_container.visible = is_vincular
            crear_mode_btn.style = _operation_button_style(active=not is_vincular)
            vincular_mode_btn.style = _operation_button_style(active=is_vincular)

            if is_vincular:
                _sync_vinculo_defaults(update_page=False)
            else:
                if producto_dd.value:
                    _sync_producto_defaults(update_page=False)

            if update_page:
                self._page.update()

        crear_mode_btn.on_click = lambda e: _sync_operacion_panel("crear")
        vincular_mode_btn.on_click = lambda e: _sync_operacion_panel("vincular")

        _sync_operacion_panel(update_page=False)

        return _section(
            "Polizas",
            [
                ft.Text(
                    "Elige si vas a crear una nueva poliza o vincular una existente; el formulario se separa segun la operacion.",
                    size=13,
                    color=_MUTED,
                ),
                operation_help_t,
                ft.Row(
                    [crear_mode_btn, vincular_mode_btn],
                    spacing=12,
                    wrap=True,
                ),
                operacion_content,
                ft.Divider(color=_BORDER, height=16),
                ft.Text("Polizas vinculadas", size=14, weight=ft.FontWeight.W_600, color=_TEXT),
                *poliza_rows,
            ],
        )

    def _build_beneficiarios_section(self) -> ft.Container:
        legacy_beneficiarios = self._beneficiarios_for_poliza(None)
        if not self._polizas:
            controls: list[ft.Control] = [
                ft.Text(
                    "Primero crea o vincula una poliza para poder asignar beneficiarios por poliza.",
                    size=13,
                    color=_MUTED,
                )
            ]
            if legacy_beneficiarios:
                controls.extend(
                    [
                        ft.Divider(color=_BORDER, height=16),
                        ft.Text("Beneficiarios sin poliza asignada", size=13, weight=ft.FontWeight.W_600, color=_WARN),
                        *self._beneficiario_rows(
                            legacy_beneficiarios,
                            focus_poliza_id=None,
                            show_poliza=True,
                        ),
                    ]
                )
            return _section("Beneficiarios", controls)

        controls: list[ft.Control] = []
        poliza_destacada = next(
            (poliza for poliza in self._polizas if poliza.id_poliza == self._focus_poliza_id),
            None,
        )
        if self._focus_tab == "beneficiarios" and poliza_destacada is not None:
            controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=_ACCENT, size=18),
                            ft.Text(
                                f"Continua con los beneficiarios de la poliza {poliza_destacada.numero_poliza}.",
                                size=13,
                                color=_TEXT,
                                weight=ft.FontWeight.W_600,
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=12,
                    bgcolor=ft.Colors.with_opacity(0.12, _ACCENT),
                    border_radius=10,
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.2, _ACCENT)),
                )
            )

        controls.append(
            ft.Text(
                "Selecciona la poliza en la que estas trabajando. Cada poliza administra sus propios beneficiarios y su propio porcentaje total.",
                size=13,
                color=_MUTED,
            )
        )

        selected_poliza_id = next(
            (
                poliza.id_poliza
                for poliza in self._polizas
                if poliza.id_poliza == self._focus_poliza_id
            ),
            self._polizas[0].id_poliza,
        )
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
                self._build_beneficiario_poliza_card(poliza) if poliza is not None else None
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

        controls.extend(
            [
                ft.Text("Poliza en trabajo", size=12, color=_MUTED),
                selector_row,
                active_poliza_content,
            ]
        )

        if legacy_beneficiarios:
            controls.extend(
                [
                    ft.Divider(color=_BORDER, height=18),
                    ft.Text("Beneficiarios heredados sin poliza asignada", size=13, weight=ft.FontWeight.W_600, color=_WARN),
                    ft.Text(
                        "Estos registros siguen visibles para que puedas reasignarlos manualmente a una poliza desde editar.",
                        size=12,
                        color=_MUTED,
                    ),
                    *self._beneficiario_rows(
                        legacy_beneficiarios,
                        focus_poliza_id=None,
                        show_poliza=True,
                    ),
                ]
            )

        _sync_selected_poliza(update_page=False)

        return _section("Beneficiarios", controls)

    def _beneficiarios_for_poliza(self, id_poliza: int | None) -> list:
        return [
            beneficiario
            for beneficiario in self._beneficiarios
            if getattr(beneficiario, "id_poliza", None) == id_poliza
        ]

    def _build_beneficiario_poliza_card(self, poliza) -> ft.Container:
        nombre_f = _field("Nombre completo")
        parentesco_f = _dropdown("Parentesco", _PARENTESCO_OPCIONES)
        porcentaje_f = _field("Porcentaje (%)", keyboard_type=ft.KeyboardType.NUMBER)
        telefono_f = _field("Telefono (opcional)", keyboard_type=ft.KeyboardType.PHONE)
        err_t = ft.Text("", color=_ERROR, size=12)

        def _guardar_beneficiario(e):
            try:
                porcentaje = float(porcentaje_f.value or "0")
                if porcentaje <= 0:
                    raise ValueError
            except ValueError:
                err_t.value = "El porcentaje debe ser un numero positivo."
                self._page.update()
                return

            response = BeneficiarioController.create_beneficiario(
                {
                    "id_asegurado": self._id,
                    "id_poliza": poliza.id_poliza,
                    "nombre_completo": nombre_f.value.strip(),
                    "parentesco": parentesco_f.value.strip(),
                    "porcentaje_participacion": porcentaje,
                    "telefono": telefono_f.value.strip() or None,
                }
            )
            if response["ok"]:
                self._reload(focus_poliza_id=poliza.id_poliza, focus_tab="beneficiarios")
            else:
                err_t.value = response.get("error", "No fue posible guardar el beneficiario.")
                self._page.update()

        beneficiarios_poliza = self._beneficiarios_for_poliza(poliza.id_poliza)
        beneficiario_rows = self._beneficiario_rows(
            beneficiarios_poliza,
            focus_poliza_id=poliza.id_poliza,
        )
        if not beneficiario_rows:
            beneficiario_rows = [ft.Text("Sin beneficiarios registrados para esta poliza.", size=13, color=_MUTED)]

        total_pct = sum(item.porcentaje_participacion for item in beneficiarios_poliza)
        producto = self._producto_map.get(poliza.id_producto)
        role = self._poliza_rol_map.get(poliza.id_poliza, "titular")
        role_label = _PART_LABELS.get(role, role.capitalize())

        return ft.Container(
            content=ft.Column(
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
                                f"Producto: {producto.nombre if producto else poliza.numero_poliza}",
                                _ACCENT,
                                ft.Colors.with_opacity(0.12, _ACCENT),
                            ),
                            _pill(
                                f"Rol actual: {role_label}",
                                _BLUE,
                                ft.Colors.with_opacity(0.12, _BLUE),
                            ),
                        ],
                        spacing=8,
                        wrap=True,
                    ),
                    ft.Text(
                        f"Total asignado en esta poliza: {total_pct:.0f}%",
                        size=12,
                        color=_ERROR if total_pct > 100 else _ACCENT,
                    ),
                    ft.ResponsiveRow(
                        [
                            ft.Container(content=nombre_f, col={"xs": 12, "md": 7}),
                            ft.Container(content=telefono_f, col={"xs": 12, "md": 5}),
                            ft.Container(content=parentesco_f, col={"xs": 12, "md": 7}),
                            ft.Container(content=porcentaje_f, col={"xs": 12, "md": 5}),
                        ],
                        spacing=12,
                        run_spacing=12,
                    ),
                    ft.Row(
                        [
                            err_t,
                            ft.Container(expand=True),
                            ft.FilledButton(
                                "Agregar beneficiario",
                                style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"),
                                on_click=_guardar_beneficiario,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.END,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(color=_BORDER, height=16),
                    *beneficiario_rows,
                ],
                spacing=12,
            ),
            padding=16,
            bgcolor=_CARD2,
            border_radius=12,
            border=ft.Border.all(1, _BORDER),
        )

    def _beneficiario_rows(
        self,
        beneficiarios: list,
        *,
        focus_poliza_id: int | None,
        show_poliza: bool = False,
    ) -> list[ft.Control]:
        rows = []
        for beneficiario in beneficiarios:
            policy_row: list[ft.Control] = []
            if show_poliza:
                id_poliza = getattr(beneficiario, "id_poliza", None)
                poliza = next((item for item in self._polizas if item.id_poliza == id_poliza), None)
                if poliza is None:
                    policy_row = [_pill("Sin poliza asignada", _WARN, ft.Colors.with_opacity(0.12, _WARN))]
                else:
                    producto = self._producto_map.get(poliza.id_producto)
                    role = self._poliza_rol_map.get(poliza.id_poliza, "titular")
                    policy_row = [
                        _pill(
                            f"Poliza {poliza.numero_poliza}",
                            _ACCENT,
                            ft.Colors.with_opacity(0.12, _ACCENT),
                        ),
                        _pill(
                            _PART_LABELS.get(role, role.capitalize()),
                            _BLUE,
                            ft.Colors.with_opacity(0.12, _BLUE),
                        ),
                    ]
                    if producto is not None:
                        policy_row.append(
                            _pill(
                                producto.nombre,
                                _TEXT,
                                ft.Colors.with_opacity(0.08, _TEXT),
                            )
                        )

            rows.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Text(beneficiario.nombre_completo, size=13, color=_TEXT, weight=ft.FontWeight.W_600),
                                            ft.Text(
                                                f"{beneficiario.parentesco} | {beneficiario.porcentaje_participacion:.0f}% | {beneficiario.telefono or 'Sin telefono'}",
                                                size=12,
                                                color=_MUTED,
                                            ),
                                        ],
                                        spacing=4,
                                        expand=True,
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT_OUTLINED,
                                        icon_color=_MUTED,
                                        tooltip="Editar beneficiario",
                                        on_click=lambda e, ben=beneficiario, pid=focus_poliza_id or getattr(beneficiario, "id_poliza", None): self._open_edit_beneficiario_modal(ben, focus_poliza_id=pid),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE_OUTLINE_ROUNDED,
                                        icon_color=_ERROR,
                                        tooltip="Eliminar beneficiario",
                                        on_click=lambda e, bid=beneficiario.id_beneficiario, pid=focus_poliza_id or getattr(beneficiario, "id_poliza", None): self._confirm_delete_beneficiario(bid, focus_poliza_id=pid),
                                    ),
                                ],
                                spacing=10,
                                vertical_alignment=ft.CrossAxisAlignment.CENTER,
                            ),
                            *( [ft.Row(policy_row, spacing=8, wrap=True)] if policy_row else [] ),
                        ],
                        spacing=8,
                    ),
                    padding=ft.Padding.all(12),
                    bgcolor=_CARD2,
                    border_radius=10,
                    border=ft.Border.all(1, _BORDER),
                )
            )
        return rows

    def _open_edit_beneficiario_modal(self, beneficiario, *, focus_poliza_id: int | None = None) -> None:
        poliza_dd = _dropdown(
            "Poliza vinculada",
            [
                ft.dropdown.Option(key=str(poliza.id_poliza), text=poliza.numero_poliza)
                for poliza in self._polizas
            ],
            value=str(getattr(beneficiario, "id_poliza", "") or "") or None,
        )
        nombre_f = _field("Nombre completo", beneficiario.nombre_completo)
        parentesco_f = _dropdown(
            "Parentesco",
            _PARENTESCO_OPCIONES,
            value=beneficiario.parentesco or None,
        )
        porcentaje_f = _field(
            "Porcentaje (%)",
            str(beneficiario.porcentaje_participacion),
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        telefono_f = _field("Telefono (opcional)", beneficiario.telefono or "", keyboard_type=ft.KeyboardType.PHONE)
        err_t = ft.Text("", color=_ERROR, size=12)

        def _guardar(e):
            try:
                porcentaje = float(porcentaje_f.value or "0")
                if porcentaje <= 0:
                    raise ValueError
            except ValueError:
                err_t.value = "El porcentaje debe ser un numero positivo."
                self._page.update()
                return

            if self._polizas and not poliza_dd.value:
                err_t.value = "Selecciona la poliza a la que pertenece este beneficiario."
                self._page.update()
                return

            selected_poliza_id = int(poliza_dd.value) if poliza_dd.value else None

            response = BeneficiarioController.update_beneficiario(
                beneficiario.id_beneficiario,
                {
                    "id_poliza": selected_poliza_id,
                    "nombre_completo": nombre_f.value.strip(),
                    "parentesco": parentesco_f.value.strip(),
                    "porcentaje_participacion": porcentaje,
                    "telefono": telefono_f.value.strip() or None,
                },
            )
            if response["ok"]:
                self._close_dialog()
                self._reload(
                    focus_poliza_id=selected_poliza_id or focus_poliza_id,
                    focus_tab="beneficiarios",
                )
            else:
                err_t.value = response.get("error", "No fue posible actualizar el beneficiario.")
                self._page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar beneficiario", color=_TEXT),
            bgcolor=_CARD,
            content=ft.Column([poliza_dd, nombre_f, parentesco_f, porcentaje_f, telefono_f, err_t], spacing=12, tight=True, width=400),
            actions=[
                ft.TextButton("Cancelar", style=ft.ButtonStyle(color=_MUTED), on_click=lambda e: self._close_dialog()),
                ft.FilledButton(
                    "Guardar",
                    style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"),
                    on_click=_guardar,
                ),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._show_dialog(dlg)

    def _confirm_delete_beneficiario(self, id_beneficiario: int, *, focus_poliza_id: int | None = None) -> None:
        btn_delete = ft.FilledButton(
            "Eliminar",
            style=ft.ButtonStyle(bgcolor=_ERROR, color=_TEXT),
        )

        def _delete(e):
            btn_delete.disabled = True
            self._page.update()
            BeneficiarioController.delete_beneficiario(id_beneficiario)
            self._close_dialog()
            self._reload(focus_poliza_id=focus_poliza_id, focus_tab="beneficiarios")

        btn_delete.on_click = _delete
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar beneficiario", color=_ERROR),
            bgcolor=_CARD,
            content=ft.Text("Esta accion eliminara el beneficiario seleccionado.", color=_MUTED, size=13),
            actions=[
                ft.TextButton("Cancelar", style=ft.ButtonStyle(color=_MUTED), on_click=lambda e: self._close_dialog()),
                btn_delete,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._show_dialog(dlg)

    def _build_beneficios_section(self) -> ft.Container:
        if not self._polizas:
            return _section(
                "Beneficios",
                [
                    ft.Text(
                        "Primero crea o vincula una poliza para poder asignar beneficios a esta persona.",
                        size=13,
                        color=_MUTED,
                    )
                ],
            )

        controls: list[ft.Control] = []
        poliza_destacada = next(
            (poliza for poliza in self._polizas if poliza.id_poliza == self._focus_poliza_id),
            None,
        )
        if poliza_destacada is not None:
            controls.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.CHECK_CIRCLE_ROUNDED, color=_ACCENT, size=18),
                            ft.Text(
                                f"Vinculo completado. Continua con los beneficios de la poliza {poliza_destacada.numero_poliza}.",
                                size=13,
                                color=_TEXT,
                                weight=ft.FontWeight.W_600,
                            ),
                        ],
                        spacing=8,
                    ),
                    padding=12,
                    bgcolor=ft.Colors.with_opacity(0.12, _ACCENT),
                    border_radius=10,
                    border=ft.Border.all(1, ft.Colors.with_opacity(0.2, _ACCENT)),
                )
            )
        controls.append(
            ft.Text(
                "Selecciona la poliza en la que estas trabajando. Los nuevos beneficios se agregan solo desde plantillas existentes del catalogo.",
                size=13,
                color=_MUTED,
            )
        )

        selected_poliza_id = next(
            (
                poliza.id_poliza
                for poliza in self._polizas
                if poliza.id_poliza == self._focus_poliza_id
            ),
            self._polizas[0].id_poliza,
        )
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
                self._build_beneficio_poliza_card(poliza) if poliza is not None else None
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

        controls.extend(
            [
                ft.Text("Poliza en trabajo", size=12, color=_MUTED),
                selector_row,
                active_poliza_content,
            ]
        )

        _sync_selected_poliza(update_page=False)

        return _section("Beneficios", controls)

    def _build_beneficio_poliza_card(self, poliza) -> ft.Container:
        participantes = self._participantes_map.get(poliza.id_poliza, [])
        beneficios = list(self._beneficios_map.get(poliza.id_poliza, []))

        producto = self._producto_map.get(poliza.id_producto)
        role = self._poliza_rol_map.get(poliza.id_poliza, "titular")
        role_label = _PART_LABELS.get(role, role.capitalize())
        prima_resumen_t = ft.Text("", size=12, color=_MUTED)
        status_info_t = ft.Text("", size=12, color=_MUTED)
        pending_statuses: dict[int, bool] = {}
        table_rows_col = ft.Column(spacing=6)

        def _money(value) -> str:
            return f"${float(value or 0):,.2f}"

        def _monto_final(beneficio) -> float:
            if getattr(beneficio, "monto_override", None) is None:
                return float(getattr(beneficio, "monto_cobertura", 0) or 0)
            return float(beneficio.monto_override or 0)

        def _effective_vigente(beneficio) -> bool:
            if beneficio.id_beneficio in pending_statuses:
                return bool(pending_statuses[beneficio.id_beneficio])
            return bool(getattr(beneficio, "vigente", True))

        def _refresh_status_info(*, update_page: bool = False) -> None:
            if pending_statuses:
                status_info_t.value = (
                    f"Hay {len(pending_statuses)} cambio(s) de estado pendiente(s). "
                    "Presiona 'Guardar estados'."
                )
                status_info_t.color = _WARN
            else:
                status_info_t.value = "Sin cambios de estado pendientes."
                status_info_t.color = _MUTED
            if update_page:
                self._page.update()

        def _update_prima_display(beneficios_list: list | None = None) -> None:
            """Recalcula y muestra la prima en pantalla SIN escribir a la BD."""
            lista = beneficios_list if beneficios_list is not None else beneficios
            prima_base = float(getattr(producto, "prima_base", 0) or 0)
            costo_beneficios = 0.0
            ajuste_total = 0.0
            for ben in lista:
                if not _effective_vigente(ben):
                    continue
                costo_beneficios += float(getattr(ben, "costo_aplicado", 0) or 0)
                if getattr(ben, "monto_override", None) is None:
                    continue
                monto_base = float(getattr(ben, "monto_cobertura", 0) or 0)
                monto_fin = float(ben.monto_override or 0)
                ajuste_total += (monto_fin - monto_base)
            prima_final = max(0.0, prima_base + costo_beneficios + ajuste_total)
            prima_resumen_t.value = (
                f"Prima base: {_money(prima_base)} · Costo beneficios: {_money(costo_beneficios)} · Ajuste por overrides: {_money(ajuste_total)} · "
                f"Prima final: {_money(prima_final)}"
            )

        def _recalculate_and_sync_prima() -> tuple[bool, str | None]:
            refreshed = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
            if not refreshed.get("ok"):
                return False, refreshed.get("error", "No fue posible recalcular la prima.")

            beneficios_actuales = list(refreshed.get("data", []))
            self._beneficios_map[poliza.id_poliza] = beneficios_actuales

            prima_base = float(getattr(producto, "prima_base", 0) or 0)
            costo_beneficios = 0.0
            ajuste_total = 0.0
            for beneficio in beneficios_actuales:
                if not getattr(beneficio, "vigente", True):
                    continue
                costo_beneficios += float(getattr(beneficio, "costo_aplicado", 0) or 0)
                if getattr(beneficio, "monto_override", None) is None:
                    continue
                monto_base = float(getattr(beneficio, "monto_cobertura", 0) or 0)
                monto_final = float(beneficio.monto_override or 0)
                ajuste_total += (monto_final - monto_base)

            prima_final = max(0.0, prima_base + costo_beneficios + ajuste_total)
            if prima_final > 0:
                update_res = PolizaController.update_poliza(poliza.id_poliza, {"prima_mensual": prima_final})
                if not update_res.get("ok"):
                    return False, update_res.get("error", "No fue posible actualizar la prima mensual.")
                poliza.prima_mensual = prima_final
            _update_prima_display(beneficios_actuales)
            return True, None

        def _open_monto_form(beneficio) -> None:
            override_f = _field(
                "Override de monto (opcional)",
                str(float(beneficio.monto_override)) if getattr(beneficio, "monto_override", None) is not None else "",
                keyboard_type=ft.KeyboardType.NUMBER,
            )
            err_t = ft.Text("", color=_ERROR, size=12)

            def _save_form(_event=None) -> None:
                try:
                    monto_override = None
                    raw = (override_f.value or "").strip()
                    if raw:
                        monto_override = float(raw)
                        if monto_override <= 0:
                            raise ValueError
                except ValueError:
                    err_t.value = "El override debe ser un número mayor a 0."
                    self._page.update()
                    return

                payload = {
                    "id_asegurado_poliza": beneficio.id_asegurado_poliza,
                    "monto_override": monto_override,
                    "vigente": _effective_vigente(beneficio),
                }
                response = BeneficioController.update_beneficio(beneficio.id_beneficio, payload)

                if not response.get("ok"):
                    err_t.value = response.get("error", "No fue posible guardar el beneficio.")
                    self._page.update()
                    return

                ok, err = _recalculate_and_sync_prima()
                if not ok:
                    err_t.value = err or "No fue posible recalcular la prima mensual."
                    self._page.update()
                    return

                self._close_dialog()
                self._reload(focus_poliza_id=poliza.id_poliza, focus_tab="beneficios")

            dlg = ft.AlertDialog(
                modal=True,
                title=ft.Text("Editar monto del beneficio", color=_TEXT),
                bgcolor=_CARD,
                content=ft.Column(
                    [
                        override_f,
                        err_t,
                    ],
                    spacing=10,
                    tight=True,
                ),
                actions=[
                    ft.TextButton("Cancelar", style=ft.ButtonStyle(color=_MUTED), on_click=lambda e: self._close_dialog()),
                    ft.FilledButton("Guardar", style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"), on_click=_save_form),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            self._show_dialog(dlg)

        def _toggle_beneficio_estado_local(beneficio, vigente: bool) -> None:
            original = bool(getattr(beneficio, "vigente", True))
            if vigente == original:
                pending_statuses.pop(beneficio.id_beneficio, None)
            else:
                pending_statuses[beneficio.id_beneficio] = bool(vigente)
            _update_prima_display()
            _refresh_status_info(update_page=True)

        def _save_status_changes(_event=None) -> None:
            if not pending_statuses:
                status_info_t.value = "No hay cambios de estado por guardar."
                status_info_t.color = _MUTED
                self._page.update()
                return

            for beneficio in beneficios:
                if beneficio.id_beneficio not in pending_statuses:
                    continue
                response = BeneficioController.update_beneficio(
                    beneficio.id_beneficio,
                    {
                        "id_asegurado_poliza": beneficio.id_asegurado_poliza,
                        "monto_override": beneficio.monto_override,
                        "vigente": bool(pending_statuses[beneficio.id_beneficio]),
                    },
                )
                if not response.get("ok"):
                    status_info_t.value = response.get("error", "No fue posible guardar cambios de estado.")
                    status_info_t.color = _ERROR
                    self._page.update()
                    return

            ok, err = _recalculate_and_sync_prima()
            if not ok:
                status_info_t.value = err or "No fue posible recalcular la prima mensual."
                status_info_t.color = _ERROR
                self._page.update()
                return

            self._reload(focus_poliza_id=poliza.id_poliza, focus_tab="beneficios")

        def _discard_status_changes(_event=None) -> None:
            pending_statuses.clear()
            _update_prima_display()
            _refresh_status_info(update_page=False)
            _render_table(update_page=False)
            self._page.update()

        def _render_table(_event=None, *, update_page: bool = False) -> None:
            rows: list[ft.Control] = []
            filtered_beneficios = beneficios

            header = ft.Container(
                content=ft.Row(
                    [
                        ft.Text("Nombre del beneficio", size=11, color=_MUTED, weight=ft.FontWeight.W_600, expand=2),
                        ft.Text("Descripción", size=11, color=_MUTED, weight=ft.FontWeight.W_600, expand=2),
                        ft.Text("Monto", size=11, color=_MUTED, weight=ft.FontWeight.W_600, expand=3),
                        ft.Text("Estado", size=11, color=_MUTED, weight=ft.FontWeight.W_600, expand=2),
                        ft.Text("Acciones", size=11, color=_MUTED, weight=ft.FontWeight.W_600, expand=1),
                    ],
                    spacing=12,
                ),
                padding=ft.Padding.symmetric(horizontal=10, vertical=8),
                border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
                bgcolor=_CARD,
                border_radius=8,
            )
            rows.append(header)

            if not filtered_beneficios:
                rows.append(
                    ft.Container(
                        content=ft.Text("Sin beneficios registrados para esta póliza.", size=12, color=_MUTED),
                        padding=ft.Padding.symmetric(horizontal=12, vertical=12),
                        bgcolor=_CARD,
                        border_radius=8,
                        border=ft.Border.all(1, _BORDER),
                    )
                )
            else:
                for beneficio in filtered_beneficios:
                    base_monto = float(getattr(beneficio, "monto_cobertura", 0) or 0)
                    final_monto = _monto_final(beneficio)
                    costo_aplicado = float(getattr(beneficio, "costo_aplicado", 0) or 0)
                    has_override = getattr(beneficio, "monto_override", None) is not None

                    estado_switch = ft.Switch(
                        value=_effective_vigente(beneficio),
                        active_color=_ACCENT,
                        on_change=lambda e, ben=beneficio: _toggle_beneficio_estado_local(ben, bool(e.control.value)),
                    )

                    row = ft.Container(
                        content=ft.Row(
                            [
                                ft.Text(beneficio.nombre_beneficio, size=12, color=_TEXT, weight=ft.FontWeight.W_600, expand=2),
                                ft.Text(
                                    beneficio.descripcion or "Sin descripción",
                                    size=12,
                                    color=_MUTED,
                                    max_lines=1,
                                    overflow=ft.TextOverflow.ELLIPSIS,
                                    expand=2,
                                ),
                                ft.Container(
                                    content=ft.Column(
                                        [
                                            ft.Text(f"Base: {_money(base_monto)}", size=11, color=_MUTED),
                                            ft.Text(f"Costo aplicado: {_money(costo_aplicado)}", size=11, color=_BLUE if costo_aplicado else _MUTED),
                                            ft.Row(
                                                [
                                                    ft.Text(f"Final: {_money(final_monto)}", size=12, color=_TEXT, weight=ft.FontWeight.W_600),
                                                    _pill("Override" if has_override else "Sin override", _WARN if has_override else _MUTED, ft.Colors.with_opacity(0.12, _WARN if has_override else _MUTED)),
                                                ],
                                                spacing=6,
                                                wrap=True,
                                            ),
                                        ],
                                        spacing=2,
                                    ),
                                    expand=3,
                                ),
                                ft.Container(
                                    content=ft.Row(
                                        [
                                            estado_switch,
                                            ft.Text("Activo" if bool(estado_switch.value) else "Inactivo", size=11, color=_TEXT),
                                        ],
                                        spacing=4,
                                    ),
                                    expand=2,
                                ),
                                ft.Container(
                                    content=ft.TextButton(
                                        "Editar monto",
                                        style=ft.ButtonStyle(color=_ACCENT),
                                        on_click=lambda e, ben=beneficio: _open_monto_form(ben),
                                    ),
                                    alignment=ft.Alignment.CENTER_LEFT,
                                    expand=1,
                                ),
                            ],
                            spacing=12,
                            vertical_alignment=ft.CrossAxisAlignment.CENTER,
                        ),
                        padding=ft.Padding.symmetric(horizontal=10, vertical=10),
                        bgcolor=_CARD,
                        border_radius=8,
                        border=ft.Border.all(1, _BORDER),
                    )
                    rows.append(row)

            table_rows_col.controls = rows
            if update_page:
                self._page.update()

        _refresh_status_info(update_page=False)
        _update_prima_display()
        _render_table(update_page=False)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Text(
                                f"Póliza {poliza.numero_poliza}",
                                size=14,
                                weight=ft.FontWeight.W_600,
                                color=_TEXT,
                            ),
                            _pill(f"Producto: {producto.nombre if producto else poliza.numero_poliza}", _ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)),
                            _pill(f"Rol actual: {role_label}", _BLUE, ft.Colors.with_opacity(0.12, _BLUE)),
                            ft.Container(expand=True),
                            ft.FilledButton(
                                "Guardar estados",
                                style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"),
                                on_click=_save_status_changes,
                            ),
                            ft.OutlinedButton(
                                "Descartar cambios",
                                style=ft.ButtonStyle(
                                    color=_TEXT,
                                    side={ft.ControlState.DEFAULT: ft.BorderSide(1, _BORDER)},
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=_discard_status_changes,
                            ),
                        ],
                        spacing=8,
                    ),
                    prima_resumen_t,
                    status_info_t,
                    ft.Divider(color=_BORDER, height=8),
                    ft.Text("Se muestran todos los beneficios de la póliza (activos e inactivos).", size=12, color=_MUTED),
                    table_rows_col,
                ],
                spacing=10,
            ),
            padding=16,
            bgcolor=_CARD2,
            border_radius=12,
            border=ft.Border.all(1, _BORDER),
        )

    def _open_edit_beneficio_modal(self, id_poliza: int, beneficio, participantes: list[dict]) -> None:
        override_f = _field(
            "Override de monto (opcional)",
            str(beneficio.monto_override) if beneficio.monto_override is not None else "",
            keyboard_type=ft.KeyboardType.NUMBER,
        )
        vigente_sw = ft.Switch(value=bool(getattr(beneficio, "vigente", True)), active_color=_ACCENT)
        err_t = ft.Text("", color=_ERROR, size=12)

        def _guardar(e):
            try:
                monto_override = None
                if (override_f.value or "").strip():
                    monto_override = float(override_f.value)
                if monto_override is not None and monto_override <= 0:
                    raise ValueError
            except ValueError:
                err_t.value = "El override debe ser un numero positivo."
                self._page.update()
                return

            response = BeneficioController.update_beneficio(
                beneficio.id_beneficio,
                {
                    "id_asegurado_poliza": beneficio.id_asegurado_poliza,
                    "monto_override": monto_override,
                    "vigente": bool(vigente_sw.value),
                },
            )
            if response["ok"]:
                self._close_dialog()
                self._recalculate_prima_poliza(id_poliza)
                self._navigate(
                    "/asegurado/asignaciones",
                    id_asegurado=self._id,
                    focus_poliza_id=id_poliza,
                )
            else:
                err_t.value = response.get("error", "No fue posible actualizar el beneficio.")
                self._page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar beneficio", color=_TEXT),
            bgcolor=_CARD,
            content=ft.Column(
                [
                    override_f,
                    ft.Row([ft.Text("Activo", size=12, color=_MUTED), vigente_sw], spacing=8),
                    err_t,
                ],
                spacing=10,
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", style=ft.ButtonStyle(color=_MUTED), on_click=lambda e: self._close_dialog()),
                ft.FilledButton("Guardar", style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"), on_click=_guardar),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._show_dialog(dlg)

    def _recalculate_prima_poliza(self, id_poliza: int) -> None:
        poliza_res = PolizaController.get_poliza_by_id(id_poliza)
        if not poliza_res.get("ok") or poliza_res.get("data") is None:
            return

        poliza = poliza_res["data"]
        producto = self._producto_map.get(poliza.id_producto)
        prima_base = float(getattr(producto, "prima_base", 0) or 0)

        beneficios_res = BeneficioController.get_beneficios_by_poliza(id_poliza)
        beneficios = list(beneficios_res.get("data", []) if beneficios_res.get("ok") else [])

        costo_beneficios = 0.0
        ajuste_total = 0.0
        for beneficio in beneficios:
            if not getattr(beneficio, "vigente", True):
                continue
            costo_beneficios += float(getattr(beneficio, "costo_aplicado", 0) or 0)
            if getattr(beneficio, "monto_override", None) is None:
                continue
            monto_base = float(getattr(beneficio, "monto_cobertura", 0) or 0)
            monto_final = float(beneficio.monto_override or 0)
            ajuste_total += (monto_final - monto_base)

        prima_final = max(0.0, prima_base + costo_beneficios + ajuste_total)
        if prima_final > 0:
            PolizaController.update_poliza(id_poliza, {"prima_mensual": prima_final})

    def _confirm_delete_beneficio(self, id_beneficio: int, id_poliza: int | None = None) -> None:
        btn_delete = ft.FilledButton(
            "Eliminar",
            style=ft.ButtonStyle(bgcolor=_ERROR, color=_TEXT),
        )

        def _delete(e):
            btn_delete.disabled = True
            self._page.update()
            BeneficioController.delete_beneficio(id_beneficio)
            self._close_dialog()
            if id_poliza is not None:
                self._recalculate_prima_poliza(id_poliza)
                self._navigate(
                    "/asegurado/asignaciones",
                    id_asegurado=self._id,
                    focus_poliza_id=id_poliza,
                )
            else:
                self._reload()

        btn_delete.on_click = _delete
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar beneficio", color=_ERROR),
            bgcolor=_CARD,
            content=ft.Text("Esta accion eliminara el beneficio seleccionado.", color=_MUTED, size=13),
            actions=[
                ft.TextButton("Cancelar", style=ft.ButtonStyle(color=_MUTED), on_click=lambda e: self._close_dialog()),
                btn_delete,
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._show_dialog(dlg)