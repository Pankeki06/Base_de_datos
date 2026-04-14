"""Vista principal (Home) del dashboard.

Muestra:
- Nombre del agente activo + botón cerrar sesión
- Buscador de asegurados por nombre o RFC
- Últimos 6 asegurados contactados (cards vacías por ahora)
"""

import flet as ft
import re


# ---------------------------------------------------------------------------
# Datos mock de asegurados para el buscador
# (sustituir por consulta a MySQL cuando esté listo)
# ---------------------------------------------------------------------------
ASEGURADOS_MOCK: list[dict] = [
    {
        "nombre": "Carlos Méndez López",
        "rfc": "MELC850312ABC",
        "celular": "9611234567",
        "polizas": ["Vida", "Auto"],
    },
    {
        "nombre": "Ana García Ruiz",
        "rfc": "GARA920105XYZ",
        "celular": "9619876543",
        "polizas": ["Gastos Médicos"],
    },
    {
        "nombre": "José Hernández Torres",
        "rfc": "HETJ780620DEF",
        "celular": "9614561230",
        "polizas": ["Auto", "Hogar"],
    },
    {
        "nombre": "María Pérez Soto",
        "rfc": "PESM010315GHI",
        "celular": "9617890123",
        "polizas": ["Vida", "Gastos Médicos", "Hogar"],
    },
    {
        "nombre": "Luis Ramírez Cruz",
        "rfc": "RACL670908JKL",
        "celular": "9612345678",
        "polizas": ["Auto"],
    },
    {
        "nombre": "Sandra Torres Díaz",
        "rfc": "TODS991224MNO",
        "celular": "9618765432",
        "polizas": ["Vida"],
    },
]

# Colores para las etiquetas de pólizas
POLIZA_COLORES: dict[str, str] = {
    "Vida":           "#4CAF50",
    "Auto":           "#2196F3",
    "Gastos Médicos": "#FF9800",
    "Hogar":          "#9C27B0",
}


def _color_poliza(nombre: str) -> str:
    return POLIZA_COLORES.get(nombre, "#607D8B")


