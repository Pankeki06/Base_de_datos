"""Unit tests for all validator functions in services/validators.py."""

import pytest
from datetime import date

from services.validators import (
    validar_requerido,
    validar_correo,
    validar_telefono,
    validar_rfc,
    validar_porcentaje,
    validar_password,
    validar_enum,
    validar_monto_positivo,
    validar_rango_fechas,
)


# ──────────────────────────────────────────────────────────────────────────────
# validar_requerido
# ──────────────────────────────────────────────────────────────────────────────


def test_requerido_acepta_valor_valido():
    validar_requerido("hola", "campo")  # no debe lanzar


def test_requerido_rechaza_cadena_vacia():
    with pytest.raises(ValueError, match="campo"):
        validar_requerido("", "campo")


def test_requerido_rechaza_solo_espacios():
    with pytest.raises(ValueError):
        validar_requerido("   ", "campo")


def test_requerido_rechaza_none():
    with pytest.raises(ValueError):
        validar_requerido(None, "campo")


def test_requerido_incluye_nombre_de_campo_en_mensaje():
    with pytest.raises(ValueError, match="mi_campo"):
        validar_requerido("", "mi_campo")


# ──────────────────────────────────────────────────────────────────────────────
# validar_correo
# ──────────────────────────────────────────────────────────────────────────────


def test_correo_valido_no_lanza():
    validar_correo("usuario@dominio.com")


def test_correo_none_permitido():
    validar_correo(None)  # campo opcional


def test_correo_sin_arroba_es_invalido():
    with pytest.raises(ValueError, match="correo"):
        validar_correo("usuariosindominio.com")


def test_correo_sin_dominio_es_invalido():
    with pytest.raises(ValueError):
        validar_correo("usuario@")


def test_correo_sin_tld_es_invalido():
    with pytest.raises(ValueError):
        validar_correo("usuario@dominio")


def test_correo_con_espacios_es_invalido():
    with pytest.raises(ValueError):
        validar_correo("usuario @dominio.com")


def test_correo_cadena_vacia_no_lanza():
    # cadena vacía equivale a "no proporcionado" — no debe lanzar
    validar_correo("")


# ──────────────────────────────────────────────────────────────────────────────
# validar_telefono
# ──────────────────────────────────────────────────────────────────────────────


def test_telefono_valido_10_digitos():
    validar_telefono("5512345678")


def test_telefono_none_es_opcional():
    validar_telefono(None)


def test_telefono_vacio_es_opcional():
    validar_telefono("")


def test_telefono_con_letras_es_invalido():
    with pytest.raises(ValueError, match="dígitos"):
        validar_telefono("551234ABCD")


def test_telefono_con_guion_es_invalido():
    with pytest.raises(ValueError):
        validar_telefono("551-234-5678")


def test_telefono_muy_corto_es_invalido():
    with pytest.raises(ValueError, match="entre"):
        validar_telefono("12345", longitud_min=10, longitud_max=15)


def test_telefono_muy_largo_es_invalido():
    with pytest.raises(ValueError):
        validar_telefono("123456789012345678901", longitud_min=10, longitud_max=20)


def test_telefono_longitud_exacta_igual_min():
    validar_telefono("5512345678", longitud_min=10, longitud_max=10)


def test_telefono_longitud_exacta_mensaje_correcto():
    with pytest.raises(ValueError, match="exactamente 10"):
        validar_telefono("12345", longitud_min=10, longitud_max=10)


# ──────────────────────────────────────────────────────────────────────────────
# validar_rfc
# ──────────────────────────────────────────────────────────────────────────────


def test_rfc_valido_4_letras():
    validar_rfc("ABCD900101AA1")


def test_rfc_valido_3_letras():
    validar_rfc("ABC900101AA1")


def test_rfc_vacio_es_invalido():
    with pytest.raises(ValueError):
        validar_rfc("")


def test_rfc_demasiado_corto():
    with pytest.raises(ValueError, match="formato"):
        validar_rfc("AB9001")


def test_rfc_con_minusculas_es_aceptado_normalizado():
    # The validator normalizes to uppercase before checking; lowercase is accepted
    validar_rfc("abcd900101aa1")  # must not raise


