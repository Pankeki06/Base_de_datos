"""Shared styled controls for Flet views."""

from __future__ import annotations

import flet as ft

from views.theme import ACCENT, BORDER, CARD, CARD_ALT, MUTED, SIDEBAR, TEXT


def styled_text_field(
    label: str,
    value: str = "",
    hint: str | None = None,
    **kwargs,
) -> ft.TextField:
    if hint is not None and "hint_text" not in kwargs:
        kwargs["hint_text"] = hint
    kwargs.setdefault("border_color", BORDER)
    kwargs.setdefault("focused_border_color", ACCENT)
    kwargs.setdefault("label_style", ft.TextStyle(color=MUTED))
    kwargs.setdefault("text_style", ft.TextStyle(color=TEXT))
    kwargs.setdefault("hint_style", ft.TextStyle(color=MUTED))
    kwargs.setdefault("bgcolor", CARD)
    kwargs.setdefault("cursor_color", ACCENT)
    return ft.TextField(label=label, value=value, **kwargs)


def styled_dropdown(
    label: str,
    options: list[ft.dropdown.Option],
    value: str | None = None,
    **kwargs,
) -> ft.Dropdown:
    kwargs.setdefault("border_color", BORDER)
    kwargs.setdefault("focused_border_color", ACCENT)
    kwargs.setdefault("label_style", ft.TextStyle(color=MUTED))
    kwargs.setdefault("text_style", ft.TextStyle(color=TEXT))
    kwargs.setdefault("hint_style", ft.TextStyle(color=MUTED))
    kwargs.setdefault("bgcolor", CARD)
    return ft.Dropdown(label=label, value=value, options=options, **kwargs)


def pill(label: str, color: str, bg: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(label, size=11, color=color, weight=ft.FontWeight.W_500),
        bgcolor=bg,
        padding=ft.Padding.symmetric(horizontal=8, vertical=3),
        border_radius=20,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.25, color)),
    )


def app_sidebar(navigate, ruta_activa: str = "/dashboard") -> ft.Container:
    from services.session_manager import cerrar_sesion, obtener_agente

    agente_actual = obtener_agente()
    is_admin = str(getattr(agente_actual, "rol", "")).strip().lower() == "admin"

    def _on_logout(_event) -> None:
        cerrar_sesion()
        navigate("/login")

    def _nav_button(icon, ruta: str, tooltip_text: str) -> ft.Container:
        activo = ruta_activa == ruta
        return ft.Container(
            content=ft.Icon(icon, size=20, color=TEXT if activo else MUTED),
            width=48,
            height=48,
            border_radius=10,
            bgcolor=CARD_ALT if activo else ft.Colors.TRANSPARENT,
            tooltip=tooltip_text,
            alignment=ft.Alignment.CENTER,
            on_click=lambda _event, target=ruta: navigate(target),
        )

    return ft.Container(
        content=ft.Column(
            [
                ft.Container(height=16),
                ft.Container(
                    content=ft.Icon(ft.Icons.GRID_VIEW_ROUNDED, size=22, color=ACCENT if ruta_activa == "/dashboard" else MUTED),
                    width=48,
                    height=48,
                    border_radius=10,
                    bgcolor=ft.Colors.with_opacity(0.15, ACCENT) if ruta_activa == "/dashboard" else ft.Colors.TRANSPARENT,
                    alignment=ft.Alignment.CENTER,
                    tooltip="Inicio",
                    on_click=lambda _event: navigate("/dashboard"),
                ),
                ft.Container(height=4),
                _nav_button(ft.Icons.PERSON_OUTLINE_ROUNDED, "/clientes", "Clientes"),
                _nav_button(ft.Icons.MENU_ROUNDED, "/polizas", "Pólizas"),
                *([
                    _nav_button(ft.Icons.ADMIN_PANEL_SETTINGS_ROUNDED, "/agentes", "Agentes")
                ] if is_admin else []),
                ft.Container(expand=True),
                ft.Container(
                    content=ft.Icon(ft.Icons.LOGOUT_ROUNDED, size=18, color=MUTED),
                    width=48,
                    height=48,
                    border_radius=10,
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
        bgcolor=SIDEBAR,
        border=ft.Border.only(right=ft.BorderSide(1, BORDER)),
    )


def modal_dialog(
    title: str,
    content: ft.Control,
    actions: list[ft.Control],
    *,
    title_color: str = TEXT,
    width: float | None = None,
) -> ft.AlertDialog:
    content_control = content
    if width is not None:
        if hasattr(content, "width"):
            content.width = width
        else:
            content_control = ft.Container(content=content, width=width)
    return ft.AlertDialog(
        modal=True,
        title=ft.Text(title, color=title_color),
        bgcolor=CARD,
        content=content_control,
        actions=actions,
        actions_alignment=ft.MainAxisAlignment.END,
    )


def empty_state(
    icon,
    title: str,
    message: str,
    *,
    icon_color: str = MUTED,
    title_color: str = TEXT,
    message_color: str = MUTED,
    action: ft.Control | None = None,
    visible: bool = False,
) -> ft.Container:
    controls: list[ft.Control] = [
        ft.Icon(icon, size=48, color=icon_color),
        ft.Container(height=12),
        ft.Text(
            title,
            size=16,
            color=title_color,
            weight=ft.FontWeight.W_600,
            text_align=ft.TextAlign.CENTER,
        ),
        ft.Text(
            message,
            size=13,
            color=message_color,
            text_align=ft.TextAlign.CENTER,
        ),
    ]
    if action is not None:
        controls.extend([ft.Container(height=16), action])
    return ft.Container(
        content=ft.Column(
            controls,
            spacing=6,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        expand=True,
        alignment=ft.Alignment.CENTER,
        visible=visible,
    )
