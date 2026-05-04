"""Piezas visuales reutilizables para la vista de asignaciones."""

from __future__ import annotations

import flet as ft

from views.theme import ACCENT, BORDER, CARD, CARD_ALT, MUTED, TEXT
from views.ui_controls import styled_dropdown, styled_text_field


def assignment_field(
    label: str,
    value: str = "",
    hint: str = "",
    keyboard_type: ft.KeyboardType = ft.KeyboardType.TEXT,
    multiline: bool = False,
    min_lines: int | None = None,
    max_lines: int | None = None,
    expand: int | None = None,
) -> ft.TextField:
    kwargs = {
        "hint_text": hint,
        "keyboard_type": keyboard_type,
        "multiline": multiline,
        "min_lines": min_lines,
        "max_lines": max_lines,
    }
    if expand is not None:
        kwargs["expand"] = expand
    return styled_text_field(label=label, value=value, **kwargs)


def assignment_dropdown(
    label: str,
    options: list[ft.dropdown.Option],
    value: str | None = None,
) -> ft.Dropdown:
    return styled_dropdown(label=label, value=value, options=options)


def section_card(title: str, body: list[ft.Control]) -> ft.Container:
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(title, size=16, weight=ft.FontWeight.W_600, color=TEXT),
                ft.Divider(color=BORDER, height=12),
                *body,
            ],
            spacing=12,
        ),
        padding=20,
        bgcolor=CARD,
        border_radius=12,
        border=ft.Border.all(1, BORDER),
    )


def panel_card(title: str, body: list[ft.Control], col: int | dict | None = None) -> ft.Container:
    kwargs = {}
    if col is not None:
        kwargs["col"] = col
    return ft.Container(
        content=ft.Column(
            [
                ft.Text(title, size=14, weight=ft.FontWeight.W_600, color=TEXT),
                *body,
            ],
            spacing=12,
        ),
        padding=16,
        bgcolor=CARD_ALT,
        border_radius=12,
        border=ft.Border.all(1, BORDER),
        **kwargs,
    )


def info_note(message: str) -> ft.Container:
    return ft.Container(
        content=ft.Text(message, size=12, color=MUTED),
        padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        bgcolor=ft.Colors.with_opacity(0.08, ACCENT),
        border_radius=10,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.15, ACCENT)),
    )