def test_rfc_con_caracteres_invalidos():
    with pytest.raises(ValueError):
        validar_rfc("AB@D900101AA1")


def test_rfc_numeros_en_inicio_es_invalido():
    with pytest.raises(ValueError):
        validar_rfc("1234900101AA1")


# ──────────────────────────────────────────────────────────────────────────────
# validar_porcentaje
# ──────────────────────────────────────────────────────────────────────────────


def test_porcentaje_100_es_valido():
    validar_porcentaje(100.0)


def test_porcentaje_0_01_es_valido():
    validar_porcentaje(0.01)


def test_porcentaje_cero_es_invalido():
    with pytest.raises(ValueError, match="entre 0 y 100"):
        validar_porcentaje(0.0)


def test_porcentaje_negativo_es_invalido():
    with pytest.raises(ValueError):
        validar_porcentaje(-10.0)


def test_porcentaje_mayor_100_es_invalido():
    with pytest.raises(ValueError):
        validar_porcentaje(100.1)


# ──────────────────────────────────────────────────────────────────────────────
# validar_password
# ──────────────────────────────────────────────────────────────────────────────


def test_password_valida():
    validar_password("Contraseña1")


def test_password_minima_8_caracteres():
    validar_password("Abcde12!")  # exactamente 8


def test_password_muy_corta_es_invalida():
    with pytest.raises(ValueError, match="8 caracteres"):
        validar_password("Abc12")


def test_password_sin_mayuscula_es_invalida():
    with pytest.raises(ValueError, match="mayúscula"):
        validar_password("password1")


def test_password_sin_digito_es_invalida():
    with pytest.raises(ValueError, match="dígito"):
        validar_password("PasswordSinNumero")


def test_password_none_es_invalida():
    with pytest.raises((ValueError, AttributeError)):
        validar_password(None)


def test_password_vacia_es_invalida():
    with pytest.raises(ValueError):
        validar_password("")


# ──────────────────────────────────────────────────────────────────────────────
# validar_enum
# ──────────────────────────────────────────────────────────────────────────────


def test_enum_valor_valido():
    validar_enum("activa", "estatus", {"activa", "cancelada", "vencida"})


def test_enum_valor_invalido():
    with pytest.raises(ValueError, match="estatus"):
        validar_enum("inexistente", "estatus", {"activa", "cancelada"})


def test_enum_vacio_es_invalido():
    with pytest.raises(ValueError):
        validar_enum("", "tipo", {"a", "b"})


def test_enum_mensaje_incluye_opciones():
    with pytest.raises(ValueError, match="activa"):
        validar_enum("otro", "campo", {"activa"})


# ──────────────────────────────────────────────────────────────────────────────
# validar_monto_positivo
# ──────────────────────────────────────────────────────────────────────────────


def test_monto_positivo_valido():
    validar_monto_positivo(100.0, "prima")


def test_monto_cero_es_invalido():
    with pytest.raises(ValueError, match="prima"):
        validar_monto_positivo(0.0, "prima")


def test_monto_negativo_es_invalido():
    with pytest.raises(ValueError):
        validar_monto_positivo(-50.0, "monto")


def test_monto_muy_pequeño_positivo_es_valido():
    validar_monto_positivo(0.01, "monto")


# ──────────────────────────────────────────────────────────────────────────────
# validar_rango_fechas
# ──────────────────────────────────────────────────────────────────────────────


def test_rango_fechas_valido():
    validar_rango_fechas(date(2026, 1, 1), date(2027, 1, 1))


def test_rango_fechas_misma_fecha_es_invalido():
    with pytest.raises(ValueError):
        validar_rango_fechas(date(2026, 6, 1), date(2026, 6, 1))


def test_rango_fechas_invertido_es_invalido():
    with pytest.raises(ValueError):
        validar_rango_fechas(date(2027, 1, 1), date(2026, 1, 1))


def test_rango_fechas_diferencia_un_dia_es_valido():
    validar_rango_fechas(date(2026, 6, 1), date(2026, 6, 2))
