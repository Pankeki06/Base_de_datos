"""Vista de administración de agentes (solo admin)."""

from __future__ import annotations

import flet as ft

from controllers.agente_controller import AgenteController
from services.session_manager import obtener_agente
from views.theme import (
    ACCENT as _ACCENT,
    BG as _BG,
    BORDER as _BORDER,
    CARD as _CARD,
    CARD_ALT as _CARD2,
    ERROR as _ERROR,
    MUTED as _MUTED,
    TEXT as _TEXT,
)
from views.ui_controls import app_sidebar, styled_dropdown as _dd, styled_text_field as _tf


_ACTIONS_COL_WIDTH = 84


class ListaAgentesView:
    def __init__(self, page: ft.Page, navigate) -> None:
        self._page = page
        self._navigate = navigate
        self._agente = obtener_agente()
        self._agentes: list = []
        self._feedback_t = ft.Text("", size=12, color=_MUTED)
        self._table_col = ft.Column(spacing=6)

    def _is_admin(self) -> bool:
        rol = getattr(self._agente, "rol", "")
        return str(rol).lower() == "admin"

    def _show_dialog(self, dialog: ft.AlertDialog) -> None:
        self._page.show_dialog(dialog)

    def _close_dialog(self) -> None:
        self._page.pop_dialog()

    def _load_data(self) -> None:
        if not self._is_admin():
            self._agentes = []
            return
        result = AgenteController.get_all_agentes()
        self._agentes = list(result.get("data", [])) if result.get("ok") else []

    def build(self) -> ft.Control:
        self._load_data()
        sidebar = app_sidebar(self._navigate, "/agentes")
        return ft.Container(
            content=ft.Row([sidebar, self._build_main()], spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    def _build_main(self) -> ft.Container:
        topbar = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Administración de agentes", size=20, weight=ft.FontWeight.BOLD, color=_TEXT),
                    ft.Container(expand=True),
                    ft.FilledButton(
                        "Nuevo agente",
                        style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"),
                        disabled=not self._is_admin(),
                        on_click=lambda e: self._open_create_modal(),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=28, vertical=20),
            border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

        if not self._is_admin():
            unauthorized = ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.LOCK_ROUNDED, size=42, color=_MUTED),
                        ft.Text("Acceso restringido", size=18, color=_TEXT, weight=ft.FontWeight.W_600),
                        ft.Text(
                            "Solo los administradores pueden gestionar agentes y roles.",
                            size=13,
                            color=_MUTED,
                            text_align=ft.TextAlign.CENTER,
                        ),
                        ft.FilledButton(
                            "Volver al dashboard",
                            style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"),
                            on_click=lambda e: self._navigate("/dashboard"),
                        ),
                    ],
                    spacing=10,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                expand=True,
                alignment=ft.Alignment.CENTER,
            )
            body = ft.Container(content=unauthorized, expand=True, padding=ft.Padding.all(24))
            return ft.Container(content=ft.Column([topbar, body], spacing=0, expand=True), expand=True, bgcolor=_BG)

        self._render_table(update_page=False)
        body = ft.Container(
            content=ft.Column(
                [
                    self._feedback_t,
                    self._table_col,
                ],
                spacing=10,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=ft.Padding.symmetric(horizontal=24, vertical=16),
            expand=True,
        )

        return ft.Container(
            content=ft.Column([topbar, body], spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    def _render_table(self, *, update_page: bool = True) -> None:
        rows: list[ft.Control] = []

        header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Nombre", size=11, color=_MUTED, weight=ft.FontWeight.W_600, expand=2),
                    ft.Text("Clave", size=11, color=_MUTED, weight=ft.FontWeight.W_600, expand=1),
                    ft.Text("Correo", size=11, color=_MUTED, weight=ft.FontWeight.W_600, expand=2),
                    ft.Text("Teléfono", size=11, color=_MUTED, weight=ft.FontWeight.W_600, expand=1),
                    ft.Text("Rol", size=11, color=_MUTED, weight=ft.FontWeight.W_600, expand=1),
                    ft.Container(
                        content=ft.Text("Acciones", size=11, color=_MUTED, weight=ft.FontWeight.W_600),
                        width=_ACTIONS_COL_WIDTH,
                        alignment=ft.Alignment.CENTER_RIGHT,
                    ),
                ],
                spacing=10,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=8),
            border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
            bgcolor=_CARD,
            border_radius=8,
        )
        rows.append(header)

        if not self._agentes:
            rows.append(
                ft.Container(
                    content=ft.Text("No hay agentes registrados.", size=13, color=_MUTED),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=12),
                    bgcolor=_CARD,
                    border_radius=8,
                    border=ft.Border.all(1, _BORDER),
                )
            )
        else:
            for agente in self._agentes:
                nombre = f"{agente.nombre} {agente.apellido_paterno} {agente.apellido_materno}".strip()
                rol_color = _ACCENT if str(getattr(agente, "rol", "")).lower() == "admin" else _MUTED

                row = ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(
                                nombre,
                                size=12,
                                color=_TEXT,
                                expand=2,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                agente.clave_agente,
                                size=12,
                                color=_MUTED,
                                expand=1,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                agente.correo,
                                size=12,
                                color=_MUTED,
                                expand=2,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Text(
                                getattr(agente, "telefono", "") or "—",
                                size=12,
                                color=_MUTED,
                                expand=1,
                                max_lines=1,
                                overflow=ft.TextOverflow.ELLIPSIS,
                            ),
                            ft.Container(
                                content=ft.Text(str(getattr(agente, "rol", "")).capitalize(), size=12, color=rol_color),
                                expand=1,
                            ),
                            ft.Container(
                                content=ft.PopupMenuButton(
                                    icon=ft.Icons.MORE_VERT_ROUNDED,
                                    icon_color=_MUTED,
                                    items=[
                                        ft.PopupMenuItem(
                                            content=ft.Row(
                                                [
                                                    ft.Icon(ft.Icons.EDIT_ROUNDED, size=16, color=_ACCENT),
                                                    ft.Text("Editar", color=_TEXT),
                                                ],
                                                spacing=8,
                                                tight=True,
                                            ),
                                            on_click=lambda e, ag=agente: self._open_edit_modal(ag),
                                        ),
                                        ft.PopupMenuItem(
                                            content=ft.Row(
                                                [
                                                    ft.Icon(ft.Icons.DELETE_OUTLINE_ROUNDED, size=16, color=_ERROR),
                                                    ft.Text("Eliminar", color=_TEXT),
                                                ],
                                                spacing=8,
                                                tight=True,
                                            ),
                                            on_click=lambda e, ag=agente: self._confirm_delete(ag),
                                        ),
                                    ],
                                ),
                                width=_ACTIONS_COL_WIDTH,
                                alignment=ft.Alignment.CENTER_RIGHT,
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    padding=ft.Padding.symmetric(horizontal=10, vertical=10),
                    bgcolor=_CARD2,
                    border_radius=8,
                    border=ft.Border.all(1, _BORDER),
                )
                rows.append(row)

        self._table_col.controls = rows
        if update_page:
            self._page.update()

    def _open_create_modal(self) -> None:
        clave_f = _tf("Clave agente")
        cedula_f = _tf("Cédula")
        nombre_f = _tf("Nombre")
        ap_pat_f = _tf("Apellido paterno")
        ap_mat_f = _tf("Apellido materno")
        correo_f = _tf("Correo")
        telefono_f = _tf("Teléfono")
        rol_dd = _dd(
            "Rol",
            [
                ft.dropdown.Option(key="admin", text="Administrador"),
                ft.dropdown.Option(key="agente", text="Agente"),
            ],
            value="agente",
        )
        password_f = _tf("Contraseña", password=True, can_reveal_password=True)
        err_t = ft.Text("", color=_ERROR, size=12)

        def _save(_event=None) -> None:
            payload = {
                "clave_agente": (clave_f.value or "").strip(),
                "cedula": (cedula_f.value or "").strip(),
                "nombre": (nombre_f.value or "").strip(),
                "apellido_paterno": (ap_pat_f.value or "").strip(),
                "apellido_materno": (ap_mat_f.value or "").strip(),
                "correo": (correo_f.value or "").strip(),
                "telefono": (telefono_f.value or "").strip(),
                "rol": rol_dd.value,
                "password": password_f.value or "",
            }
            result = AgenteController.create_agente(payload)
            if not result.get("ok"):
                err_t.value = result.get("error", "No fue posible crear el agente.")
                self._page.update()
                return

            self._close_dialog()
            self._feedback_t.value = "Agente creado correctamente."
            self._feedback_t.color = _ACCENT
            self._load_data()
            self._render_table(update_page=False)
            self._page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Crear agente", color=_TEXT),
            bgcolor=_CARD,
            content=ft.Column(
                [
                    clave_f,
                    cedula_f,
                    nombre_f,
                    ap_pat_f,
                    ap_mat_f,
                    correo_f,
                    telefono_f,
                    rol_dd,
                    password_f,
                    err_t,
                ],
                spacing=8,
                tight=True,
                width=420,
                height=530,
                scroll=ft.ScrollMode.AUTO,
            ),
            actions=[
                ft.TextButton("Cancelar", style=ft.ButtonStyle(color=_MUTED), on_click=lambda e: self._close_dialog()),
                ft.FilledButton("Guardar", style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"), on_click=_save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._show_dialog(dlg)

    def _open_edit_modal(self, agente) -> None:
        nombre_f = _tf("Nombre", value=str(getattr(agente, "nombre", "")))
        ap_pat_f = _tf("Apellido paterno", value=str(getattr(agente, "apellido_paterno", "")))
        ap_mat_f = _tf("Apellido materno", value=str(getattr(agente, "apellido_materno", "")))
        correo_f = _tf("Correo", value=str(getattr(agente, "correo", "")))
        telefono_f = _tf("Teléfono", value=str(getattr(agente, "telefono", "") or ""))
        rol_dd = _dd(
            "Rol",
            [
                ft.dropdown.Option(key="admin", text="Administrador"),
                ft.dropdown.Option(key="agente", text="Agente"),
            ],
            value=str(getattr(agente, "rol", "agente")),
        )
        password_f = _tf("Nueva contraseña (opcional)", password=True, can_reveal_password=True)
        err_t = ft.Text("", color=_ERROR, size=12)

        def _save(_event=None) -> None:
            payload = {
                "nombre": (nombre_f.value or "").strip(),
                "apellido_paterno": (ap_pat_f.value or "").strip(),
                "apellido_materno": (ap_mat_f.value or "").strip(),
                "correo": (correo_f.value or "").strip(),
                "telefono": (telefono_f.value or "").strip(),
                "rol": rol_dd.value,
            }
            if (password_f.value or "").strip():
                payload["password"] = password_f.value

            result = AgenteController.update_agente(agente.id_agente, payload)
            if not result.get("ok"):
                err_t.value = result.get("error", "No fue posible actualizar el agente.")
                self._page.update()
                return

            self._close_dialog()
            self._feedback_t.value = "Agente actualizado correctamente."
            self._feedback_t.color = _ACCENT
            self._load_data()
            self._render_table(update_page=False)
            self._page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar agente", color=_TEXT),
            bgcolor=_CARD,
            content=ft.Column(
                [
                    nombre_f,
                    ap_pat_f,
                    ap_mat_f,
                    correo_f,
                    telefono_f,
                    rol_dd,
                    password_f,
                    err_t,
                ],
                spacing=8,
                tight=True,
                width=420,
            ),
            actions=[
                ft.TextButton("Cancelar", style=ft.ButtonStyle(color=_MUTED), on_click=lambda e: self._close_dialog()),
                ft.FilledButton("Guardar", style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"), on_click=_save),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._show_dialog(dlg)

    def _confirm_delete(self, agente) -> None:
        if self._agente and agente.id_agente == getattr(self._agente, "id_agente", None):
            self._feedback_t.value = "No puedes eliminar tu propio usuario mientras tienes sesión activa."
            self._feedback_t.color = _ERROR
            self._page.update()
            return

        err_t = ft.Text("", color=_ERROR, size=12)

        def _delete(_event=None) -> None:
            result = AgenteController.delete_agente(agente.id_agente)
            if not result.get("ok"):
                err_t.value = result.get("error", "No fue posible eliminar el agente.")
                self._page.update()
                return

            self._close_dialog()
            self._feedback_t.value = "Agente eliminado correctamente."
            self._feedback_t.color = _ACCENT
            self._load_data()
            self._render_table(update_page=False)
            self._page.update()

        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Eliminar agente", color=_TEXT),
            bgcolor=_CARD,
            content=ft.Column(
                [
                    ft.Text(
                        f"¿Eliminar a {agente.nombre} {agente.apellido_paterno}? Esta acción es lógica (soft-delete).",
                        color=_TEXT,
                    ),
                    err_t,
                ],
                tight=True,
                spacing=8,
                width=380,
            ),
            actions=[
                ft.TextButton("Cancelar", style=ft.ButtonStyle(color=_MUTED), on_click=lambda e: self._close_dialog()),
                ft.FilledButton("Eliminar", style=ft.ButtonStyle(bgcolor=_ERROR, color="#FFFFFF"), on_click=_delete),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        self._show_dialog(dlg)
