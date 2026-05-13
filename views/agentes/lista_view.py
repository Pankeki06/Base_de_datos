"""Vista de gestion de agentes."""

from __future__ import annotations

import flet as ft

from controllers.agente_controller import AgenteController
from services.session_manager import obtener_agente
from views.theme import (
    ACCENT as _ACCENT,
    BG as _BG,
    BORDER as _BORDER,
    CARD as _CARD,
    ERROR as _ERROR,
    MUTED as _MUTED,
    TEXT as _TEXT,
)
from views.ui_controls import app_sidebar as _app_sidebar
from views.ui_controls import modal_dialog as _modal_dialog


class ListaAgentesView:
    # ── Constructor y estado de paginación ─────────────────────────────────────
    def __init__(self, page: ft.Page, navigate) -> None:
        self._page = page
        self._navigate = navigate
        self._agentes: list = []
        self._page_size = 20
        self._current_page = 1
        self._total_items = 0
        self._total_pages = 1
        self._nombre_query = ""
        self._modo = "activos"  # "activos" | "desactivados"
        self._tabla = ft.Column(spacing=10)
        self._page_info = ft.Text("", size=12, color=_MUTED)
        self._btn_prev = ft.OutlinedButton("Anterior", disabled=True)
        self._btn_next = ft.OutlinedButton("Siguiente", disabled=True)
        self._search_field = ft.TextField(
            hint_text="Buscar por nombre",
            border_color=_BORDER,
            focused_border_color=_ACCENT,
            text_style=ft.TextStyle(color=_TEXT),
            hint_style=ft.TextStyle(color=_MUTED),
            bgcolor=_CARD,
            content_padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            on_submit=lambda _e: self._on_search(),
            expand=True,
        )

    # ── Build principal ────────────────────────────────────────────────────────
    def build(self) -> ft.Control:
        self._load_agentes()
        sidebar = _app_sidebar(self._navigate, "/agentes")
        return ft.Container(
            content=ft.Row([sidebar, self._build_main()], spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    # ── Panel principal (topbar + body) ────────────────────────────────────────
    def _build_main(self) -> ft.Container:
        agente_actual = obtener_agente()
        rol_actual = str(getattr(agente_actual, "rol", "")).strip().lower()
        is_admin = rol_actual == "admin"

        topbar = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Gestion de Agentes", size=18, weight=ft.FontWeight.BOLD, color=_TEXT),
                    ft.Container(expand=True),
                    ft.FilledButton(
                        content=ft.Row(
                            [ft.Icon(ft.Icons.ADD_ROUNDED, size=16), ft.Text("Nuevo agente", size=13)],
                            spacing=6,
                        ),
                        style=ft.ButtonStyle(
                            bgcolor=_ACCENT,
                            color="#000000",
                            shape=ft.RoundedRectangleBorder(radius=8),
                        ),
                        disabled=not is_admin or self._modo == "desactivados",
                        on_click=lambda _e: self._open_create_modal(),
                    ),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=28, vertical=16),
            border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

        self._tabla.controls = self._build_rows(is_admin)
        self._btn_prev = ft.OutlinedButton("Anterior", disabled=True, on_click=lambda _e: self._go_prev_page())
        self._btn_next = ft.OutlinedButton("Siguiente", disabled=True, on_click=lambda _e: self._go_next_page())
        self._update_pagination_state()

        def _tab_activos(_e):
            self._switch_modo("activos")

        def _tab_desactivados(_e):
            self._switch_modo("desactivados")

        self._tab_activos_cont = ft.Container(
            content=ft.TextButton(
                "Agentes activos",
                on_click=_tab_activos,
                style=ft.ButtonStyle(
                    color={ft.ControlState.DEFAULT: _TEXT if self._modo == "activos" else _MUTED},
                    overlay_color=ft.Colors.TRANSPARENT,
                ),
            ),
            border=ft.Border.only(
                bottom=ft.BorderSide(3, _ACCENT if self._modo == "activos" else ft.Colors.TRANSPARENT)
            ),
        )
        self._tab_desact_cont = ft.Container(
            content=ft.TextButton(
                "Agentes desactivados",
                on_click=_tab_desactivados,
                style=ft.ButtonStyle(
                    color={ft.ControlState.DEFAULT: _TEXT if self._modo == "desactivados" else _MUTED},
                    overlay_color=ft.Colors.TRANSPARENT,
                ),
            ),
            border=ft.Border.only(
                bottom=ft.BorderSide(3, _ACCENT if self._modo == "desactivados" else ft.Colors.TRANSPARENT)
            ),
        )

        tabs_row = ft.Row(
            [self._tab_activos_cont, self._tab_desact_cont],
            spacing=0,
        )

        body = ft.Container(
            content=ft.Column(
                [
                    tabs_row,
                    ft.Container(height=6),
                    ft.Text(
                        "Solo administradores pueden crear, editar y desactivar agentes."
                        if is_admin
                        else "Tu usuario no tiene permisos para administrar agentes.",
                        size=12,
                        color=_MUTED,
                    ),
                    ft.Container(height=6),
                    ft.Row(
                        [
                            self._search_field,
                            ft.FilledButton(
                                "Buscar",
                                style=ft.ButtonStyle(
                                    bgcolor=_ACCENT,
                                    color="#000000",
                                    shape=ft.RoundedRectangleBorder(radius=8),
                                ),
                                on_click=lambda _e: self._on_search(),
                            ),
                            ft.TextButton(
                                "Limpiar",
                                on_click=lambda _e: self._on_clear_search(),
                            ),
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=8),
                    self._tabla,
                    ft.Container(height=10),
                    ft.Row(
                        [
                            self._page_info,
                            ft.Container(expand=True),
                            self._btn_prev,
                            self._btn_next,
                        ],
                        spacing=10,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                ],
                spacing=0,
                scroll=ft.ScrollMode.AUTO,
                expand=True,
            ),
            padding=ft.Padding.symmetric(horizontal=28, vertical=20),
            expand=True,
        )

        return ft.Container(
            content=ft.Column([topbar, body], spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    def _switch_modo(self, modo: str) -> None:
        self._modo = modo
        self._current_page = 1
        self._nombre_query = ""
        self._search_field.value = ""
        self._refresh()

    # ── Carga de agentes desde el backend ──────────────────────────────────────
    def _load_agentes(self) -> None:
        if self._modo == "desactivados":
            res = AgenteController.get_agentes_desactivados_page(
                page=self._current_page,
                page_size=self._page_size,
                nombre_query=self._nombre_query,
            )
        else:
            res = AgenteController.get_agentes_page(
                page=self._current_page,
                page_size=self._page_size,
                nombre_query=self._nombre_query,
            )
        if not res.get("ok"):
            self._agentes = []
            self._total_items = 0
            self._total_pages = 1
            return

        self._agentes = list(res.get("data", []))
        meta = res.get("meta", {})
        self._total_items = int(meta.get("total", 0) or 0)
        self._total_pages = max(1, int(meta.get("total_pages", 1) or 1))

        if self._current_page > self._total_pages:
            self._current_page = self._total_pages
            self._load_agentes()

    # ── Refresco de tabla y paginación ─────────────────────────────────────────
    def _refresh(self) -> None:
        agente_actual = obtener_agente()
        is_admin = str(getattr(agente_actual, "rol", "")).strip().lower() == "admin"
        self._load_agentes()
        self._tabla.controls = self._build_rows(is_admin)
        self._update_pagination_state()
        # update tab visual state if controls exist
        if hasattr(self, "_tab_activos_cont"):
            self._tab_activos_cont.border = ft.Border.only(
                bottom=ft.BorderSide(3, _ACCENT if self._modo == "activos" else ft.Colors.TRANSPARENT)
            )
            self._tab_activos_cont.content.style = ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: _TEXT if self._modo == "activos" else _MUTED},
                overlay_color=ft.Colors.TRANSPARENT,
            )
            self._tab_desact_cont.border = ft.Border.only(
                bottom=ft.BorderSide(3, _ACCENT if self._modo == "desactivados" else ft.Colors.TRANSPARENT)
            )
            self._tab_desact_cont.content.style = ft.ButtonStyle(
                color={ft.ControlState.DEFAULT: _TEXT if self._modo == "desactivados" else _MUTED},
                overlay_color=ft.Colors.TRANSPARENT,
            )
        self._page.update()

    # ── Actualización de controles de paginación ───────────────────────────────
    def _update_pagination_state(self) -> None:
        inicio = 0 if self._total_items == 0 else ((self._current_page - 1) * self._page_size) + 1
        fin = min(self._current_page * self._page_size, self._total_items)
        self._page_info.value = (
            f"Mostrando {inicio}-{fin} de {self._total_items} · "
            f"Pagina {self._current_page}/{self._total_pages}"
        )
        self._btn_prev.disabled = self._current_page <= 1
        self._btn_next.disabled = self._current_page >= self._total_pages

    def _on_search(self) -> None:
        self._nombre_query = (self._search_field.value or "").strip()
        self._current_page = 1
        self._refresh()

    def _on_clear_search(self) -> None:
        self._search_field.value = ""
        self._nombre_query = ""
        self._current_page = 1
        self._refresh()

    def _go_prev_page(self) -> None:
        if self._current_page <= 1:
            return
        self._current_page -= 1
        self._refresh()

    def _go_next_page(self) -> None:
        if self._current_page >= self._total_pages:
            return
        self._current_page += 1
        self._refresh()

    # ── Renderizado de filas de la tabla de agentes ────────────────────────────
    def _build_rows(self, is_admin: bool) -> list[ft.Control]:
        modo_desact = self._modo == "desactivados"
        if not self._agentes:
            msg = "No hay agentes desactivados." if modo_desact else "No hay agentes registrados."
            return [
                ft.Container(
                    content=ft.Text(msg, color=_MUTED, size=13),
                    padding=ft.Padding.all(16),
                    bgcolor=_CARD,
                    border=ft.Border.all(1, _BORDER),
                    border_radius=10,
                )
            ]

        header = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Clave", color=_MUTED, size=12, expand=2),
                    ft.Text("Nombre", color=_MUTED, size=12, expand=3),
                    ft.Text("Correo", color=_MUTED, size=12, expand=3),
                    ft.Text("Rol", color=_MUTED, size=12, expand=1),
                    ft.Text("", expand=1),
                ],
                spacing=8,
            ),
            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
        )

        rows: list[ft.Control] = [header]
        for agente in self._agentes:
            nombre = " ".join(
                [
                    getattr(agente, "nombre", "") or "",
                    getattr(agente, "apellido_paterno", "") or "",
                    getattr(agente, "apellido_materno", "") or "",
                ]
            ).strip()
            rows.append(
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Text(str(getattr(agente, "clave_agente", "")), color=_TEXT, size=13, expand=2),
                            ft.Text(nombre, color=_TEXT, size=13, expand=3),
                            ft.Text(str(getattr(agente, "correo", "")), color=_TEXT, size=13, expand=3),
                            ft.Text(str(getattr(agente, "rol", "")), color=_TEXT, size=13, expand=1),
                            ft.Row(
                                [
                                    ft.IconButton(
                                        icon=ft.Icons.RESTORE_ROUNDED,
                                        tooltip="Reactivar agente",
                                        icon_color=ft.Colors.GREEN_600,
                                        icon_size=16,
                                        disabled=not is_admin,
                                        on_click=lambda _e, a=agente: self._confirm_reactivate(a),
                                    ),
                                ] if modo_desact else [
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT_OUTLINED,
                                        tooltip="Editar",
                                        icon_color=_MUTED,
                                        icon_size=16,
                                        disabled=not is_admin,
                                        on_click=lambda _e, a=agente: self._open_edit_modal(a),
                                    ),
                                    ft.IconButton(
                                        icon=ft.Icons.BLOCK_ROUNDED,
                                        tooltip="Desactivar agente",
                                        icon_color=_ERROR,
                                        icon_size=16,
                                        disabled=not is_admin,
                                        on_click=lambda _e, a=agente: self._confirm_deactivate(a),
                                    ),
                                ],
                                spacing=0,
                                expand=1,
                                alignment=ft.MainAxisAlignment.END,
                            ),
                        ],
                        spacing=8,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    bgcolor=_CARD,
                    border=ft.Border.all(1, _BORDER),
                    border_radius=10,
                    padding=ft.Padding.symmetric(horizontal=14, vertical=10),
                )
            )
        return rows

    def _open_create_modal(self) -> None:
        self._open_form_modal(title="Nuevo agente")

    def _open_edit_modal(self, agente) -> None:
        self._open_form_modal(title="Editar agente", agente=agente)

    # ── Modal: formulario crear/editar agente ──────────────────────────────────
    def _open_form_modal(self, title: str, agente=None) -> None:
        tf_base = {
            "border_color": _BORDER,
            "focused_border_color": _ACCENT,
            "label_style": ft.TextStyle(color=_MUTED),
            "hint_style": ft.TextStyle(color=_MUTED),
            "text_style": ft.TextStyle(color=_TEXT),
            "bgcolor": _CARD,
            "expand": True,
        }
        dd_base = {
            "border_color": _BORDER,
            "focused_border_color": _ACCENT,
            "label_style": ft.TextStyle(color=_MUTED),
            "text_style": ft.TextStyle(color=_TEXT),
            "bgcolor": _CARD,
            "expand": True,
        }

        clave_f = ft.TextField(label="Clave", value=getattr(agente, "clave_agente", ""), **tf_base)
        cedula_f = ft.TextField(label="Cedula", value=getattr(agente, "cedula", ""), **tf_base)
        nombre_f = ft.TextField(label="Nombre", value=getattr(agente, "nombre", ""), **tf_base)
        ap_pat_f = ft.TextField(label="Apellido paterno", value=getattr(agente, "apellido_paterno", ""), **tf_base)
        ap_mat_f = ft.TextField(label="Apellido materno", value=getattr(agente, "apellido_materno", ""), **tf_base)
        correo_f = ft.TextField(label="Correo", value=getattr(agente, "correo", ""), **tf_base)
        tel_f = ft.TextField(label="Telefono", value=getattr(agente, "telefono", "") or "", **tf_base)
        rol_dd = ft.Dropdown(
            label="Rol",
            options=[ft.dropdown.Option("admin"), ft.dropdown.Option("agente")],
            value=getattr(agente, "rol", "agente"),
            **dd_base,
        )
        pass_f = ft.TextField(
            label="Password" if agente is None else "Password nueva (opcional)",
            password=True,
            can_reveal_password=True,
            **tf_base,
        )
        error_t = ft.Text("", color=_ERROR, size=12)

        if agente is not None:
            clave_f.disabled = True

        def _save(_event) -> None:
            payload = {
                "cedula": cedula_f.value.strip(),
                "nombre": nombre_f.value.strip(),
                "apellido_paterno": ap_pat_f.value.strip(),
                "apellido_materno": ap_mat_f.value.strip(),
                "correo": correo_f.value.strip(),
                "telefono": tel_f.value.strip(),
                "rol": rol_dd.value,
            }

            if agente is None:
                payload["clave_agente"] = clave_f.value.strip()
                payload["password"] = pass_f.value or ""
                res = AgenteController.create_agente(payload)
            else:
                if pass_f.value:
                    payload["password"] = pass_f.value
                res = AgenteController.update_agente(agente.id_agente, payload)

            if not res.get("ok"):
                error_t.value = str(res.get("error") or "No fue posible guardar el agente.")
                self._page.update()
                return

            self._page.pop_dialog()
            self._refresh()

        content = ft.Container(
            width=760,
            content=ft.Column(
                [
                    ft.ResponsiveRow(
                        [
                            ft.Container(content=clave_f, col={"xs": 12, "md": 6}),
                            ft.Container(content=cedula_f, col={"xs": 12, "md": 6}),
                        ],
                        spacing=10,
                        run_spacing=10,
                    ),
                    ft.ResponsiveRow(
                        [
                            ft.Container(content=nombre_f, col={"xs": 12, "md": 4}),
                            ft.Container(content=ap_pat_f, col={"xs": 12, "md": 4}),
                            ft.Container(content=ap_mat_f, col={"xs": 12, "md": 4}),
                        ],
                        spacing=10,
                        run_spacing=10,
                    ),
                    ft.ResponsiveRow(
                        [
                            ft.Container(content=correo_f, col={"xs": 12, "md": 6}),
                            ft.Container(content=tel_f, col={"xs": 12, "md": 6}),
                        ],
                        spacing=10,
                        run_spacing=10,
                    ),
                    ft.ResponsiveRow(
                        [
                            ft.Container(content=rol_dd, col={"xs": 12, "md": 4}),
                            ft.Container(content=pass_f, col={"xs": 12, "md": 8}),
                        ],
                        spacing=10,
                        run_spacing=10,
                    ),
                    error_t,
                ],
                spacing=10,
                tight=True,
                scroll=ft.ScrollMode.AUTO,
            ),
        )

        dialog = _modal_dialog(
            title,
            content,
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _e: self._close_dialog()),
                ft.FilledButton("Guardar", on_click=_save),
            ],
            width=760,
        )
        self._page.show_dialog(dialog)

    # ── Modal: confirmar desactivación de agente ───────────────────────────────
    def _confirm_deactivate(self, agente) -> None:
        def _deactivate(_event) -> None:
            res = AgenteController.delete_agente(agente.id_agente)
            if not res.get("ok"):
                self._page.snack_bar = ft.SnackBar(
                    ft.Text(str(res.get("error") or "No fue posible desactivar."), color="#ffffff"),
                    bgcolor=_ERROR,
                )
                self._page.snack_bar.open = True
                self._page.update()
                return
            self._page.pop_dialog()
            self._refresh()

        dialog = _modal_dialog(
            "Desactivar agente",
            ft.Text(
                f"Se desactivara el agente {getattr(agente, 'clave_agente', '')}. Solo podras hacerlo si no tiene polizas asignadas.",
                color=_TEXT,
                size=13,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _e: self._close_dialog()),
                ft.FilledButton(
                    "Desactivar",
                    style=ft.ButtonStyle(bgcolor=_ERROR, color="#ffffff"),
                    on_click=_deactivate,
                ),
            ],
            width=460,
        )
        self._page.show_dialog(dialog)

    # ── Modal: confirmar reactivación de agente ────────────────────────────────
    def _confirm_reactivate(self, agente) -> None:
        def _reactivate(_event) -> None:
            res = AgenteController.reactivate_agente(agente.id_agente)
            if not res.get("ok"):
                self._page.snack_bar = ft.SnackBar(
                    ft.Text(str(res.get("error") or "No fue posible reactivar."), color="#ffffff"),
                    bgcolor=_ERROR,
                )
                self._page.snack_bar.open = True
                self._page.update()
                return
            self._page.pop_dialog()
            self._refresh()

        dialog = _modal_dialog(
            "Reactivar agente",
            ft.Text(
                f"Se reactivara el agente {getattr(agente, 'clave_agente', '')}. Volvera a aparecer en la lista de agentes activos.",
                color=_TEXT,
                size=13,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda _e: self._close_dialog()),
                ft.FilledButton(
                    "Reactivar",
                    style=ft.ButtonStyle(bgcolor=ft.Colors.GREEN_600, color="#ffffff"),
                    on_click=_reactivate,
                ),
            ],
            width=460,
        )
        self._page.show_dialog(dialog)

    def _close_dialog(self) -> None:
        self._page.pop_dialog()
