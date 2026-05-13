"""Vista de lista de seguimientos (folios) de un asegurado."""

from __future__ import annotations

import flet as ft

from controllers.asegurado_controller import AseguradoController
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
from views.ui_controls import app_sidebar, modal_dialog, pill as _pill, styled_text_field as _tf


class ListaSeguimientosView:
    """Lista de folios de seguimiento de un asegurado."""

    # ── Constructor ────────────────────────────────────────────────────────────
    def __init__(self, page: ft.Page, navigate, id_asegurado: int) -> None:
        self._page = page
        self._navigate = navigate
        self._id_asegurado = id_asegurado

        self._asegurado = None
        self._seguimientos: list[dict] = []  # Cada item: {"seguimiento": ..., "contactos": [...]}
        self._seg_col_ref = ft.Ref[ft.Column]()

    # ── Carga de datos (asegurado + seguimientos) ──────────────────────────────
    def _load_data(self) -> None:
        """Carga los datos del asegurado y sus seguimientos con contactos."""
        # Cargar asegurado
        aseg_res = AseguradoController.get_asegurado_by_id(self._id_asegurado)
        if aseg_res["ok"]:
            self._asegurado = aseg_res["data"]

        # Cargar seguimientos con contactos
        seg_res = SeguimientoController.get_seguimientos_by_asegurado_con_contactos(
            self._id_asegurado
        )
        if seg_res["ok"]:
            self._seguimientos = seg_res["data"]

    # ── Tarjeta de folio con resumen de contactos ──────────────────────────────
    def _build_folio_card(self, item: dict) -> ft.Container:
        """Construye una tarjeta de folio con resumen de contactos."""
        seguimiento = item["seguimiento"]
        contactos = item["contactos"]
        
        # Colores según resultado del último contacto
        resultado_colors = {
            "resuelto": (_ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)),
            "pendiente": (_WARN, ft.Colors.with_opacity(0.12, _WARN)),
            "sin_respuesta": (_MUTED, _CARD2),
        }
        
        # Obtener estado del último contacto
        ultimo_estado = "sin_respuesta"
        if contactos:
            ultimo_contacto = contactos[-1]  # Ya vienen ordenados por fecha
            ultimo_estado = getattr(ultimo_contacto, "resultado", "sin_respuesta")
        
        estado_fg, estado_bg = resultado_colors.get(ultimo_estado, (_MUTED, _CARD2))
        
        # Contador de contactos
        n_contactos = len(contactos)
        contactos_text = f"{n_contactos} contacto{'s' if n_contactos != 1 else ''}"
        
        # Fecha del último contacto
        fecha_ultimo = ""
        if contactos:
            fecha_ultimo = getattr(contactos[-1], "fecha_hora", None)
            if fecha_ultimo:
                fecha_ultimo = f"Último: {fecha_ultimo.strftime('%d/%m/%Y %H:%M')}"
        
        def _on_click(_):
            self._navigate("/seguimiento/detalle", id_seguimiento=seguimiento.id_seguimiento)

        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.FOLDER_OPEN_OUTLINED, color=_ACCENT, size=24),
                            ft.Column(
                                [
                                    ft.Text(
                                        seguimiento.folio,
                                        size=14,
                                        weight=ft.FontWeight.W_600,
                                        color=_TEXT,
                                    ),
                                    ft.Text(
                                        seguimiento.asunto,
                                        size=12,
                                        color=_MUTED,
                                        max_lines=1,
                                        overflow=ft.TextOverflow.ELLIPSIS,
                                    ),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            _pill(
                                ultimo_estado.replace("_", " ").upper(),
                                estado_fg,
                                estado_bg,
                            ),
                        ],
                        spacing=12,
                    ),
                    ft.Divider(color=_BORDER, height=1),
                    ft.Row(
                        [
                            ft.Icon(ft.Icons.CHAT_BUBBLE_OUTLINE, size=14, color=_MUTED),
                            ft.Text(contactos_text, size=11, color=_MUTED),
                            ft.Container(expand=True),
                            ft.Text(fecha_ultimo, size=11, color=_MUTED),
                        ],
                        spacing=6,
                    ),
                ],
                spacing=8,
            ),
            padding=16,
            bgcolor=_CARD,
            border_radius=10,
            border=ft.Border.all(1, _BORDER),
            on_click=_on_click,
            ink=True,
        )

    # ── Estado vacío: sin seguimientos ─────────────────────────────────────────
    def _build_empty_state(self) -> ft.Container:
        """Estado vacío cuando no hay seguimientos."""
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.FOLDER_OPEN_OUTLINED, size=48, color=_MUTED),
                    ft.Container(height=12),
                    ft.Text(
                        "Sin seguimientos",
                        size=16,
                        weight=ft.FontWeight.W_600,
                        color=_TEXT,
                    ),
                    ft.Text(
                        "No hay folios de seguimiento registrados para este asegurado.",
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

    # ── Modal: crear nuevo folio de seguimiento ────────────────────────────────
    def _open_nuevo_folio_modal(self) -> None:
        """Abre modal para crear nuevo folio de seguimiento."""
        from services.session_manager import obtener_agente
        
        folio_f = _tf("Número de folio", hint="ej: SEG-2026-001")
        asunto_f = _tf("Asunto", hint="Descripción breve del caso")
        err_t = ft.Text("", color=_ERROR, size=12)
        
        agente = obtener_agente()

        def _save(_):
            if not folio_f.value or not asunto_f.value:
                err_t.value = "Folio y asunto son requeridos."
                self._page.update()
                return
            
            if agente is None:
                err_t.value = "No hay sesión activa."
                self._page.update()
                return

            r = SeguimientoController.create_seguimiento({
                "folio": folio_f.value.strip(),
                "asunto": asunto_f.value.strip(),
                "id_asegurado": self._id_asegurado,
                "id_agente": agente.id_agente,
            })
            
            if r["ok"]:
                self._close_dialog()
                self._reload()
            else:
                err_t.value = r.get("error", "Error al crear folio.")
                self._page.update()

        dlg = modal_dialog(
            "Nuevo folio de seguimiento",
            ft.Column(
                [
                    folio_f,
                    asunto_f,
                    err_t,
                ],
                spacing=12,
                tight=True,
            ),
            [
                ft.TextButton("Cancelar", on_click=lambda _: self._close_dialog()),
                ft.ElevatedButton(
                    "Crear folio",
                    on_click=_save,
                    style=ft.ButtonStyle(bgcolor=_ACCENT, color=ft.Colors.WHITE),
                ),
            ],
            width=400,
        )
        self._page.show_dialog(dlg)

    def _close_dialog(self) -> None:
        self._page.pop_dialog()

    def _reload(self) -> None:
        """Recarga la vista."""
        self._navigate("/seguimiento/lista", id_asegurado=self._id_asegurado)

    # ── Encabezado con info del asegurado ──────────────────────────────────────
    def _build_header(self) -> ft.Container:
        """Construye el encabezado con info del asegurado."""
        nombre = ""
        if self._asegurado:
            nombre = f"{self._asegurado.nombre} {self._asegurado.apellido_paterno}"
        
        return ft.Container(
            content=ft.Column(
                [
                    ft.Row(
                        [
                            ft.IconButton(
                                icon=ft.Icons.ARROW_BACK_ROUNDED,
                                icon_color=_MUTED,
                                on_click=lambda _: self._navigate("/clientes"),
                            ),
                            ft.Column(
                                [
                                    ft.Text("Seguimientos", size=20, weight=ft.FontWeight.W_700, color=_TEXT),
                                    ft.Text(nombre, size=13, color=_MUTED),
                                ],
                                spacing=2,
                                expand=True,
                            ),
                            ft.ElevatedButton(
                                "Nuevo folio",
                                icon=ft.Icons.ADD_ROUNDED,
                                on_click=lambda _: self._open_nuevo_folio_modal(),
                                style=ft.ButtonStyle(bgcolor=_ACCENT, color=ft.Colors.WHITE),
                            ),
                        ],
                        spacing=8,
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

        # Construir lista de folios
        seg_col = ft.Column(ref=self._seg_col_ref, spacing=12)

        if self._seguimientos:
            for item in self._seguimientos:
                seg_col.controls.append(self._build_folio_card(item))
        else:
            seg_col.controls.append(self._build_empty_state())

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
                                        seg_col,
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