# ---------------------------------------------------------------------------
# Constructor principal
# ---------------------------------------------------------------------------
def create_home_view(page: ft.Page, agente=None) -> ft.Column:
    """
    Parameters
    ----------
    page   : ft.Page  – referencia a la página de Flet
    agente : Agente   – objeto SQLModel devuelto por AuthController (puede ser None en dev)
    """

    # Nombre del agente: acceso directo a atributos del modelo SQLModel
    nombre_agente = "Agente"
    if agente:
        try:
            nombre_agente = f"{agente.nombre} {agente.apellido_paterno}"
        except AttributeError:
            nombre_agente = str(agente)

    # -----------------------------------------------------------------------
    # CERRAR SESIÓN
    # -----------------------------------------------------------------------
    def cerrar_sesion(e):
        from views.login_view import create_login_view
        page.controls.clear()
        page.add(create_login_view(page))
        page.update()

    # -----------------------------------------------------------------------
    # HEADER: nombre del agente + botón cerrar sesión
    # -----------------------------------------------------------------------
    header = ft.Row(
        controls=[
            ft.Row(
                controls=[
                    ft.Icon(ft.Icons.ACCOUNT_CIRCLE, size=36, color=ft.Colors.BLUE_400),
                    ft.Column(
                        controls=[
                            ft.Text(
                                f"Bienvenido, {nombre_agente}",
                                size=18,
                                weight=ft.FontWeight.BOLD,
                            ),
                            ft.Text(
                                "Agente activo",
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                        ],
                        spacing=0,
                    ),
                ],
                spacing=10,
            ),
            ft.ElevatedButton(
                content=ft.Row(
                    [ft.Icon(ft.Icons.LOGOUT, color=ft.Colors.WHITE, size=18),
                     ft.Text("Cerrar sesión", color=ft.Colors.WHITE)],
                    spacing=6,
                    tight=True,
                ),
                on_click=cerrar_sesion,
                style=ft.ButtonStyle(
                    bgcolor=ft.Colors.RED_400,
                    padding=ft.padding.symmetric(horizontal=16, vertical=10),
                ),
            ),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )

    # -----------------------------------------------------------------------
    # BUSCADOR + RESULTADOS
    # -----------------------------------------------------------------------
    resultados_col = ft.Column(spacing=8, visible=False)

    def _etiquetas_poliza(polizas: list[str]) -> ft.Row:
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(p, size=11, color=ft.Colors.WHITE),
                    bgcolor=_color_poliza(p),
                    border_radius=12,
                    padding=ft.padding.symmetric(horizontal=8, vertical=3),
                )
                for p in polizas
            ],
            spacing=6,
            wrap=True,
        )

    def _tarjeta_asegurado(a: dict) -> ft.Card:
        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(horizontal=16, vertical=12),
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(ft.Icons.PERSON, color=ft.Colors.BLUE_400, size=20),
                                ft.Text(
                                    a["nombre"],
                                    weight=ft.FontWeight.BOLD,
                                    size=14,
                                    expand=1,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Text(
                            f"RFC: {a['rfc']}  |  Cel: {a['celular']}",
                            size=12,
                            color=ft.Colors.GREY_600,
                        ),
                        _etiquetas_poliza(a.get("polizas", [])),
                    ],
                    spacing=6,
                ),
                on_click=lambda e, aseg=a: _ir_detalle(aseg),
                ink=True,
                border_radius=8,
            ),
            elevation=2,
        )

    def _ir_detalle(asegurado: dict):
        """Navega al detalle del asegurado (placeholder hasta implementar la vista)."""
        snack = ft.SnackBar(
            ft.Text(f"Detalle de {asegurado['nombre']} — próximamente")
        )
        try:
            page.open(snack)
        except AttributeError:
            page.snack_bar = snack
            page.snack_bar.open = True
            page.update()

    def buscar(e):
        query = (buscador.value or "").strip().lower()
        resultados_col.controls.clear()

        if not query:
            resultados_col.visible = False
            page.update()
            return

        encontrados = [
            a for a in ASEGURADOS_MOCK
            if query in a["nombre"].lower() or query in a["rfc"].lower()
        ]

        if encontrados:
            resultados_col.controls.append(
                ft.Text(
                    f"{len(encontrados)} resultado(s)",
                    size=12,
                    color=ft.Colors.GREY_600,
                )
            )
            for a in encontrados:
                resultados_col.controls.append(_tarjeta_asegurado(a))
        else:
            resultados_col.controls.append(
                ft.Text(
                    "Sin resultados para esa búsqueda.",
                    color=ft.Colors.GREY_500,
                    italic=True,
                )
            )

        resultados_col.visible = True
        page.update()

    buscador = ft.TextField(
        label="Buscar asegurado por nombre o RFC…",
        prefix_icon=ft.Icons.SEARCH,
        on_change=buscar,
        expand=True,
        border_radius=10,
    )

    seccion_buscador = ft.Column(
        controls=[
            ft.Text(
                "Buscador de Asegurados",
                size=16,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.BLUE_400,
            ),
            ft.Row([buscador], expand=True),
            resultados_col,
        ],
        spacing=10,
    )

    # -----------------------------------------------------------------------
    # ÚLTIMOS 6 ASEGURADOS CONTACTADOS (cards vacías por ahora)
    # -----------------------------------------------------------------------
    def _card_vacia() -> ft.Card:
        return ft.Card(
            content=ft.Container(
                padding=ft.padding.symmetric(horizontal=16, vertical=14),
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Icon(
                                    ft.Icons.PERSON_OUTLINE,
                                    color=ft.Colors.GREY_400,
                                    size=20,
                                ),
                                ft.Text(
                                    "—",
                                    color=ft.Colors.GREY_400,
                                    size=14,
                                    expand=1,
                                ),
                            ],
                            spacing=8,
                        ),
                        ft.Text(
                            "Sin datos aún",
                            size=12,
                            color=ft.Colors.GREY_400,
                            italic=True,
                        ),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    content=ft.Text("—", size=11, color=ft.Colors.WHITE),
                                    bgcolor=ft.Colors.GREY_300,
                                    border_radius=12,
                                    padding=ft.padding.symmetric(horizontal=8, vertical=3),
                                )
                            ]
                        ),
                    ],
                    spacing=6,
                ),
                ink=True,
                border_radius=8,
            ),
            elevation=1,
        )

    # Grid 2 columnas × 3 filas
    ultimos_grid = ft.Column(
        controls=[
            ft.Row(
                controls=[_card_vacia(), _card_vacia()],
                spacing=12,
                expand=True,
            )
            for _ in range(3)
        ],
        spacing=10,
    )

    seccion_ultimos = ft.Column(
        controls=[
            ft.Text(
                "Últimos 6 Asegurados Contactados",
                size=16,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.BLUE_400,
            ),
            ft.Text(
                "Toca cualquier tarjeta para ver el detalle.",
                size=12,
                color=ft.Colors.GREY_500,
            ),
            ultimos_grid,
        ],
        spacing=8,
    )

    # -----------------------------------------------------------------------
    # LAYOUT RAÍZ
    # -----------------------------------------------------------------------
    contenido = ft.Column(
        controls=[
            header,
            ft.Divider(height=1),
            seccion_buscador,
            ft.Divider(height=1),
            seccion_ultimos,
        ],
        spacing=16,
        scroll=ft.ScrollMode.ALWAYS,
        expand=True,
    )

    return ft.Column(
        controls=[
            ft.Container(
                content=contenido,
                expand=True,
                padding=ft.padding.symmetric(horizontal=32, vertical=16),
            )
        ],
        expand=True,
    )