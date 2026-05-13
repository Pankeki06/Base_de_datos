"""Vista de lista de asegurados (optimizada con paginación real y carga batch)."""

from __future__ import annotations

import flet as ft
from controllers.asegurado_controller import AseguradoController
from controllers.poliza_controller import PolizaController
from services.session_manager import obtener_agente
from views.theme import (
    ACCENT as _ACCENT,
    ACCENT_HOVER as _ACCENT_HOVER,
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
from views.ui_controls import empty_state as _empty_state_view, pill as _pill_global

# ── Constantes de configuración de la vista ───────────────────────────────
PAGE_SIZE = 10  # Número de asegurados por página (reducido para mejor rendimiento)


def _status_badge(polizas: list, participaciones: list | None = None) -> ft.Container:
    """Returns a colored badge for the most recent policy status."""
    if not polizas:
        tiene_derivada = any(
            p.get("tipo_participante") != "titular"
            for p in (participaciones or [])
        )
        if tiene_derivada:
            label, color, bg = "Cobertura derivada", _BLUE, ft.Colors.with_opacity(0.12, _BLUE)
        else:
            label, color, bg = "Sin póliza", _MUTED, ft.Colors.with_opacity(0.12, _MUTED)
    else:
        latest = max(polizas, key=lambda p: p.fecha_vencimiento)
        if latest.estatus == "activa":
            label, color, bg = "Activa", _ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)
        elif latest.estatus == "vencida":
            label, color, bg = "Vencida", _ERROR, ft.Colors.with_opacity(0.12, _ERROR)
        else:
            label = latest.estatus.capitalize()
            label, color, bg = label, _WARN, ft.Colors.with_opacity(0.12, _WARN)
    return ft.Container(
        content=ft.Text(label, size=11, color=color, weight=ft.FontWeight.W_500),
        bgcolor=bg,
        padding=ft.Padding.symmetric(horizontal=10, vertical=4),
        border_radius=20,
        border=ft.Border.all(1, ft.Colors.with_opacity(0.3, color)),
    )


def _participacion_badges(participaciones: list) -> list[ft.Container]:
    if not participaciones:
        return []

    estilos = {
        "titular": ("Titular", _ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)),
        "conyuge": ("Conyuge", _BLUE, ft.Colors.with_opacity(0.12, _BLUE)),
        "hijo": ("Hijo", _WARN, ft.Colors.with_opacity(0.12, _WARN)),
        "dependiente": ("Dependiente", _MUTED, ft.Colors.with_opacity(0.12, _MUTED)),
    }
    orden = {"titular": 0, "conyuge": 1, "hijo": 2, "dependiente": 3}
    tipos = sorted(
        {p.get("tipo_participante", "dependiente") for p in participaciones},
        key=lambda t: orden.get(t, 99),
    )

    badges = []
    for tipo in tipos:
        label, color, bg = estilos.get(tipo, estilos["dependiente"])
        badges.append(
            ft.Container(
                content=ft.Text(label, size=10, color=color, weight=ft.FontWeight.W_500),
                bgcolor=bg,
                padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                border_radius=14,
                border=ft.Border.all(1, ft.Colors.with_opacity(0.3, color)),
            )
        )
    return badges


