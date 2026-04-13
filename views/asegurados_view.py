import flet as ft
import re
from datetime import datetime

from services.validators import RFC_PATTERN

# Correo restringido a los dominios permitidos
CORREO_PERMITIDO = re.compile(
    r'^[a-zA-Z0-9._%+\-]+@(gmail\.com|outlook\.com|hotmail\.com)$',
    re.IGNORECASE,
)

def create_asegurados_view(page: ft.Page) -> ft.Column:

    # Lista en memoria de asegurados ya guardados (para detección de duplicados)
    asegurados_guardados: list[dict] = []

    # ─────────────────────────────────────────────────────────
    # ALERTA REUTILIZABLE
    # Un solo AlertDialog que se reutiliza para cualquier mensaje,
    # cambiando su título y contenido antes de abrirlo.
    # ─────────────────────────────────────────────────────────
    _alerta_titulo  = ft.Text("", size=16, weight=ft.FontWeight.BOLD)
    _alerta_cuerpo  = ft.Text("", size=14)

    def _cerrar_alerta(e=None):
        alerta_dlg.open = False
        page.update()

    alerta_dlg = ft.AlertDialog(
        modal=True,
        open=False,
        title=_alerta_titulo,
        content=_alerta_cuerpo,
        actions=[
            ft.TextButton("Aceptar", on_click=_cerrar_alerta)
        ],
        actions_alignment=ft.MainAxisAlignment.END,
    )

    def mostrar_alerta(titulo: str, mensaje: str):
        _alerta_titulo.value = titulo
        _alerta_cuerpo.value = mensaje
        if alerta_dlg not in page.overlay:
            page.overlay.append(alerta_dlg)
        alerta_dlg.open = True
        page.update()

    # ─────────────────────────────────────────────────────────
    # FILTRO NUMÉRICO
    # on_change que elimina cualquier carácter no numérico.
    # Se asigna a celular, num_ext, num_int y cp.
    # ─────────────────────────────────────────────────────────
    def solo_numeros(e):
        campo = e.control
        valor_limpio = re.sub(r'\D', '', campo.value or '')
        if campo.value != valor_limpio:
            campo.value = valor_limpio
            campo.update()

    # ─────────────────────────────────────────────────────────
    # CAMPOS DEL FORMULARIO
    # ─────────────────────────────────────────────────────────

    # — Datos personales
    nombre_input     = ft.TextField(label="Nombre(s)*",        expand=1)
    ap_paterno_input = ft.TextField(label="Apellido Paterno*", expand=1)
    ap_materno_input = ft.TextField(label="Apellido Materno*", expand=1)

    rfc_input    = ft.TextField(label="RFC*",               hint_text="Ej. VECJ880326XXX", max_length=13, expand=1)
    correo_input = ft.TextField(
        label="Correo Electrónico*",
        hint_text="usuario@gmail.com / outlook.com / hotmail.com",
        expand=2,
    )
    celular_input = ft.TextField(
        label="Celular*",
        hint_text="10 dígitos",
        max_length=10,
        expand=1,
        on_change=solo_numeros,     # solo números
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # — Dirección
    calle_input     = ft.TextField(label="Calle*",     expand=3)
    num_ext_input   = ft.TextField(
        label="No. Ext*",
        expand=1,
        on_change=solo_numeros,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    num_int_input   = ft.TextField(
        label="No. Int",
        expand=1,
        on_change=solo_numeros,
        keyboard_type=ft.KeyboardType.NUMBER,
    )
    colonia_input   = ft.TextField(label="Colonia*",   expand=1)
    municipio_input = ft.TextField(label="Municipio*", expand=1)
    estado_input    = ft.TextField(label="Estado*",    expand=1)
    cp_input        = ft.TextField(
        label="C.P.*",
        max_length=5,
        expand=1,
        on_change=solo_numeros,
        keyboard_type=ft.KeyboardType.NUMBER,
    )

    # Lista visual de asegurados guardados
    asegurados_lista = ft.ListView(spacing=6, auto_scroll=True, height=170)

    # ─────────────────────────────────────────────────────────
    # HELPERS
    # ─────────────────────────────────────────────────────────
    def limpiar_formulario():
        for campo in [
            nombre_input, ap_paterno_input, ap_materno_input,
            rfc_input, correo_input, celular_input,
            calle_input, num_ext_input, num_int_input,
            colonia_input, municipio_input, estado_input, cp_input,
        ]:
            campo.value = ""
            campo.error_text = None

    def agregar_tarjeta(datos: dict):
        nombre_completo = (
            f"{datos['nombre']} {datos['ap_paterno']} {datos['ap_materno']}"
        )
        asegurados_lista.controls.insert(
            0,
            ft.Card(
                content=ft.Container(
                    padding=8,
                    content=ft.Column([
                        ft.Text(nombre_completo, weight=ft.FontWeight.BOLD, size=13),
                        ft.Text(
                            f"RFC: {datos['rfc']}  |  {datos['correo']}",
                            size=12,
                            color=ft.Colors.GREY_600,
                        ),
                    ], spacing=2),
                )
            ),
        )

    def es_duplicado(datos: dict) -> bool:
        """
        Compara el RFC del nuevo asegurado contra los ya guardados.
        El RFC es único por persona, por lo que es suficiente para
        detectar duplicados sin comparar todos los campos.
        """
        rfc_nuevo = datos["rfc"].upper()
        return any(a["rfc"].upper() == rfc_nuevo for a in asegurados_guardados)

    def mostrar_snackbar(msg: str):
        snack = ft.SnackBar(ft.Text(msg))
        try:
            page.open(snack)
        except AttributeError:
            page.snack_bar = snack
            page.snack_bar.open = True
            page.update()

    # ─────────────────────────────────────────────────────────
    # VALIDACIÓN Y GUARDADO
    # ─────────────────────────────────────────────────────────
    def validar_y_guardar(e):
        es_valido = True

        # — Campos de texto requeridos
        requeridos = [
            (nombre_input,    "Nombre"),
            (ap_paterno_input,"Apellido Paterno"),
            (ap_materno_input,"Apellido Materno"),
            (correo_input,    "Correo"),
            (celular_input,   "Celular"),
            (calle_input,     "Calle"),
            (num_ext_input,   "No. Ext"),
            (colonia_input,   "Colonia"),
            (municipio_input, "Municipio"),
            (estado_input,    "Estado"),
            (cp_input,        "C.P."),
        ]
        campos_vacios = []
        for campo, nombre in requeridos:
            if not campo.value or not campo.value.strip():
                campo.error_text = "Obligatorio"
                es_valido = False
                campos_vacios.append(nombre)
            else:
                campo.error_text = None

        # — RFC
        rfc = rfc_input.value.strip().upper() if rfc_input.value else ""
        if not rfc:
            rfc_input.error_text = "Obligatorio"
            es_valido = False
            campos_vacios.append("RFC")
        elif not RFC_PATTERN.match(rfc):
            rfc_input.error_text = "Formato inválido (ej. VECJ880326XXX)"
            es_valido = False
        else:
            rfc_input.error_text = None

        # — Si hay campos vacíos, mostramos alerta y detenemos
        if campos_vacios:
            page.update()
            faltantes = ", ".join(campos_vacios)
            mostrar_alerta(
                "⚠️ Campos incompletos",
                f"Por favor completa los siguientes campos:\n{faltantes}",
            )
            return

        # — Correo: solo gmail.com, outlook.com o hotmail.com
        correo_val = correo_input.value.strip()
        if not CORREO_PERMITIDO.match(correo_val):
            correo_input.error_text = "Debe ser @gmail.com, @outlook.com o @hotmail.com"
            es_valido = False

        page.update()
        if not es_valido:
            return

        # — Construir diccionario
        datos = {
            "nombre":     nombre_input.value.strip(),
            "ap_paterno": ap_paterno_input.value.strip(),
            "ap_materno": ap_materno_input.value.strip(),
            "rfc":        rfc,
            "correo":     correo_val,
            "celular":    celular_input.value.strip(),
            "calle":      calle_input.value.strip(),
            "num_ext":    num_ext_input.value.strip(),
            "num_int":    num_int_input.value.strip() if num_int_input.value else "",
            "colonia":    colonia_input.value.strip(),
            "municipio":  municipio_input.value.strip(),
            "estado":     estado_input.value.strip(),
            "cp":         cp_input.value.strip(),
        }

        # — Verificar duplicado por RFC
        if es_duplicado(datos):
            mostrar_alerta(
                "⚠️ Asegurado duplicado",
                f"Ya existe un asegurado registrado con el RFC «{rfc}».\n"
                "Verifica los datos e intenta de nuevo.",
            )
            return

        # — Guardar
        asegurados_guardados.append(datos)
        agregar_tarjeta(datos)

        # TODO: conectar con MySQL
        # from services.asegurados_service import guardar_asegurado
        # guardar_asegurado(datos)
        print("Datos para MySQL:", datos)

        limpiar_formulario()
        mostrar_snackbar("✅ Asegurado guardado exitosamente.")
        page.update()

    btn_guardar = ft.ElevatedButton(
        "Guardar Asegurado",
        on_click=validar_y_guardar,
        icon=ft.Icons.SAVE,
        style=ft.ButtonStyle(padding=ft.padding.symmetric(horizontal=24, vertical=14)),
    )

    # ─────────────────────────────────────────────────────────
    # LAYOUT DEL FORMULARIO — ocupa el ancho completo
    #
    # Fila 1: Nombre(2) | Ap. Paterno(1) | Ap. Materno(1)
    # Fila 2: RFC(1)    | Correo(2)      | Celular(1)
    # Fila 3: Calle(3)  | No.Ext(1)      | No.Int(1)
    # Fila 4: Colonia(1)| Municipio(1)   | Estado(1) | C.P.(1)
    # ─────────────────────────────────────────────────────────
    formulario = ft.Column(
        controls=[
            # ── Encabezado ──────────────────────────────────
            ft.Container(
                content=ft.Text("Gestión de Asegurados", size=22, weight=ft.FontWeight.BOLD),
                padding=ft.padding.only(bottom=4),
            ),
            ft.Divider(height=1),

            # ── Datos personales ────────────────────────────
            ft.Text("Datos Personales", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_400),
            ft.Row(
                [nombre_input,
                 ap_paterno_input,
                 ap_materno_input],
                expand=True, spacing=12,
            ),
            ft.Row(
                [rfc_input,
                 correo_input,
                 celular_input],
                expand=True, spacing=12,
            ),

            ft.Container(height=8),   # separador visual

            # ── Dirección ───────────────────────────────────
            ft.Text("Dirección", size=16, weight=ft.FontWeight.W_600, color=ft.Colors.BLUE_400),
            ft.Row(
                [calle_input,
                 num_ext_input,
                 num_int_input],
                expand=True, spacing=12,
            ),
            ft.Row(
                [colonia_input,
                 municipio_input,
                 estado_input,
                 cp_input],
                expand=True, spacing=12,
            ),

            ft.Container(height=4),

            # ── Botón guardar ────────────────────────────────
            ft.Row([btn_guardar], alignment=ft.MainAxisAlignment.END),

            ft.Divider(height=1),

            # ── Lista de asegurados guardados ────────────────
            ft.Text(
                "Asegurados Guardados en esta sesión",
                size=13,
                weight=ft.FontWeight.W_500,
                color=ft.Colors.GREY_600,
            ),
            asegurados_lista,
        ],
        scroll=True,
        expand=True,
        spacing=10,
    )

    # ─────────────────────────────────────────────────────────
    # LAYOUT RAÍZ
    # ─────────────────────────────────────────────────────────
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