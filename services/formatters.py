"""Formateadores de texto y fechas."""

from datetime import date, datetime


def formatear_fecha(fecha) -> str:
    """Convierte fecha a string en formato dd/mm/yyyy. Acepta date, datetime o str ISO."""
    if isinstance(fecha, (date, datetime)):
        return fecha.strftime("%d/%m/%Y")
    if isinstance(fecha, str) and fecha:
        for fmt in ("%Y-%m-%d", "%Y-%m-%dT%H:%M:%S", "%d/%m/%Y"):
            try:
                return datetime.strptime(fecha, fmt).strftime("%d/%m/%Y")
            except ValueError:
                continue
    return str(fecha) if fecha is not None else ""


def formatear_nombre(nombre: str) -> str:
    return nombre.title()