class ListaAseguradoView:
    """Vista principal del listado de asegurados con paginación real y búsqueda."""

    def __init__(self, page: ft.Page, navigate) -> None:
        self._page = page
        self._navigate = navigate
        self._agente = obtener_agente()

        # ── Estado de datos ───────────────────────────────────────────────
        self._todos: list = []                  # Todos los asegurados cargados
        self._filtered: list = []               # Asegurados filtrados (búsqueda)
        self._visible_filtered: list = []       # Asegurados visibles en la página actual
        self._asegurados_ids: set[int] = set()  # IDs de asegurados cargados
        self._page_num: int = 0                 # Número de página actual (0-based)
        self._total: int = 0                    # Total de registros en el backend
        self._search_scope = "portfolio"        # "portfolio" | "global"
        self._search_query = ""                 # Texto de búsqueda actual

        # ── Caches de datos relacionados (evita N+1 queries) ──────────────
        self._polizas_map: dict = {}              # {id_asegurado: [Poliza]}
        self._participaciones_map: dict = {}      # {id_asegurado: [participacion]}
        self._participantes_poliza_map: dict = {} # {id_poliza: [participante]}

        # ── Referencias a controles de UI (para actualizar dinámicamente) ──
        self._search_field: ft.TextField | None = None      # Campo de búsqueda
        self._scope_help_text: ft.Text | None = None        # Texto ayuda del scope
        self._portfolio_button: ft.Button | None = None     # Botón "Mi cartera"
        self._global_button: ft.Button | None = None        # Botón "Búsqueda global"
        self._list_col = ft.Column(spacing=4)               # Columna del listado
        self._empty_state = ft.Container(visible=False)     # Estado: sin asegurados
        self._no_results_state = ft.Container(visible=False)# Estado: búsqueda sin resultados
        self._global_prompt_state = ft.Container(visible=False) # Estado: global vacío
        self._pagination_row_ref = ft.Ref[ft.Row]()         # Fila de paginación
        self._page_label_ref = ft.Ref[ft.Text]()            # Label "Página X de Y"

    # ── Construcción de la vista completa ───────────────────────────────────

    def build(self) -> ft.Control:
        """Construye la vista completa: sidebar + panel principal."""
        self._load_data()
        from views.dashboard_view import _sidebar
        agente = self._agente
        nombre_agente = (f"{agente.nombre} {agente.apellido_paterno}"
                         if agente else "Agente")
        # Sidebar de navegación lateral
        sidebar = _sidebar(self._navigate, "/clientes")
        # Panel principal con listado, búsqueda y paginación
        main = self._build_main()
        return ft.Container(
            content=ft.Row([sidebar, main], spacing=0, expand=True),
            expand=True,
            bgcolor=_BG,
        )

    # ── Data ─────────────────────────────────────────────────────────────────

    def _load_data(self) -> None:
        agente = self._agente
        if not agente:
            return

        if self._search_scope == "portfolio" and not self._search_query:
            # Paginación real desde el backend (solo titulares)
            result = AseguradoController.get_titulares_by_agente_page(
                agente.id_agente, self._page_num + 1, PAGE_SIZE
            )
            if result["ok"]:
                self._filtered = result["data"]
                self._total = result.get("total", 0)
            else:
                self._filtered = []
                self._total = 0
            self._todos = self._filtered
        elif self._search_scope == "portfolio" and self._search_query:
            # Búsqueda en cartera: buscar global y filtrar titulares en memoria
            result = AseguradoController.search_asegurados(self._search_query)
            data = result.get("data", []) if result["ok"] else []
            # Filtrar solo los del agente
            data = [a for a in data if getattr(a, "id_agente_responsable", None) == agente.id_agente]
            self._todos = data
            self._filtered = self._only_titulares(data)
            self._total = len(self._filtered)
            self._page_num = 0
        else:
            # Global sin query
            self._filtered = []
            self._total = 0

        self._asegurados_ids = {a.id_asegurado for a in self._todos}
        self._load_page_data()

    def _get_search_hint(self) -> str:
        if self._search_scope == "global":
            return "Buscar en todos los asegurados por nombre o RFC…"
        return "Filtrar mi cartera por nombre o RFC…"

    def _get_scope_help_text(self) -> str:
        if self._search_scope == "global":
            return "Búsqueda global activada. Puedes abrir clientes de cualquier agente."
        return "Mostrando tu cartera. Cambia a búsqueda global cuando necesites salir de ella."

    def _scope_button_style(self, active: bool) -> ft.ButtonStyle:
        return ft.ButtonStyle(
            bgcolor={
                ft.ControlState.DEFAULT: _ACCENT if active else _CARD2,
                ft.ControlState.HOVERED: _ACCENT_HOVER if active else _CARD,
            },
            shape=ft.RoundedRectangleBorder(radius=999),
            side={
                ft.ControlState.DEFAULT: ft.BorderSide(1, _ACCENT if active else _BORDER)
            },
            padding=ft.Padding.symmetric(horizontal=16, vertical=0),
            elevation={"pressed": 0, "": 0},
        )

    def _apply_scope_ui(self) -> None:
        if self._search_field is not None:
            self._search_field.hint_text = self._get_search_hint()
        if self._scope_help_text is not None:
            self._scope_help_text.value = self._get_scope_help_text()

        for scope, button in (
            ("portfolio", self._portfolio_button),
            ("global", self._global_button),
        ):
            if button is None:
                continue
            active = self._search_scope == scope
            button.style = self._scope_button_style(active)
            if isinstance(button.content, ft.Text):
                button.content.color = "#000000" if active else _TEXT

    def _set_search_scope(self, scope: str) -> None:
        if scope not in {"portfolio", "global"} or scope == self._search_scope:
            return

        self._search_scope = scope
        self._search_query = ""
        self._page_num = 0
        self._polizas_map.clear()
        self._participaciones_map.clear()

        if self._search_field is not None:
            self._search_field.value = ""

        self._apply_scope_ui()

        if self._search_scope == "portfolio":
            self._load_data()
        else:
            self._filtered = []
            self._total = 0

        self._render_list(self._filtered, searched=False)
        self._page.update()

    def _load_page_data(self) -> None:
        """Load polizas, participaciones and participantes in batch for visible asegurados."""
        if not self._filtered:
            return

        # ¿El backend ya devolvió solo los de esta página?
        backend_paginated = (
            self._search_scope == "portfolio"
            and not self._search_query
        )

        if backend_paginated:
            page_items = self._filtered
        else:
            start = self._page_num * PAGE_SIZE
            end = start + PAGE_SIZE
            page_items = self._filtered[start:end]
        ids = [a.id_asegurado for a in page_items]
        if not ids:
            return

        # 1. Cargar pólizas en batch
        ids_sin_polizas = [aid for aid in ids if aid not in self._polizas_map]
        if ids_sin_polizas:
            res = PolizaController.get_polizas_by_asegurado_ids(ids_sin_polizas)
            if res["ok"]:
                for poliza in res["data"]:
                    aid = poliza.id_asegurado
                    if aid not in self._polizas_map:
                        self._polizas_map[aid] = []
                    self._polizas_map[aid].append(poliza)
            # Asegurar que todos tengan lista (aunque vacía)
            for aid in ids_sin_polizas:
                if aid not in self._polizas_map:
                    self._polizas_map[aid] = []

        # 2. Cargar participaciones en batch
        ids_sin_part = [aid for aid in ids if aid not in self._participaciones_map]
        if ids_sin_part:
            res = PolizaController.get_participaciones_by_asegurado_ids(ids_sin_part)
            if res["ok"]:
                for part in res["data"]:
                    aid = part.get("id_asegurado")
                    if aid is not None:
                        if aid not in self._participaciones_map:
                            self._participaciones_map[aid] = []
                        self._participaciones_map[aid].append(part)
            for aid in ids_sin_part:
                if aid not in self._participaciones_map:
                    self._participaciones_map[aid] = []

        # 3. Cargar participantes de pólizas en batch
        poliza_ids = set()
        for a in page_items:
            for p in self._polizas_map.get(a.id_asegurado, []):
                poliza_ids.add(p.id_poliza)
        ids_sin_partic = [pid for pid in poliza_ids if pid not in self._participantes_poliza_map]
        if ids_sin_partic:
            res = PolizaController.get_participantes_by_poliza_ids(ids_sin_partic)
            if res["ok"]:
                for part in res["data"]:
                    pid = part.get("id_poliza")
                    if pid is not None:
                        if pid not in self._participantes_poliza_map:
                            self._participantes_poliza_map[pid] = []
                        self._participantes_poliza_map[pid].append(part)
            for pid in ids_sin_partic:
                if pid not in self._participantes_poliza_map:
                    self._participantes_poliza_map[pid] = []

    # ── Main panel ────────────────────────────────────────────────────────────

    def _build_main(self) -> ft.Container:
        """Construye el panel principal: barra superior, búsqueda, listado y paginación."""

        # ── Campo de búsqueda por nombre o RFC ────────────────────────────
        self._search_field = ft.TextField(
            hint_text=self._get_search_hint(),
            hint_style=ft.TextStyle(color=_MUTED, size=14),
            text_style=ft.TextStyle(color=_TEXT, size=14),
            prefix_icon=ft.Icons.SEARCH_ROUNDED,
            border_color=_BORDER,
            focused_border_color=_ACCENT,
            bgcolor=_CARD,
            border_radius=10,
            content_padding=ft.Padding.symmetric(horizontal=16, vertical=14),
            expand=True,
            on_change=lambda e: self._filter(e.control.value),
        )

        # ── Botones de scope: Mi cartera / Búsqueda global ────────────────
        self._portfolio_button = ft.Button(
            content=ft.Text(
                "Mi cartera",
                size=12,
                weight=ft.FontWeight.W_600,
                color="#000000",
            ),
            height=40,
            style=self._scope_button_style(True),
            on_click=lambda e: self._set_search_scope("portfolio"),
        )
        self._global_button = ft.Button(
            content=ft.Text(
                "Búsqueda global",
                size=12,
                weight=ft.FontWeight.W_600,
                color=_TEXT,
            ),
            height=40,
            style=self._scope_button_style(False),
            on_click=lambda e: self._set_search_scope("global"),
        )
        self._scope_help_text = ft.Text(
            self._get_scope_help_text(),
            size=12,
            color=_MUTED,
        )

        # ── Botón "Nuevo asegurado" (esquina superior derecha) ────────────
        btn_nuevo = ft.Button(
            content=ft.Row(
                [
                    ft.Icon(ft.Icons.ADD_ROUNDED, size=16, color="#000000"),
                    ft.Text("Nuevo asegurado", size=13,
                            weight=ft.FontWeight.W_600, color="#000000"),
                ],
                spacing=6,
                tight=True,
            ),
            height=46,
            style=ft.ButtonStyle(
                bgcolor={ft.ControlState.DEFAULT: _ACCENT,
                         ft.ControlState.HOVERED: _ACCENT_HOVER},
                shape=ft.RoundedRectangleBorder(radius=10),
                padding=ft.Padding.symmetric(horizontal=18, vertical=0),
                elevation={"pressed": 0, "": 1},
            ),
            on_click=lambda e: self._navigate("/asegurado/nuevo"),
        )

        # ── Barra superior con título "Asegurados" ────────────────────────
        topbar = ft.Container(
            content=ft.Row(
                [
                    ft.Text("Asegurados", size=18,
                            weight=ft.FontWeight.BOLD, color=_TEXT),
                ],
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=28, vertical=16),
            border=ft.Border.only(bottom=ft.BorderSide(1, _BORDER)),
        )

        # ── Estado vacío: sin asegurados registrados ──────────────────────
        self._empty_state = _empty_state_view(
            ft.Icons.PERSON_OFF_OUTLINED,
            "Aún no tienes asegurados registrados",
            "Agrega tu primer asegurado con el botón de arriba.",
            action=ft.Button(
                content=ft.Row(
                    [
                        ft.Icon(ft.Icons.ADD_ROUNDED, size=16, color="#000000"),
                        ft.Text("Nuevo asegurado", size=13, weight=ft.FontWeight.W_600, color="#000000"),
                    ],
                    spacing=6,
                    tight=True,
                ),
                height=46,
                style=ft.ButtonStyle(
                    bgcolor={ft.ControlState.DEFAULT: _ACCENT, ft.ControlState.HOVERED: _ACCENT_HOVER},
                    shape=ft.RoundedRectangleBorder(radius=10),
                    padding=ft.Padding.symmetric(horizontal=18, vertical=0),
                ),
                on_click=lambda e: self._navigate("/asegurado/nuevo"),
            ),
            visible=False,
        )

        # ── Estado vacío: búsqueda sin resultados ─────────────────────────
        self._no_results_state = _empty_state_view(
            ft.Icons.SEARCH_OFF_ROUNDED,
            "Sin resultados",
            "No se encontraron resultados para ese nombre o RFC.",
            title_color=_MUTED,
            message_color=_MUTED,
            visible=False,
        )

        # ── Estado vacío: búsqueda global lista (sin texto aún) ───────────
        self._global_prompt_state = _empty_state_view(
            ft.Icons.TRAVEL_EXPLORE_ROUNDED,
            "Búsqueda global lista",
            "Escribe un nombre o RFC para consultar asegurados de cualquier agente.",
            icon_color=_BLUE,
            visible=False,
        )

        # Render inicial del listado (puede estar vacío hasta cargar datos)
        self._render_list(self._filtered)

        # ── Cuerpo del listado con Stack para superponer estados vacíos ───
        body = ft.Container(
            content=ft.Stack(
                [
                    self._list_col,
                    self._empty_state,
                    self._no_results_state,
                    self._global_prompt_state,
                ],
                expand=True,
            ),
            expand=True,
        )

        # ── Fila de paginación (anterior / página X de Y / siguiente) ─────
        pagination = ft.Row(
            ref=self._pagination_row_ref,
            controls=self._build_pagination_controls(),
            alignment=ft.MainAxisAlignment.CENTER,
        )

        # ── Ensamblado final del panel principal ──────────────────────────
        return ft.Container(
            content=ft.Column(
                [
                    topbar,
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [self._portfolio_button, self._global_button],
                                    spacing=10,
                                    wrap=True,
                                ),
                                self._scope_help_text,
                                ft.Row(
                                    [self._search_field, btn_nuevo],
                                    spacing=12,
                                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                                ),
                                ft.Container(height=4),
                                body,
                                pagination,
                            ],
                            spacing=12,
                            scroll=ft.ScrollMode.AUTO,
                            expand=True,
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

    # ── Participantes helpers ─────────────────────────────────────────────────

    _PART_STYLE = {
        "titular":    ("Titular",    _ACCENT, ft.Colors.with_opacity(0.12, _ACCENT), ft.Colors.with_opacity(0.35, _ACCENT)),
        "conyuge":    ("Conyuge",    _BLUE,   ft.Colors.with_opacity(0.14, _BLUE),   ft.Colors.with_opacity(0.25, _BLUE)),
        "hijo":       ("Hijo",       _WARN,   ft.Colors.with_opacity(0.14, _WARN),   ft.Colors.with_opacity(0.25, _WARN)),
        "dependiente":("Dependiente",_MUTED,  _CARD2,                                ft.Colors.with_opacity(0.20, _MUTED)),
    }

    def _pill(self, label: str, fg: str, bg: str) -> ft.Container:
        return _pill_global(label, fg, bg)

    def _short_person_name(self, full_name: str | None) -> str:
        parts = [part for part in str(full_name or "").split() if part]
        if not parts:
            return "Sin nombre"
        if len(parts) == 1:
            return parts[0]
        return f"{parts[0]} {parts[1][0]}."

    def _policy_metrics(self, asegurado, polizas: list, participaciones: list) -> tuple[float, int, int]:
        policy_totals: dict[int, float] = {}
        personas_unicas: set[str] = set()

        for poliza in polizas:
            try:
                policy_totals[poliza.id_poliza] = float(getattr(poliza, "prima_mensual", 0) or 0)
            except (TypeError, ValueError):
                policy_totals[poliza.id_poliza] = 0.0

            participantes = self._participantes_poliza_map.get(poliza.id_poliza, [])
            if participantes:
                visibles = list(participantes) if self._search_scope == "global" else [
                    p for p in participantes if p.get("id_asegurado") in self._asegurados_ids
                ]
                for participante in visibles:
                    pid = participante.get("id_asegurado")
                    if pid is not None:
                        personas_unicas.add(f"id:{pid}")
                    else:
                        personas_unicas.add(f"name:{participante.get('nombre_completo', '')}")
            else:
                personas_unicas.add(f"id:{asegurado.id_asegurado}")

        for participacion in participaciones:
            pid = participacion.get("id_poliza")
            if pid and pid not in policy_totals:
                try:
                    policy_totals[pid] = float(
                        participacion.get("prima_mensual")
                        or participacion.get("prima_mensual_poliza")
                        or 0
                    )
                except (TypeError, ValueError):
                    policy_totals[pid] = 0.0

            person_id = participacion.get("id_asegurado")
            if person_id is not None:
                personas_unicas.add(f"id:{person_id}")
            elif participacion.get("nombre_completo"):
                personas_unicas.add(f"name:{participacion['nombre_completo']}")

        if not personas_unicas:
            personas_unicas.add(f"id:{asegurado.id_asegurado}")

        return sum(policy_totals.values()), len(policy_totals), len(personas_unicas)

    def _participant_card(self, participante: dict, *, compact: bool = False) -> ft.Container:
        tipo = participante.get("tipo_asegurado", "dependiente")
        label, fg, bg, border = self._PART_STYLE.get(tipo, self._PART_STYLE["dependiente"])
        aid = participante.get("id_asegurado")
        nombre = participante.get("nombre_completo", "Sin nombre")
        titulo = self._short_person_name(nombre) if compact else nombre

        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(titulo, size=12, color=_TEXT, weight=ft.FontWeight.W_600),
                    self._pill(label, fg, bg),
                ],
                spacing=6,
            ),
            padding=ft.Padding.symmetric(horizontal=12, vertical=10),
            bgcolor=_CARD,
            border_radius=10,
            border=ft.Border.all(1, border),
            col={"xs": 12, "sm": 6, "lg": 3},
            on_click=(lambda e, asegurado_id=aid: self._navigate("/asegurado/detalle", id_asegurado=asegurado_id)) if aid else None,
            ink=bool(aid),
        )

    def _personas_cubiertas_section(self, participantes: list) -> list:
        """Build participant cards for one poliza without profile avatars."""
        # En portfolio mostramos todos los participantes de la poliza del titular;
        # en global filtramos solo los que estan cargados en la busqueda actual.
        if self._search_scope == "global":
            visibles = [
                p for p in participantes
                if p.get("id_asegurado") in self._asegurados_ids
            ]
        else:
            visibles = list(participantes)

        if not visibles:
            return [ft.Text("Sin personas cubiertas visibles en esta póliza.", size=11, color=_MUTED)]

        orden = {"titular": 0, "conyuge": 1, "hijo": 2, "dependiente": 3}
        visibles = sorted(
            visibles,
            key=lambda x: (
                orden.get(x.get("tipo_asegurado", "dependiente"), 99),
                str(x.get("nombre_completo", "")),
            ),
        )

        cards = [
            self._participant_card(
                participante,
                compact=participante.get("tipo_asegurado") != "titular",
            )
            for participante in visibles
        ]

        return [ft.ResponsiveRow(cards, spacing=10, run_spacing=10)]

    # ── Row builder ───────────────────────────────────────────────────────────

    def _build_row(self, asegurado, polizas: list, participaciones: list) -> ft.Container:
        nombre = (f"{asegurado.nombre} {asegurado.apellido_paterno} "
                  f"{asegurado.apellido_materno}".strip())
        celular = asegurado.celular or "—"
        iniciales = ((asegurado.nombre or " ")[:1] + (asegurado.apellido_paterno or " ")[:1]).upper()
        es_externo = bool(
            self._agente
            and getattr(asegurado, "id_agente_responsable", None) not in (None, self._agente.id_agente)
        )
        resumen_badges = [_status_badge(polizas, participaciones), *_participacion_badges(participaciones)]
        if self._search_scope == "global":
            resumen_badges.append(
                self._pill(
                    "Cartera externa" if es_externo else "Mi cartera",
                    _BLUE if es_externo else _ACCENT,
                    ft.Colors.with_opacity(0.12, _BLUE if es_externo else _ACCENT),
                )
            )

        total_mensual, total_polizas, total_personas = self._policy_metrics(
            asegurado,
            polizas,
            participaciones,
        )

        # Build poliza cards with participant cards styled for the list surface.
        poliza_cards: list = []
        estatus_colors = {
            "activa":    (_ACCENT, ft.Colors.with_opacity(0.12, _ACCENT)),
            "vencida":   (_ERROR,  ft.Colors.with_opacity(0.12, _ERROR)),
            "cancelada": (_MUTED,  _CARD2),
        }
        for p in polizas:
            fg, bg = estatus_colors.get(p.estatus, (_MUTED, _CARD2))
            participantes = self._participantes_poliza_map.get(p.id_poliza, [])
            personas = self._personas_cubiertas_section(participantes)
            poliza_cards.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row(
                                [
                                    ft.Column(
                                        [
                                            ft.Row(
                                                [
                                                    ft.Text(str(p.numero_poliza), size=15, weight=ft.FontWeight.W_700, color=_TEXT),
                                                ],
                                                spacing=6,
                                            ),
                                            ft.Row(
                                                [
                                                    ft.Text(f"{p.fecha_inicio} -> {p.fecha_vencimiento}", size=11, color=_MUTED),
                                                    self._pill(p.estatus.capitalize(), fg, bg),
                                                ],
                                                spacing=8,
                                                wrap=True,
                                            ),
                                        ],
                                        spacing=4,
                                        expand=True,
                                    ),
                                    ft.Column(
                                        [
                                            ft.Text(f"${float(getattr(p, 'prima_mensual', 0) or 0):,.0f}", size=18, weight=ft.FontWeight.BOLD, color=_WARN),
                                            ft.Text("/mes", size=11, color=_MUTED, weight=ft.FontWeight.W_600),
                                        ],
                                        spacing=2,
                                        horizontal_alignment=ft.CrossAxisAlignment.END,
                                    ),
                                ],
                                spacing=10,
                                vertical_alignment=ft.CrossAxisAlignment.START,
                            ),
                            ft.Divider(color=_BORDER, height=10),
                            *personas,
                        ],
                        spacing=8,
                    ),
                    padding=ft.Padding.symmetric(horizontal=16, vertical=14),
                    bgcolor=_CARD2,
                    border_radius=12,
                    border=ft.Border.all(1, _BORDER),
                )
            )

        if not polizas and participaciones:
            for participacion in participaciones:
                role = participacion.get("tipo_participante", "dependiente")
                role_label, role_fg, role_bg, _ = self._PART_STYLE.get(
                    role,
                    self._PART_STYLE["dependiente"],
                )
                status_fg, status_bg = estatus_colors.get(
                    participacion.get("estatus_poliza"),
                    (_MUTED, _CARD2),
                )
                poliza_cards.append(
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.Column(
                                            [
                                                ft.Row(
                                                    [
                                                        ft.Text(
                                                            str(participacion.get('numero_poliza', '—')),
                                                            size=15,
                                                            weight=ft.FontWeight.W_600,
                                                            color=_TEXT,
                                                        ),
                                                        self._pill(
                                                            str(participacion.get("estatus_poliza", "activa")).capitalize(),
                                                            status_fg,
                                                            status_bg,
                                                        ),
                                                        self._pill(role_label, role_fg, role_bg),
                                                    ],
                                                    spacing=6,
                                                    wrap=True,
                                                ),
                                                ft.Text(
                                                    "Cobertura derivada desde una póliza donde participa este asegurado.",
                                                    size=11,
                                                    color=_MUTED,
                                                ),
                                            ],
                                            spacing=2,
                                            expand=True,
                                        ),
                                    ],
                                    spacing=10,
                                    vertical_alignment=ft.CrossAxisAlignment.START,
                                ),
                            ],
                            spacing=8,
                        ),
                        padding=ft.Padding.symmetric(horizontal=16, vertical=14),
                        bgcolor=_CARD2,
                        border_radius=12,
                        border=ft.Border.all(1, _BORDER),
                    )
                )
        elif not poliza_cards:
            poliza_cards.append(
                ft.Container(
                    content=ft.Text("Sin póliza", size=12, color=_MUTED),
                    padding=ft.Padding.symmetric(horizontal=4, vertical=4),
                )
            )

        info_card = ft.Container(
            content=ft.Row(
                [
                    ft.Container(
                        content=ft.Text(iniciales, size=16, color=_TEXT, weight=ft.FontWeight.BOLD),
                        width=44,
                        height=44,
                        border_radius=22,
                        bgcolor=_CARD,
                        alignment=ft.Alignment.CENTER,
                        border=ft.Border.all(1, _BORDER),
                    ),
                    ft.Column(
                        [
                            ft.Text(nombre, size=18, weight=ft.FontWeight.W_700, color=_TEXT),
                            ft.Text(f"{asegurado.rfc} · {celular}", size=12, color=_MUTED),
                            ft.Row(resumen_badges, spacing=6, wrap=True),
                        ],
                        spacing=6,
                        expand=True,
                    ),
                    ft.Container(width=1, height=52, bgcolor=_BORDER),
                    ft.Column(
                        [
                            ft.Text("Total mensual", size=11, color=_MUTED, text_align=ft.TextAlign.RIGHT),
                            ft.Text(f"${total_mensual:,.0f}", size=18, weight=ft.FontWeight.BOLD, color=_WARN, text_align=ft.TextAlign.RIGHT),
                            ft.Text(f"{total_polizas} póliza(s) · {total_personas} persona(s)", size=12, color=_MUTED, text_align=ft.TextAlign.RIGHT),
                        ],
                        spacing=2,
                        horizontal_alignment=ft.CrossAxisAlignment.END,
                    ),
                ],
                spacing=14,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=18, vertical=16),
            bgcolor=_CARD2,
            border_radius=12,
            border=ft.Border.all(1, _BORDER),
            on_click=lambda e, aid=asegurado.id_asegurado: self._navigate(
                "/asegurado/detalle",
                id_asegurado=aid,
            ),
            ink=True,
        )

        return ft.Container(
            content=ft.Column(
                [
                    info_card,
                    ft.Container(
                        content=ft.Column(poliza_cards, spacing=12),
                    ),
                ],
                spacing=14,
            ),
            padding=ft.Padding.symmetric(horizontal=20, vertical=14),
            bgcolor=_CARD,
            border_radius=12,
            border=ft.Border.all(1, _BORDER),
        )

    # ── Pagination ────────────────────────────────────────────────────────────

    # ── Paginación ────────────────────────────────────────────────────────────

    def _build_pagination_controls(self) -> list:
        """Crea los controles de paginación: [Anterior] [Página X de Y] [Siguiente]."""
        total_pages = max(1, (self._total + PAGE_SIZE - 1) // PAGE_SIZE)
        page_label = ft.Text(
            ref=self._page_label_ref,
            value=f"Página {self._page_num + 1} de {total_pages}",
            size=13, color=_TEXT,
        )
        # Botón "Página anterior"
        btn_prev = ft.IconButton(
            icon=ft.Icons.CHEVRON_LEFT_ROUNDED,
            icon_color=_TEXT if self._page_num > 0 else _MUTED,
            disabled=self._page_num == 0,
            on_click=lambda e: self._prev_page(),
            tooltip="Página anterior",
        )
        # Botón "Página siguiente"
        btn_next = ft.IconButton(
            icon=ft.Icons.CHEVRON_RIGHT_ROUNDED,
            icon_color=_TEXT if self._page_num < total_pages - 1 else _MUTED,
            disabled=self._page_num >= total_pages - 1,
            on_click=lambda e: self._next_page(),
            tooltip="Página siguiente",
        )
        return [btn_prev, page_label, btn_next]

    def _update_pagination(self) -> None:
        """Actualiza la fila de paginación con los controles actuales."""
        row = self._pagination_row_ref.current
        if row is None:
            return
        total_pages = max(1, (self._total + PAGE_SIZE - 1) // PAGE_SIZE)
        row.controls = self._build_pagination_controls()
        row.visible = self._total > 0

    def _prev_page(self) -> None:
        """Acción al hacer clic en "Página anterior"."""
        if self._page_num > 0:
            self._page_num -= 1
            if self._search_scope == "portfolio" and not self._search_query:
                self._load_data()
            else:
                self._load_page_data()
            self._render_list(self._filtered)
            self._page.update()

    def _next_page(self) -> None:
        """Acción al hacer clic en "Página siguiente"."""
        total_pages = max(1, (self._total + PAGE_SIZE - 1) // PAGE_SIZE)
        if self._page_num < total_pages - 1:
            self._page_num += 1
            if self._search_scope == "portfolio" and not self._search_query:
                self._load_data()
            else:
                self._load_page_data()
            self._render_list(self._filtered)
            self._page.update()

    # ── Filter ────────────────────────────────────────────────────────────────

    def _filter(self, query: str) -> None:
        q = query.strip()
        self._search_query = q
        _GLOBAL_LIMIT = 100
        if self._search_scope == "global":
            if not q:
                self._filtered = []
                self._total = 0
            else:
                result = AseguradoController.search_asegurados(q)
                data = result.get("data", []) if result["ok"] else []
                self._filtered = data[:_GLOBAL_LIMIT]
                self._total = len(self._filtered)
        else:
            if not q:
                self._page_num = 0
                self._load_data()
                self._render_list(self._filtered, searched=False)
                self._page.update()
                return
            else:
                # Búsqueda en cartera con query
                result = AseguradoController.search_asegurados(q)
                data = result.get("data", []) if result["ok"] else []
                agente = self._agente
                if agente:
                    data = [a for a in data if getattr(a, "id_agente_responsable", None) == agente.id_agente]
                self._todos = data
                self._filtered = self._only_titulares(data)
                self._total = len(self._filtered)
        self._page_num = 0
        self._load_page_data()
        self._render_list(self._filtered, searched=bool(q))
        self._page.update()

    def _render_list(self, asegurados: list, searched: bool = False) -> None:
        self._list_col.controls.clear()
        self._empty_state.visible = False
        self._no_results_state.visible = False
        self._global_prompt_state.visible = False
        self._visible_filtered = []

        # ¿Paginación real del backend? (portfolio sin búsqueda)
        backend_paginated = (
            self._search_scope == "portfolio"
            and not self._search_query
        )

        if self._search_scope == "global" and not self._search_query:
            self._global_prompt_state.visible = True
        elif not self._filtered:
            if self._search_scope == "portfolio" and not self._search_query:
                self._empty_state.visible = True
            else:
                self._no_results_state.visible = True
        else:
            self._visible_filtered = list(asegurados)

        if self._search_scope != "global" or self._search_query:
            total_pages = max(1, (self._total + PAGE_SIZE - 1) // PAGE_SIZE)
            if self._page_num >= total_pages:
                self._page_num = 0

        if self._search_scope == "global" and not self._search_query:
            pass
        elif not self._visible_filtered:
            self._no_results_state.visible = True
        else:
            if backend_paginated:
                # El backend ya devolvió solo los de esta página
                page_slice = self._visible_filtered
            else:
                start = self._page_num * PAGE_SIZE
                end = start + PAGE_SIZE
                page_slice = self._visible_filtered[start:end]
            for a in page_slice:
                polizas = self._polizas_map.get(a.id_asegurado, [])
                participaciones = self._participaciones_map.get(a.id_asegurado, [])
                self._list_col.controls.append(
                    self._build_row(a, polizas, participaciones)
                )
        self._update_pagination()

    def _is_titular(self, asegurado) -> bool:
        aid = asegurado.id_asegurado

        if aid not in self._polizas_map:
            polizas_result = PolizaController.get_polizas_by_asegurado(aid)
            self._polizas_map[aid] = polizas_result["data"] if polizas_result["ok"] else []
        if aid not in self._participaciones_map:
            participaciones_result = PolizaController.get_participaciones_by_asegurado(aid)
            self._participaciones_map[aid] = participaciones_result["data"] if participaciones_result["ok"] else []

        polizas = self._polizas_map.get(aid, [])
        if polizas:
            return True

        participaciones = self._participaciones_map.get(aid, [])
        return any(
            participacion.get("tipo_participante") == "titular"
            for participacion in participaciones
        )

    def _only_titulares(self, asegurados: list) -> list:
        return [asegurado for asegurado in asegurados if self._is_titular(asegurado)]