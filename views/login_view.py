"""Vista de login."""

import flet as ft
from controllers.auth_controller import AuthController
from services.session_manager import guardar_sesion

# Paleta de colores
_BG = "#0F1117"
_CARD = "#1A1D27"
_ACCENT = "#00C17C"
_TEXT = "#E8EAF0"
_MUTED = "#6B7280"
_ERROR = "#EF4444"
_BORDER = "#2D3148"


class LoginView:
    def __init__(self, page: ft.Page, navigate) -> None:
        self._page = page
        self._navigate = navigate

    def build(self) -> ft.Control:
        clave_field = ft.TextField(
            label="CLAVE DE AGENTE",
            hint_text="ID-000000",
            autofocus=True,
            width=340,
            border_color=_BORDER,
            focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED, size=11, weight=ft.FontWeight.W_600),
            hint_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT),
            bgcolor=_CARD,
            cursor_color=_ACCENT,
            prefix_icon=ft.Icons.BADGE_OUTLINED,
            on_submit=lambda e: password_field.focus(),
        )

        password_field = ft.TextField(
            label="CONTRASEÑA",
            hint_text="••••••••",
            width=340,
            password=True,
            can_reveal_password=True,
            border_color=_BORDER,
            focused_border_color=_ACCENT,
            label_style=ft.TextStyle(color=_MUTED, size=11, weight=ft.FontWeight.W_600),
            hint_style=ft.TextStyle(color=_MUTED),
            text_style=ft.TextStyle(color=_TEXT),
            bgcolor=_CARD,
            cursor_color=_ACCENT,
            prefix_icon=ft.Icons.LOCK_OUTLINE_ROUNDED,
            on_submit=lambda e: self._handle_login(clave_field, password_field, error_text, btn_login),
        )

        error_text = ft.Text(
            "",
            color=_ERROR,
            size=12,
            visible=False,
        )

        btn_login = ft.ElevatedButton(
            content=ft.Row(
                [
                    ft.Text("Entrar", size=14, weight=ft.FontWeight.W_600,
                            color="#000000"),
                    ft.Icon(ft.Icons.ARROW_FORWARD_ROUNDED, size=16, color="#000000"),
                ],
                spacing=8,
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            width=340,
            height=46,
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: _ACCENT,
                         ft.ControlState.HOVERED: "#00A86B"},
                shape=ft.RoundedRectangleBorder(radius=8),
                elevation={"pressed": 0, "": 2},
            ),
            on_click=lambda e: self._handle_login(clave_field, password_field, error_text, btn_login),
        )

        # Logo + brand header
        logo = ft.Container(
            content=ft.Icon(ft.Icons.ACCOUNT_BALANCE_ROUNDED, size=28, color=_TEXT),
            width=56,
            height=56,
            bgcolor="#1E2235",
            border_radius=12,
            border=ft.border.all(1, _BORDER),
            alignment=ft.Alignment.CENTER,
        )

        card = ft.Container(
            content=ft.Column(
                controls=[
                    # Branding
                    ft.Column(
                        [
                            logo,
                            ft.Text("The Architectural Trust", size=16,
                                    weight=ft.FontWeight.BOLD, color=_TEXT),
                            ft.Text("Insurance Portal", size=12, color=_ACCENT),
                        ],
                        spacing=6,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Divider(height=28, color=ft.Colors.TRANSPARENT),
                    # Heading
                    ft.Text("Portal de Acceso", size=22,
                            weight=ft.FontWeight.BOLD, color=_TEXT),
                    ft.Container(height=4),
                    # Fields
                    clave_field,
                    password_field,
                    # Error
                    error_text,
                    ft.Container(height=4),
                    btn_login,
                    ft.Container(height=8),
                    ft.Text(
                        "© 2024 The Architectural Trust. Systems Security Protocol Enabled.",
                        size=10,
                        color=_MUTED,
                        text_align=ft.TextAlign.CENTER,
                    ),
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            width=440,
            padding=ft.padding.symmetric(horizontal=44, vertical=44),
            border_radius=18,
            bgcolor=_CARD,
            border=ft.border.all(1, _BORDER),
        )

        return ft.Container(
            content=card,
            expand=True,
            bgcolor=_BG,
            alignment=ft.Alignment.CENTER,
        )

    def _handle_login(
        self,
        clave_field: ft.TextField,
        password_field: ft.TextField,
        error_text: ft.Text,
        btn: ft.ElevatedButton,
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
            password_field.focus()
            self._page.update()

