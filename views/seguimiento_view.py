"""Vista de formulario de Seguimiento — compatible con Flet 0.21+"""
import re
from datetime import datetime

import flet as ft

# ════════════════════════════════════════════════════════════════
# NOTAS DE COMPATIBILIDAD (Flet < 0.21):
#   ft.Icons.*  (minúsculas)   ft.Colors.*  (minúsculas)
#   scroll=True                page.overlay para AlertDialog
#   ft.Row con expand=True cuando sus hijos usan expand=N
# ════════════════════════════════════════════════════════════════

# Patrón de fecha-hora aceptado: YYYY-MM-DD HH:MM
_FECHA_PATTERN = re.compile(r'^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]) ([01]\d|2[0-3]):[0-5]\d$')


def create_seguimiento_view(page: ft.Page) -> ft.Column:
    """
    Formulario de seguimiento basado en el modelo Seguimiento:
        id_asegurado  (int, FK)
        id_agente     (int, FK)
        tipo_contacto (str ≤ 20)
        observaciones (str ≤ 1000)
        resultado     (str ≤ 20)
        fecha_hora    (datetime)

    Retorna ft.Column con expand=True para que el Tab padre
    le asigne el espacio completo.
    """

    # Historial en memoria para detectar duplicados en la sesión
    seguimientos_guardados: list[dict] = []

    # ────────────────────────────────────────────────────────────
    # ALERTA REUTILIZABLE
    # Un solo AlertDialog para todos los mensajes de error/aviso.
    # Se registra en page.overlay la primera vez que se muestra.
    # ────────────────────────────────────────────────────────────
    _alerta_titulo = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
    _alerta_cuerpo = ft.Text("", size=14)

    def _cerrar_alerta(e=None):
        alerta_dlg.open = False
        page.update()

    alerta_dlg = ft.AlertDialog(
        modal=True,
        open=False,
        title=_alerta_titulo,
        content=_alerta_cuerpo,
        actions=[ft.TextButton("Aceptar", on_click=_cerrar_alerta)],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def mostrar_alerta(titulo: str, mensaje: str):
        _alerta_titulo.value = titulo
        _alerta_cuerpo.value = mensaje
        # page.overlay es el único mecanismo que funciona en TODAS
        # las versiones de Flet para mostrar diálogos flotantes.
        if alerta_dlg not in page.overlay:
            page.overlay.append(alerta_dlg)
        alerta_dlg.open = True
        page.update()

    # ────────────────────────────────────────────────────────────
    # FILTRO NUMÉRICO
    # Elimina en tiempo real cualquier carácter no numérico.
    # Se asigna mediante on_change a los campos de IDs.
    # ────────────────────────────────────────────────────────────
    def solo_numeros(e):
        campo = e.control
        limpio = re.sub(r'\D', '', campo.value or '')
        if campo.value != limpio:
            campo.value = limpio
            campo.update()

    # ────────────────────────────────────────────────────────────
    # CAMPOS DEL FORMULARIO
    # ────────────────────────────────────────────────────────────

    # id_asegurado e id_agente son FKs enteros.
    # Hasta conectar con BD, el usuario los ingresa manualmente.
    # solo_numeros garantiza que no se escriban letras.
    # TODO: reemplazar por Dropdown cargado desde la BD cuando
    #       los servicios estén listos.
    id_asegurado_input = ft.TextField(
        label="ID Asegurado*",
        hint_text="Número entero",
        expand=1,
        on_change=solo_numeros,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    id_agente_input = ft.TextField(
        label="ID Agente*",
        hint_text="Número entero",
        expand=1,
        on_change=solo_numeros,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # tipo_contacto: máx 20 caracteres → Dropdown de valores fijos
    tipo_contacto_dd = ft.Dropdown(
        label="Tipo de Contacto*",
        options=[
            ft.dropdown.Option("Llamada"),   # contacto telefónico
            ft.dropdown.Option("Correo"),    # correo electrónico
            ft.dropdown.Option("Visita"),    # visita presencial
        ],
        expand=1,
    )

    # resultado: máx 20 caracteres → Dropdown de valores fijos
    resultado_dd = ft.Dropdown(
        label="Resultado*",
        options=[
            ft.dropdown.Option("Exitoso"),   # objetivo cumplido
            ft.dropdown.Option("Pendiente"), # queda algo por resolver
            ft.dropdown.Option("Rechazado"), # asegurado no aceptó
        ],
        expand=1,
    )

    # fecha_hora: el usuario escribe en formato YYYY-MM-DD HH:MM.
    # Se valida con regex y luego se convierte a datetime.
    fecha_hora_input = ft.TextField(
        label="Fecha y Hora*",
        hint_text="YYYY-MM-DD HH:MM  (ej. 2026-04-12 14:30)",
        expand=1,
    )

    # observaciones: texto libre, máx 1000 caracteres.
    # max_lines controla la altura visible sin limitar el contenido.
    observaciones_input = ft.TextField(
        label="Observaciones*",
        hint_text="Describa el resultado del contacto (máx. 1000 caracteres)",
        multiline=True,
        max_lines=5,
        max_length=1000,
        expand=True,
    )

    # Lista visual de seguimientos guardados en la sesión
    historial_lista = ft.ListView(spacing=6, auto_scroll=True, height=200)

    # ────────────────────────────────────────────────────────────
    # HELPERS
    # ────────────────────────────────────────────────────────────
    def limpiar_formulario():
        for campo in [id_asegurado_input, id_agente_input,
                      fecha_hora_input, observaciones_input]:
            campo.value = ""
            campo.error_text = None
        tipo_contacto_dd.value = None
        tipo_contacto_dd.error_text = None
        resultado_dd.value = None
        resultado_dd.error_text = None

    def agregar_tarjeta(datos: dict):
        """Inserta una tarjeta al inicio del historial visible."""
        historial_lista.controls.insert(
            0,
            ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column([
                        ft.Row([
                            ft.Icon(ft.Icons.ACCESS_TIME, size=14, color=ft.Colors.GREY_500),
                            ft.Text(datos["fecha_hora"], size=12, color=ft.Colors.GREY_500),
                        ], spacing=4),
                        ft.Row([
                            ft.Text(
                                f"Asegurado #{datos['id_asegurado']}  ·  "
                                f"Agente #{datos['id_agente']}",
                                size=12,
                                color=ft.Colors.GREY_600,
                            ),
                        ]),
                        ft.Text(
                            f"{datos['tipo_contacto']}  ·  {datos['resultado']}",
                            weight=ft.FontWeight.BOLD,
                            size=14,
                        ),
                        ft.Text(datos["observaciones"], size=13),
                    ], spacing=4),
                )
            ),
        )

    def es_duplicado(datos: dict) -> bool:
        """
        Un seguimiento se considera duplicado cuando coinciden:
        id_asegurado, id_agente, tipo_contacto, resultado,
        fecha_hora y observaciones.
        Excluye campos autogenerados (id, created_at, deleted_at).
        """
        claves = ("id_asegurado", "id_agente", "tipo_contacto",
                  "resultado", "fecha_hora", "observaciones")
        for guardado in seguimientos_guardados:
            if all(guardado[k] == datos[k] for k in claves):
                return True
        return False

    def mostrar_snackbar(msg: str):
        snack = ft.SnackBar(ft.Text(msg))
        try:
            page.open(snack)
        except AttributeError:
            page.snack_bar = snack
            page.snack_bar.open = True
            page.update()

    # ────────────────────────────────────────────────────────────
    # VALIDACIÓN Y GUARDADO
    # ────────────────────────────────────────────────────────────
    def validar_y_guardar(e):
        es_valido = True
        campos_vacios: list[str] = []

        # — Campos de texto requeridos
        texto_requeridos = [
            (id_asegurado_input, "ID Asegurado"),
            (id_agente_input,    "ID Agente"),
            (fecha_hora_input,   "Fecha y Hora"),
            (observaciones_input,"Observaciones"),
        ]
        for campo, nombre in texto_requeridos:
            if not campo.value or not campo.value.strip():
                campo.error_text = "Obligatorio"
                es_valido = False
                campos_vacios.append(nombre)
            else:
                campo.error_text = None

        # — Dropdowns requeridos
        dd_requeridos = [
            (tipo_contacto_dd, "Tipo de Contacto"),
            (resultado_dd,     "Resultado"),
        ]
        for dd, nombre in dd_requeridos:
            if not dd.value:
                dd.error_text = "Obligatorio"
                es_valido = False
                campos_vacios.append(nombre)
            else:
                dd.error_text = None

        # — Si hay vacíos: alerta y detenemos antes de validaciones
        #   de formato para no confundir al usuario con dos errores.
        if campos_vacios:
            page.update()
            mostrar_alerta(
                "⚠️ Campos incompletos",
                "Por favor completa los siguientes campos:\n"
                + ", ".join(campos_vacios),
            )
            return

        # — Validar formato de fecha_hora: YYYY-MM-DD HH:MM
        fecha_str = fecha_hora_input.value.strip()
        if not _FECHA_PATTERN.match(fecha_str):
            fecha_hora_input.error_text = "Formato inválido. Usa YYYY-MM-DD HH:MM"
            es_valido = False
        else:
            fecha_hora_input.error_text = None
            # Verificar que sea una fecha real (ej. no 2026-02-30)
            try:
                datetime.strptime(fecha_str, "%Y-%m-%d %H:%M")
            except ValueError:
                fecha_hora_input.error_text = "Fecha inexistente"
                es_valido = False

        page.update()
        if not es_valido:
            return

        # — Construir diccionario alineado al modelo Seguimiento
        datos = {
            "id_asegurado":  int(id_asegurado_input.value.strip()),
            "id_agente":     int(id_agente_input.value.strip()),
            "tipo_contacto": tipo_contacto_dd.value,
            "observaciones": observaciones_input.value.strip(),
            "resultado":     resultado_dd.value,
            "fecha_hora":    fecha_str,
            # created_at y deleted_at los genera el ORM automáticamente
        }

        # — Verificar duplicado
        if es_duplicado(datos):
            mostrar_alerta(
                "⚠️ Seguimiento duplicado",
                "Ya existe un seguimiento registrado con exactamente\n"
                "los mismos datos en esta sesión.\n\n"
                "Verifica la información e intenta de nuevo.",
            )
            return

        # — Guardar
        seguimientos_guardados.append(datos)
        agregar_tarjeta(datos)

        # TODO: conectar con MySQL cuando el servicio esté listo:
        # from services.seguimiento_service import guardar_seguimiento
        # guardar_seguimiento(datos)
        print("Seguimiento para MySQL:", datos)

        limpiar_formulario()
        mostrar_snackbar("✅ Seguimiento guardado exitosamente.")
        page.update()

    btn_guardar = ft.ElevatedButton(
        "Guardar Seguimiento",
        on_click=validar_y_guardar,
        icon=ft.Icons.SAVE,
        style=ft.ButtonStyle(
            padding=ft.padding.symmetric(horizontal=24, vertical=14)
        ),
    )

    # ────────────────────────────────────────────────────────────
    # LAYOUT DEL FORMULARIO
    #
    # Fila 1: ID Asegurado(1) | ID Agente(1) | Tipo Contacto(1) | Resultado(1)
    # Fila 2: Fecha y Hora(1) — ocupa su propia fila
    # Fila 3: Observaciones  — campo expandible
    # ────────────────────────────────────────────────────────────
    formulario = ft.Column(
        controls=[
            # ── Encabezado ──────────────────────────────────────
            ft.Container(
                content=ft.Text(
                    "Registro de Seguimiento",
                    size=22,
                    weight=ft.FontWeight.BOLD,
                ),
                padding=ft.padding.only(bottom=4),
            ),
            ft.Divider(height=1),

            # ── Identificadores y clasificación ─────────────────
            ft.Text(
                "Datos del Seguimiento",
                size=16,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.BLUE_400,
            ),
            # Fila 1: IDs + dropdowns en una sola línea
            ft.Row(
                [id_asegurado_input,
                 id_agente_input,
                 tipo_contacto_dd,
                 resultado_dd],
                expand=True,
                spacing=12,
            ),

            # Fila 2: Fecha y hora (campo individual para mayor anchura)
            ft.Row(
                [fecha_hora_input],
                expand=True,
                spacing=12,
            ),

            ft.Container(height=4),

            # ── Observaciones ────────────────────────────────────
            ft.Text(
                "Observaciones",
                size=16,
                weight=ft.FontWeight.W_600,
                color=ft.Colors.BLUE_400,
            ),
            # expand=True en el TextField hace que crezca verticalmente
            ft.Row(
                [observaciones_input],
                expand=True,
                spacing=12,
            ),

            ft.Container(height=4),

            # ── Botón alineado a la derecha ──────────────────────
            ft.Row([btn_guardar], alignment=ft.MainAxisAlignment.END),

            ft.Divider(height=1),

            # ── Historial de la sesión ───────────────────────────
            ft.Text(
                "Seguimientos Guardados en esta sesión",
                size=13,
                weight=ft.FontWeight.W_500,
                color=ft.Colors.GREY_600,
            ),
            historial_lista,
        ],
        scroll=True,   # compatible con todas las versiones de Flet
        expand=True,
        spacing=10,
    )

    # ────────────────────────────────────────────────────────────
    # LAYOUT RAÍZ
    # ────────────────────────────────────────────────────────────
    return ft.Column(
        controls=[
            ft.Container(
                content=formulario,
                expand=True,
                padding=ft.padding.symmetric(horizontal=32, vertical=16),
            ),
        ],
        expand=True,
    )