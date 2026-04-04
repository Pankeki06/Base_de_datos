"""Validadores de datos para el negocio."""


def validar_rfc(rfc: str) -> bool:
    return len(rfc) > 0


def validar_correo(correo: str) -> bool:
    return "@" in correo
