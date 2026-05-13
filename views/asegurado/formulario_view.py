"""Formulario para registrar o editar un asegurado."""

from __future__ import annotations

import flet as ft
from controllers.asegurado_controller import AseguradoController
from controllers.poliza_controller import PolizaController
from views.theme import (
    ACCENT as _ACCENT,
    BG as _BG,
    BORDER as _BORDER,
    CARD as _CARD,
    ERROR as _ERROR,
    MUTED as _MUTED,
    TEXT as _TEXT,
)
from views.ui_controls import app_sidebar, modal_dialog, styled_dropdown as _dropdown, styled_text_field as _field


class FormularioAseguradoView:
    # ── Constructor ────────────────────────────────────────────────────────────
    def __init__(self, page: ft.Page, navigate, asegurado=None) -> None:
        self._page = page
        self._navigate = navigate
        self._asegurado = asegurado
        self._editing = asegurado is not None
        self._errors: dict[str, ft.Text] = {}

    # ── Build del layout con sidebar ───────────────────────────────────────────
    def build(self) -> ft.Control:
        from services.session_manager import obtener_agente
        agente = obtener_agente()
        nombre_agente = f"{agente.nombre} {agente.apellido_paterno}" if agente else "Agente"
        sidebar = app_sidebar(self._navigate, "/clientes")
        main = self._build_form()
        return ft.Container(
            content=ft.Row([sidebar, main], spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    # ── Helpers de validación visual ───────────────────────────────────────────
    def _err(self, key: str) -> ft.Text:
        t = ft.Text("", color=_ERROR, size=11, visible=False)
        self._errors[key] = t
        return t

    def _set_err(self, key: str, msg: str) -> None:
        t = self._errors.get(key)
        if t:
            t.value = msg
            t.visible = bool(msg)

    def _clear_errors(self) -> None:
        for t in self._errors.values():
            t.value = ""
            t.visible = False

    # ── Opciones post-guardado (nuevo asegurado) ───────────────────────────────
    def _show_post_save_options(self, id_asegurado: int) -> None:
        def _go_asignaciones(e):
            self._page.pop_dialog()
            self._navigate("/asegurado/asignaciones", id_asegurado=id_asegurado)

        dlg = modal_dialog(
            "Siguiente paso recomendado",
            ft.Column(
                [
                    ft.Text(
                        "El asegurado ya quedó registrado. Continúa en Asignaciones para seguir el orden pólizas, luego beneficiarios y por último beneficios.",
                        size=13,
                        color=_MUTED,
                    ),
                ],
                tight=True,
                spacing=10,
            ),
            [
                ft.TextButton(
                    "Volver a clientes",
                    style=ft.ButtonStyle(color=_MUTED),
                    on_click=lambda e: (
                        self._page.pop_dialog(),
                        self._navigate("/clientes"),
                    ),
                ),
                ft.FilledButton(
                    "Ir a Asignaciones",
                    style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"),
                    on_click=_go_asignaciones,
                ),
            ],
            width=420,
        )
        self._page.show_dialog(dlg)

    # ── Modal: vincular a póliza existente ─────────────────────────────────────
    def _open_link_to_existing_poliza_modal(self, id_asegurado: int) -> None:
        result = PolizaController.get_available_polizas_for_participante(id_asegurado)
        if not result["ok"]:
            self._show_post_save_options(id_asegurado)
            return

        polizas = result.get("data", [])
        if not polizas:
            dlg_empty = modal_dialog(
                "Sin pólizas disponibles",
                ft.Text(
                    "No hay pólizas activas disponibles para vincular. Puedes crear una nueva póliza desde la pantalla de asignaciones del asegurado.",
                    color=_MUTED,
                    size=12,
                ),
                [
                    ft.TextButton(
                        "Cerrar",
                        style=ft.ButtonStyle(color=_MUTED),
                        on_click=lambda e: (
                            self._page.pop_dialog(),
                            self._show_post_save_options(id_asegurado),
                        ),
                    ),
                    ft.FilledButton(
                        "Ir a asignaciones",
                        style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"),
                        on_click=lambda e: (
                            self._page.pop_dialog(),
                            self._navigate("/asegurado/asignaciones", id_asegurado=id_asegurado),
                        ),
                    ),
                ],
            )
            self._page.show_dialog(dlg_empty)
            return

        poliza_dd = _dropdown(
            label="Póliza activa",
            options=[
                ft.dropdown.Option(
                    key=str(p.id_poliza),
                    text=f"{p.numero_poliza}",
                )
                for p in polizas
            ],
        )
        tipo_dd = _dropdown(
            label="Tipo de participante",
            value="dependiente",
            options=[
                ft.dropdown.Option(key="conyuge", text="Cónyuge"),
                ft.dropdown.Option(key="hijo", text="Hijo"),
                ft.dropdown.Option(key="dependiente", text="Dependiente"),
            ],
        )
        err_t = ft.Text("", color=_ERROR, size=12)

        def _save_link(e):
            if not poliza_dd.value:
                err_t.value = "Selecciona una póliza para continuar."
                self._page.update()
                return

            link_res = PolizaController.add_participante_to_poliza(
                {
                    "id_poliza": int(poliza_dd.value),
                    "id_asegurado": id_asegurado,
                    "tipo_participante": tipo_dd.value or "dependiente",
                }
            )
            if not link_res["ok"]:
                err_t.value = link_res.get("error", "No fue posible vincular al asegurado.")
                self._page.update()
                return

            self._page.pop_dialog()
            self._navigate("/asegurado/asignaciones", id_asegurado=id_asegurado)

        dlg = modal_dialog(
            "Vincular a póliza existente",
            ft.Column(
                [poliza_dd, tipo_dd, err_t],
                spacing=12,
                tight=True,
            ),
            [
                ft.TextButton(
                    "Atrás",
                    style=ft.ButtonStyle(color=_MUTED),
                    on_click=lambda e: (
                        self._page.pop_dialog(),
                        self._show_post_save_options(id_asegurado),
                    ),
                ),
                ft.FilledButton(
                    "Vincular",
                    style=ft.ButtonStyle(bgcolor=_ACCENT, color="#000000"),
                    on_click=_save_link,
                ),
            ],
            width=420,
        )
        self._page.show_dialog(dlg)

    # ── Formulario principal (datos personales + dirección) ──────────────────────
    def _build_form(self) -> ft.Container:
        a = self._asegurado
        title = "Editar asegurado" if self._editing else "Nuevo asegurado"

        # ── Campos personales
        nombre_f = _field("Nombre *", a.nombre if a else "")
        ap_f = _field("Apellido paterno *", a.apellido_paterno if a else "")
        am_f = _field("Apellido materno *", a.apellido_materno if a else "")
        rfc_f = _field("RFC *", a.rfc if a else "", hint="Ej. GOME850412H19",
                       max_length=13)
        correo_f = _field("Correo electrónico", a.correo or "" if a else "",
                          hint="usuario@correo.com",
                          keyboard_type=ft.KeyboardType.EMAIL)
        celular_f = _field("Celular (10 dígitos)", a.celular or "" if a else "",
                           hint="5512345678",
                           keyboard_type=ft.KeyboardType.PHONE,
                           max_length=10)

        # ── Dirección
        calle_f = _field("Calle *", a.calle if a else "")
        num_ext_f = _field("Número exterior *", a.numero_exterior if a else "")
        num_int_f = _field("Número interior", a.numero_interior or "" if a else "")
        colonia_f = _field("Colonia *", a.colonia if a else "")
        municipio_f = _field("Municipio *", a.municipio if a else "")
        estado_f = _field("Estado *", a.estado if a else "")
        cp_f = _field("Código postal *", a.codigo_postal if a else "",
                      keyboard_type=ft.KeyboardType.NUMBER)

        global_err = ft.Text("", color=_ERROR, size=13)

        def section_card(titulo: str, controls: list) -> ft.Container:
            return ft.Container(
                content=ft.Column(
                    [
                        ft.Text(titulo, size=15, weight=ft.FontWeight.W_600, color=_TEXT),
                        ft.Divider(color=_BORDER, height=12),
                        *controls,
                    ],
                    spacing=12,
                ),
                padding=20,
                bgcolor=_CARD,
                border_radius=12,
                border=ft.Border.all(1, _BORDER),
            )

        info_card = section_card(
            "Información Personal",
            [
                ft.Row([nombre_f, ap_f, am_f], spacing=12),
                ft.Row(
                    [self._err("nombre"), self._err("apellido_paterno"),
                     self._err("apellido_materno")],
                    spacing=12,
                ),
                ft.Row([rfc_f, correo_f, celular_f], spacing=12),
                ft.Row(
                    [self._err("rfc"), self._err("correo"), self._err("celular")],
                    spacing=12,
                ),
            ],
        )

        dir_card = section_card(
            "Dirección",
            [
                ft.Row([calle_f, num_ext_f, num_int_f], spacing=12),
                ft.Row([colonia_f, municipio_f], spacing=12),
                ft.Row([estado_f, cp_f], spacing=12),
                ft.Row(
                    [self._err("calle"), self._err("numero_exterior"),
                     self._err("colonia"), self._err("municipio"),
                     self._err("estado"), self._err("codigo_postal")],
                    spacing=8, wrap=True,
                ),
            ],
        )

        def on_guardar(e):
            self._clear_errors()
            global_err.value = ""
            import re as _re
            rfc_val = rfc_f.value.strip().upper()
            if not _re.fullmatch(r"[A-ZÑ&]{3,4}\d{6}[A-Z0-9]{3}", rfc_val):
                self._set_err("rfc", "El RFC no tiene un formato válido (ej. GOME850412H19).")
                self._page.update()
                return
            data = {
                "nombre": nombre_f.value.strip(),
                "apellido_paterno": ap_f.value.strip(),
                "apellido_materno": am_f.value.strip(),
                "rfc": rfc_val,
                "correo": correo_f.value.strip() or None,
                "celular": celular_f.value.strip() or None,
                "calle": calle_f.value.strip(),
                "numero_exterior": num_ext_f.value.strip(),
                "numero_interior": num_int_f.value.strip() or None,
                "colonia": colonia_f.value.strip(),
                "municipio": municipio_f.value.strip(),
                "estado": estado_f.value.strip(),
                "codigo_postal": cp_f.value.strip(),
            }
            from services.session_manager import obtener_agente
            ag = obtener_agente()
            if ag:
                data["id_agente_responsable"] = ag.id_agente

            if self._editing:
                result = AseguradoController.update_asegurado(
                    self._asegurado.id_asegurado, data)
            else:
                result = AseguradoController.create_asegurado(data)

            if result["ok"]:
                if self._editing:
                    self._navigate(
                        "/asegurado/detalle",
                        id_asegurado=result["data"].id_asegurado,
                    )
                else:
                    self._show_post_save_options(result["data"].id_asegurado)
            else:
                err = result["error"]
                # Map field-level errors
                campo_map = {
                    "'nombre'": "nombre",
                    "'apellido_paterno'": "apellido_paterno",
                    "'apellido_materno'": "apellido_materno",
                    "'rfc'": "rfc", "RFC": "rfc",
                    "'correo'": "correo", "correo": "correo",
                    "'calle'": "calle",
                    "'numero_exterior'": "numero_exterior",
                    "'colonia'": "colonia",
                    "'municipio'": "municipio",
                    "'estado'": "estado",
                    "'codigo_postal'": "codigo_postal",
                }
                mapped = False
                for key, campo in campo_map.items():
                    if key in err:
                        self._set_err(campo, err)
                        mapped = True
                        break
                if not mapped:
                    global_err.value = err
                self._page.update()

        btn_guardar = ft.Button(
            content=ft.Text("Guardar asegurado" if not self._editing else "Actualizar", size=14),
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: _ACCENT},
                color={ft.ControlState.DEFAULT: "#000000"},
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding.symmetric(horizontal=24, vertical=12),
            ),
            on_click=on_guardar,
        )
        btn_cancelar = ft.OutlinedButton(
            content=ft.Text("Cancelar", size=14, color=_MUTED),
            style=ft.ButtonStyle(
                color=_MUTED,
                side={ft.ControlState.DEFAULT: ft.BorderSide(1, _BORDER)},
                shape=ft.RoundedRectangleBorder(radius=8),
                padding=ft.Padding.symmetric(horizontal=24, vertical=12),
            ),
            on_click=lambda e: (
                self._navigate("/asegurado/detalle",
                               id_asegurado=self._asegurado.id_asegurado)
                if self._editing else self._navigate("/clientes")
            ),
        )

        topbar = ft.Container(
            content=ft.Row(
                [
                    ft.TextButton(
                        "← Asegurados" if not self._editing else "← Detalle",
                        style=ft.ButtonStyle(color=_MUTED),
                        on_click=lambda e: (
                            self._navigate("/asegurado/detalle",
                                           id_asegurado=self._asegurado.id_asegurado)
                            if self._editing else self._navigate("/clientes")
                        ),
                    ),
                    ft.Text(title, size=20, weight=ft.FontWeight.BOLD, color=_TEXT),
                ],
                spacing=16,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=28, vertical=20),
            border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

        return ft.Container(
            content=ft.Column(
                [
                    topbar,
                    ft.Container(
                        content=ft.Column(
                            [
                                info_card,
                                dir_card,
                                global_err,
                                ft.Row(
                                    [btn_cancelar, btn_guardar],
                                    spacing=12,
                                ),
                            ],
                            spacing=16,
                            scroll=ft.ScrollMode.AUTO,
                        ),
                        padding=ft.Padding.symmetric(horizontal=28, vertical=20),
                        expand=True,
                    ),
                ],
                spacing=0,
                expand=True,
            ),
            expand=True,
            bgcolor=_BG,
        )

