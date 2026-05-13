"""Vista de detalle de un folio de seguimiento con historial de contactos."""

from __future__ import annotations

import flet as ft

from controllers.asegurado_controller import AseguradoController
from controllers.agente_controller import AgenteController
from controllers.seguimiento_controller import SeguimientoController
from controllers.seguimiento_contacto_controller import SeguimientoContactoController
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


class DetalleSeguimientoView:
    """Detalle de un folio de seguimiento con historial de contactos."""

    # ── Constructor ────────────────────────────────────────────────────────────
    def __init__(self, page: ft.Page, navigate, id_seguimiento: int) -> None:
        self._page = page
        self._navigate = navigate
        self._id_seguimiento = id_seguimiento

        self._seguimiento = None
        self._contactos: list = []
        self._asegurado = None
        self._agente = None
        self._contactos_col_ref = ft.Ref[ft.Column]()

    # ── Carga de datos (seguimiento + contactos + asegurado + agente) ──────────
    def _load_data(self) -> None:
        """Carga el seguimiento con sus contactos."""
        # Cargar seguimiento con contactos
        seg_res = SeguimientoController.get_seguimiento_con_contactos(self._id_seguimiento)
        if seg_res["ok"]:
            data = seg_res["data"]
            self._seguimiento = data["seguimiento"]
            self._contactos = data["contactos"]
            
            # Cargar asegurado
            if self._seguimiento:
                aseg_res = AseguradoController.get_asegurado_by_id(
                    self._seguimiento.id_asegurado
                )
                if aseg_res["ok"]:
                    self._asegurado = aseg_res["data"]
                
                # Cargar agente
                agente_res = AgenteController.get_agente_by_id(
                    self._seguimiento.id_agente
                )
                if agente_res["ok"]:
                    self._agente = agente_res["data"]

    # ── Item de contacto para la línea temporal ────────────────────────────────
    def _build_contacto_item(self, contacto) -> ft.Container:
        """Construye un item de contacto para el historial."""
        # Iconos según tipo
        tipo_icons = {
            "llamada": ft.Icons.PHONE_ROUNDED,
            "visita": ft.Icons.PERSON_ROUNDED,
            "mensaje": ft.Icons.MESSAGE_ROUNDED,
        }
        
        # Colores según resultado
        resultado_colors = {
            "resuelto": (_ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)),
            "pendiente": (_WARN, ft.Colors.with_opacity(0.12, _WARN)),
            "sin_respuesta": (_MUTED, _CARD2),
        }
        
        # Quién inició
        iniciado_por = getattr(contacto, "iniciado_por", "agente")
        iniciado_label = "Agente" if iniciado_por == "agente" else "Asegurado"
        iniciado_color = _BLUE if iniciado_por == "agente" else _ACCENT
        
        tipo = getattr(contacto, "tipo_contacto", "llamada")
        resultado = getattr(contacto, "resultado", "sin_respuesta")
        observaciones = getattr(contacto, "observaciones", "")
        fecha_hora = getattr(contacto, "fecha_hora", None)
        
        icon = tipo_icons.get(tipo, ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED)
        res_fg, res_bg = resultado_colors.get(resultado, (_MUTED, _CARD2))
        
        fecha_str = ""
        if fecha_hora:
            fecha_str = fecha_hora.strftime("%d/%m/%Y %H:%M")

        return ft.Container(
            content=ft.Row(
                [
                    # Línea temporal
                    ft.Column(
                        [
                            ft.Container(
                                width=12,
                                height=12,
                                border_radius=6,
                                bgcolor=_ACCENT,
                            ),
                            ft.Container(
                                width=2,
                                expand=True,
                                bgcolor=ft.Colors.with_opacity(0.2, _BORDER),
                            ),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=0,
                    ),
                    ft.Container(width=12),
                    # Contenido
                    ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Container(
                                        content=ft.Icon(icon, size=16, color=_ACCENT),
                                        width=32,
                                        height=32,
                                        border_radius=8,
                                        bgcolor=ft.Colors.with_opacity(0.12, _ACCENT),
                                        alignment=ft.Alignment.CENTER,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Text(
                                                        tipo.capitalize(),
                                                        size=13,
                                                        weight=ft.FontWeight.W_600,
                                                        color=_TEXT,
                                                    ),
                                                    _pill(
                                                        iniciado_label,
                                                        iniciado_color,
                                                        ft.Colors.with_opacity(0.12, iniciado_color),
                                                    ),
                                                    _pill(
                                                        resultado.replace("_", " ").upper(),
                                                        res_fg,
                                                        res_bg,
                                                    ),
                                                ],
                                                spacing=8,
                                            ),
                                            ft.Text(
                                                fecha_str,
                                                size=11,
                                                color=_MUTED,
                                            ),
                                        ],
                                        spacing=2,
                                        expand=True,
                                    ),
                                ],
                                spacing=8,
                            ),
                            ft.Container(
                                content=ft.Text(
                                    observaciones,
                                    size=13,
                                    color=_TEXT,
                                ),
                                padding=ft.Padding.only(left=40),
                            ),
                        ],
                        spacing=8,
                        expand=True,
                    ),
                ],
                spacing=0,
                vertical_alignment=ft.CrossAxisAlignment.START,
            ),
            padding=ft.Padding.symmetric(vertical=12),
        )

    # ── Estado vacío: sin contactos ────────────────────────────────────────────
    def _build_empty_contactos(self) -> ft.Container:
        """Estado vacío cuando no hay contactos."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, size=48, color=_MUTED),
                    ft.Container(height=12),
                    ft.Text(
                        "Sin contactos",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color=_TEXT,
                    ),
                    ft.Text(
                        "Este folio aún no tiene contactos registrados.",
                        size=12,
                        color=_MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=40,
            alignment=ft.Alignment.CENTER,
        )

    # ── Modal: agregar contacto al folio ───────────────────────────────────────
    def _open_agregar_contacto_modal(self) -> None:
        """Abre modal para agregar un contacto al folio."""
        tipo_dd = _dd("Tipo de contacto", [
            ft.dropdown.Option(key="llamada", text="Llamada"),
            ft.dropdown.Option(key="visita", text="Visita"),
            ft.dropdown.Option(key="mensaje", text="Mensaje"),
        ])
        
        iniciado_dd = _dd("Iniciado por", [
            ft.dropdown.Option(key="agente", text="Agente"),
            ft.dropdown.Option(key="asegurado", text="Asegurado"),
        ])
        
        resultado_dd = _dd("Resultado", [
            ft.dropdown.Option(key="resuelto", text="Resuelto"),
            ft.dropdown.Option(key="pendiente", text="Pendiente"),
            ft.dropdown.Option(key="sin_respuesta", text="Sin respuesta"),
        ])
        
        obs_f = _tf("Observaciones", multiline=True, min_lines=3, max_lines=5)
        fecha_f = _tf("Fecha y hora", hint_text="AAAA-MM-DD HH:MM")
        err_t = ft.Text("", color=_ERROR, size=12)
        
        # Prellenar fecha actual
        from datetime import datetime
        fecha_f.value = datetime.now().strftime("%Y-%m-%d %H:%M")

        def _save(_):
            from datetime import datetime as dt
            
            try:
                fecha_hora = dt.strptime(fecha_f.value.strip(), "%Y-%m-%d %H:%M")
            except (ValueError, AttributeError):
                err_t.value = "Formato inválido. Use AAAA-MM-DD HH:MM."
                self._page.update()
                return
            
            if not tipo_dd.value or not resultado_dd.value:
                err_t.value = "Tipo y resultado son requeridos."
                self._page.update()
                return

            r = SeguimientoContactoController.create_contacto({
                "id_seguimiento": self._id_seguimiento,
                "iniciado_por": iniciado_dd.value or "agente",
                "tipo_contacto": tipo_dd.value,
                "resultado": resultado_dd.value,
                "observaciones": obs_f.value or "",
                "fecha_hora": fecha_hora,
            })
            
            if r["ok"]:
                self._close_dialog()
                self._reload()
            else:
                err_t.value = r.get("error", "Error al guardar contacto.")
                self._page.update()

        dlg = modal_dialog(
            "Agregar contacto",
            ft.Column(
                [
                    ft.Row([tipo_dd, iniciado_dd], spacing=12),
                    resultado_dd,
                    obs_f,
                    fecha_f,
                    ft.Text("Formato: AAAA-MM-DD HH:MM", size=11, color=_MUTED),
                    err_t,
                ],
                spacing=12,
                tight=True,
            ),
            [
                ft.TextButton("Cancelar", on_click=lambda _: self._close_dialog()),
                ft.ElevatedButton(
                    "Guardar",
                    on_click=_save,
                    style=ft.ButtonStyle(bgcolor=_ACCENT, color=ft.Colors.WHITE),
                ),
            ],
            width=450,
        )
        self._page.show_dialog(dlg)

    def _close_dialog(self) -> None:
        self._page.pop_dialog()

    def _reload(self) -> None:
        """Recarga la vista."""
        self._navigate("/seguimiento/detalle", id_seguimiento=self._id_seguimiento)

    # ── Encabezado con info del folio ──────────────────────────────────────────
    def _build_header(self) -> ft.Container:
        """Construye el encabezado con info del folio."""
        folio = ""
        asunto = ""
        asegurado_nombre = ""
        agente_nombre = ""
        fecha_creacion = ""
        
        if self._seguimiento:
            folio = self._seguimiento.folio
            asunto = self._seguimiento.asunto
            if self._seguimiento.created_at:
                fecha_creacion = self._seguimiento.created_at.strftime("%d/%m/%Y")
        
        if self._asegurado:
            asegurado_nombre = f"{self._asegurado.nombre} {self._asegurado.apellido_paterno}"
        
        if self._agente:
            agente_nombre = f"{self._agente.nombre} {self._agente.apellido_paterno}"

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK_ROUNDED,
                                icon_color=_MUTED,
                                on_click=lambda _: self._navigate(
                                    "/seguimiento/lista",
                                    id_asegurado=self._seguimiento.id_asegurado if self._seguimiento else 0,
                                ),
                            ),
                            ft.Column(
                                [
                                    ft.Row(
                                        [
                                            ft.Icon(ft.Icons.FOLDER_OPEN, color=_ACCENT, size=20),
                                            ft.Text(folio, size=18, weight=ft.FontWeight.W_700, color=_TEXT),
                                        ],
                                        spacing=8,
                                    ),
                                    ft.Text(asunto, size=13, color=_MUTED),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                        ],
                        spacing=8,
                    ),
                    ft.Divider(color=_BORDER, height=16),
                    ft.Row(
                        [
                            ft.Column(
                                [
                                    ft.Text("ASEGURADO", size=10, color=_MUTED, weight=ft.FontWeight.W_600),
                                    ft.Text(asegurado_nombre, size=12, color=_TEXT),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.Text("AGENTE", size=10, color=_MUTED, weight=ft.FontWeight.W_600),
                                    ft.Text(agente_nombre, size=12, color=_TEXT),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.Column(
                                [
                                    ft.Text("CREADO", size=10, color=_MUTED, weight=ft.FontWeight.W_600),
                                    ft.Text(fecha_creacion, size=12, color=_TEXT),
                                ],
                                spacing=2,
                            ),
                        ],
                        spacing=24,
                    ),
                ],
                spacing=0,
            ),
            padding=ft.Padding.symmetric(horizontal=20, vertical=16),
            bgcolor=_CARD,
            border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

    # ── Build de la vista completa ─────────────────────────────────────────────
    def build(self) -> ft.Control:
        """Construye y retorna la vista."""
        self._load_data()

        # Construir lista de contactos
        contactos_col = ft.Column(ref=self._contactos_col_ref, spacing=0)

        if self._contactos:
            for i, contacto in enumerate(self._contactos):
                contactos_col.controls.append(self._build_contacto_item(contacto))
        else:
            contactos_col.controls.append(self._build_empty_contactos())

        return ft.Container(
            content=ft.Row(
                [
                    app_sidebar(self._navigate, "/clientes"),
                    ft.Column(
                        [
                            self._build_header(),
                            ft.Container(
                                content=ft.Column(
                                    [
                                        ft.Row(
                                            [
                                                ft.Text(
                                                    "Historial de contactos",
                                                    size=15,
                                                    weight=ft.FontWeight.W_600,
                                                    color=_TEXT,
                                                ),
                                                ft.Container(expand=True),
                                                ft.ElevatedButton(
                                                    "Agregar contacto",
                                                    icon=ft.Icons.ADD_ROUNDED,
                                                    on_click=lambda _: self._open_agregar_contacto_modal(),
                                                    style=ft.ButtonStyle(
                                                        bgcolor=_ACCENT,
                                                        color=ft.Colors.WHITE,
                                                    ),
                                                ),
                                            ],
                                        ),
                                        ft.Divider(color=_BORDER, height=8),
                                        contactos_col,
                                    ],
                                    spacing=12,
                                    scroll=ft.ScrollMode.AUTO,
                                    expand=True,
                                ),
                                padding=20,
                                expand=True,
                            ),
                        ],
                        expand=True,
                        spacing=0,
                    ),
                ],
                expand=True,
                spacing=0,
            ),
            bgcolor=_BG,
            padding=0,
            expand=True,
        )
