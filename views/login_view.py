"""Vista de login."""

import inspect

import flet as ft
from controllers.auth_controller import AuthController
from services.session_manager import guardar_sesion
from views.theme import (
    ACCENT as _ACCENT,
    ACCENT_HOVER as _ACCENT_HOVER,
    BG as _BG,
    BORDER as _BORDER,
    CARD as _CARD,
    ERROR as _ERROR,
    MUTED as _MUTED,
    TEXT as _TEXT,
)
from views.ui_controls import styled_text_field


class LoginView:
    def __init__(self, page: ft.Page, navigate) -> None:
        self._page = page
        self._navigate = navigate

    def _focus_control(self, control: ft.Control) -> None:
        if inspect.iscoroutinefunction(control.focus):
            run_task = getattr(self._page, "run_task", None)
            if callable(run_task):
                run_task(control.focus)
            return
        control.focus()

    def build(self) -> ft.Control:
        clave_field = styled_text_field(
            label="IDENTIFICADOR",
            hint_text="Ingresa tu identificador",
            autofocus=True,
            width=300,
            label_style=ft.TextStyle(color=_MUTED, size=11, weight=ft.FontWeight.W_600),
            hint_style=ft.TextStyle(color=_MUTED),
            on_submit=lambda e: self._focus_control(password_field),
        )

        password_field = styled_text_field(
            label="CONTRASEÑA",
            hint_text="Ingresa tu contrasena",
            width=300,
            password=True,
            can_reveal_password=True,
            label_style=ft.TextStyle(color=_MUTED, size=11, weight=ft.FontWeight.W_600),
            hint_style=ft.TextStyle(color=_MUTED),
            on_submit=lambda e: self._handle_login(clave_field, password_field, error_text, btn_login),
        )

        error_text = ft.Text(
            "",
            color=_ERROR,
            size=12,
            visible=False,
        )

        btn_login = ft.Button(
            content=ft.Row(
                [
                    ft.Text("Iniciar sesion", size=14, weight=ft.FontWeight.W_600,
                            color=_TEXT),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=300,
            height=44,
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: _ACCENT,
                         ft.ControlState.HOVERED: _ACCENT_HOVER},
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation={"pressed": 0, "": 2},
            ),
            on_click=lambda e: self._handle_login(clave_field, password_field, error_text, btn_login),
        )

        card = ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Icon(ft.Icons.LOGIN_ROUNDED, size=24, color="#F8FBF8"),
                        width=52,
                        height=52,
                        bgcolor=_TEXT,
                        border_radius=26,
                        border=ft.Border.all(1, ft.Colors.with_opacity(0.35, _ACCENT_HOVER)),
                        alignment=ft.Alignment.CENTER,
                    ),
                    ft.Text("Iniciar sesion", size=20, weight=ft.FontWeight.W_600, color=_TEXT),
                    clave_field,
                    password_field,
                    error_text,
                    btn_login,
                ],
                spacing=12,
                alignment=ft.MainAxisAlignment.CENTER,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=380,
            height=360,
            padding=ft.Padding.symmetric(horizontal=28, vertical=24),
            border_radius=14,
            bgcolor=_CARD,
            border=ft.Border.all(1, _BORDER),
        )

        return ft.Container(
            content=card,
            expand=True,
            alignment=ft.Alignment.CENTER,
            bgcolor=_BG,
            padding=ft.Padding.symmetric(horizontal=24, vertical=24),
        )

    def _handle_login(
        self,
        clave_field: ft.TextField,
        password_field: ft.TextField,
        error_text: ft.Text,
        btn: ft.Button,
    ) -> None:
        btn.disabled = True
        error_text.visible = False
        self._page.update()
        try:
            result = AuthController.login(
                clave_field.value or "",
                password_field.value or "",
            )
        except Exception as exc:
            result = {"ok": False, "error": str(exc)}
        finally:
            btn.disabled = False

        if result["ok"]:
            guardar_sesion(result["data"])
            self._navigate("/dashboard")
        else:
            msg = result["error"]
            if "cryptography" in msg or "caching_sha2" in msg or "sha256_password" in msg:
                msg = "Error de conexión con la base de datos. Contacte al administrador."
            error_text.value = msg
            error_text.visible = True
            password_field.value = ""
            self._focus_control(password_field)
            self._page.update()


def create_login_view(page: ft.Page, login_callback):
    """Compatibilidad para pruebas UI legacy."""
    validation_text = ft.Text("")
    clave_field = ft.TextField(label="Clave de agente")
    password_field = ft.TextField(label="Contraseña", password=True)

    def _on_click(_):
        login_callback(
            clave_field.value or "",
            password_field.value or "",
            validation_text,
            page,
        )

    login_button = ft.Button("Entrar", on_click=_on_click)
    return ft.Column(
        controls=[
            clave_field,
            password_field,
            login_button,
            validation_text,
        ]
    )

