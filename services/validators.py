"""Validadores de datos para el negocio."""

import re
from datetime import date

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
RFC_PATTERN = re.compile(r"^[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}$")
PHONE_PATTERN = re.compile(r"^\d+$")


def validar_requerido(valor: str, campo: str) -> None:
    if not valor or not str(valor).strip():
        raise ValueError(f"El campo '{campo}' es obligatorio.")


def validar_correo(correo: str | None) -> None:
    if correo and not EMAIL_PATTERN.match(correo):
        raise ValueError("El correo no tiene un formato válido.")


def validar_telefono(
    telefono: str | None,
    campo: str = "telefono",
    longitud_min: int = 10,
    longitud_max: int = 20,
) -> None:
    if telefono is None or not str(telefono).strip():
        return

    valor = str(telefono).strip()
    if not PHONE_PATTERN.match(valor):
        raise ValueError(f"El campo '{campo}' solo debe contener dígitos.")

    if not longitud_min <= len(valor) <= longitud_max:
        if longitud_min == longitud_max:
            raise ValueError(
                f"El campo '{campo}' debe contener exactamente {longitud_min} dígitos."
            )
        raise ValueError(
            f"El campo '{campo}' debe contener entre {longitud_min} y {longitud_max} dígitos."
        )


def validar_rfc(rfc: str) -> None:
    validar_requerido(rfc, "rfc")
    if not RFC_PATTERN.match(rfc.upper()):
        raise ValueError("El RFC no tiene un formato válido.")


def validar_porcentaje(porcentaje: float) -> None:
    if porcentaje <= 0 or porcentaje > 100:
        raise ValueError("El porcentaje de participación debe estar entre 0 y 100.")


def validar_password(password: str) -> None:
    if not password or len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    if not any(c.isupper() for c in password):
        raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
    if not any(c.isdigit() for c in password):
        raise ValueError("La contraseña debe contener al menos un dígito.")


def validar_enum(valor: str, campo: str, opciones_validas: set[str]) -> None:
    validar_requerido(valor, campo)
    if str(valor).strip().lower() not in opciones_validas:
        opciones = ", ".join(sorted(opciones_validas))
        raise ValueError(f"El campo '{campo}' debe ser uno de: {opciones}.")


def validar_monto_positivo(monto: float, campo: str) -> None:
    if monto <= 0:
        raise ValueError(f"El campo '{campo}' debe ser mayor a 0.")


def validar_rango_fechas(fecha_inicio: date, fecha_vencimiento: date) -> None:
    if fecha_vencimiento <= fecha_inicio:
        raise ValueError("La fecha de vencimiento debe ser mayor que la fecha de inicio.")
