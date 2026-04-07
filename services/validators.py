"""Validadores de datos para el negocio."""

import re
from datetime import date

EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")
RFC_PATTERN = re.compile(r"^[A-Z&Ñ]{3,4}\d{6}[A-Z0-9]{3}$")


def validar_requerido(valor: str, campo: str) -> None:
    if not valor or not str(valor).strip():
        raise ValueError(f"El campo '{campo}' es obligatorio.")


def validar_correo(correo: str | None) -> None:
    if correo and not EMAIL_PATTERN.match(correo):
        raise ValueError("El correo no tiene un formato válido.")


def validar_rfc(rfc: str) -> None:
    validar_requerido(rfc, "rfc")
    if not RFC_PATTERN.match(rfc.upper()):
        raise ValueError("El RFC no tiene un formato válido.")


def validar_porcentaje(porcentaje: float) -> None:
    if porcentaje <= 0 or porcentaje > 100:
        raise ValueError("El porcentaje de participación debe estar entre 0 y 100.")


def validar_monto_positivo(monto: float, campo: str) -> None:
    if monto <= 0:
        raise ValueError(f"El campo '{campo}' debe ser mayor a 0.")


def validar_rango_fechas(fecha_inicio: date, fecha_vencimiento: date) -> None:
    if fecha_vencimiento <= fecha_inicio:
        raise ValueError("La fecha de vencimiento debe ser mayor que la fecha de inicio.")
