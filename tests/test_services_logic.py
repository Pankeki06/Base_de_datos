"""
Comprehensive integration tests covering service business logic and controller
error-handling for all entities in the application.

Uses the same SQLite in-memory fixture pattern as test_database.py.
"""

from __future__ import annotations

from datetime import date, datetime

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

import repositories.agente_repository as agente_repo
import repositories.asegurado_repository as asegurado_repo
import repositories.beneficiario_repository as beneficiario_repo
import repositories.beneficio_repository as beneficio_repo
import repositories.poliza_repository as poliza_repo
import repositories.producto_poliza_repository as producto_poliza_repo
import repositories.producto_beneficio_repository as producto_beneficio_repo
import repositories.seguimiento_repository as seguimiento_repo
from controllers.agente_controller import AgenteController
from controllers.asegurado_controller import AseguradoController
from controllers.auth_controller import AuthController
from controllers.beneficiario_controller import BeneficiarioController
from controllers.beneficio_controller import BeneficioController
from controllers.poliza_controller import PolizaController
from controllers.producto_beneficio_controller import ProductoBeneficioController
from controllers.producto_poliza_controller import ProductoPolizaController
from controllers.seguimiento_controller import SeguimientoController


# ─── Fixture ──────────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def test_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    SQLModel.metadata.create_all(engine)

    def _create_session():
        return Session(engine)

    agente_repo.create_session = _create_session
    asegurado_repo.create_session = _create_session
    beneficiario_repo.create_session = _create_session
    beneficio_repo.create_session = _create_session
    poliza_repo.create_session = _create_session
    producto_poliza_repo.create_session = _create_session
    producto_beneficio_repo.create_session = _create_session
    seguimiento_repo.create_session = _create_session
    yield


# ─── Helpers ──────────────────────────────────────────────────────────────────

_SUFFIX = [0]


def _uid(tag: str) -> str:
    _SUFFIX[0] += 1
    return f"{tag}{_SUFFIX[0]}"


def _agente(tag: str = "AG"):
    uid = _uid(tag)
    r = AgenteController.create_agente({
        "clave_agente": f"clave-{uid}",
        "cedula": f"{uid[:10].ljust(10, '0')}",
        "nombre": "Test",
        "apellido_paterno": "Agente",
        "apellido_materno": "X",
        "correo": f"{uid}@test.com",
        "telefono": "5500000000",
        "rol": "agente",
        "password": "Test1234",
    })
    assert r["ok"], r.get("error")
    return r["data"]


def _asegurado(agente_id: int, tag: str = "AS"):
    _SUFFIX[0] += 1
    n = _SUFFIX[0]
    # Build a valid RFC: 4 uppercase letters + 6 digits + 3 alphanum
    L = "".join(chr(65 + (n // (26 ** i)) % 26) for i in range(4))
    rfc = L + "900101AA1"
    uid = f"{tag}{n}"
    r = AseguradoController.create_asegurado({
        "nombre": f"Aseg{uid}",
        "apellido_paterno": "Test",
        "apellido_materno": "Test",
        "rfc": rfc,
        "correo": f"aseg{n}@test.com",
        "celular": "5511112233",
        "calle": "Calle 1",
        "numero_exterior": "1",
        "colonia": "Col",
        "municipio": "Mun",
        "estado": "Edo",
        "codigo_postal": "00001",
        "id_agente_responsable": agente_id,
    })
    assert r["ok"], r.get("error")
    return r["data"]


def _producto(tag: str = "PROD"):
    uid = _uid(tag)
    r = ProductoPolizaController.create_producto({
        "nombre": f"Producto {uid}",
        "tipo_seguro": "Vida",
        "prima_base": 500.0,
        "descripcion": "Test",
    })
    assert r["ok"], r.get("error")
    return r["data"]


def _poliza(id_asegurado: int, id_producto: int, tag: str = "PZ"):
    uid = _uid(tag)
    r = PolizaController.create_poliza({
        "id_asegurado": id_asegurado,
        "id_producto": id_producto,
        "numero_poliza": f"POL-{uid}",
        "fecha_inicio": date(2026, 1, 1),
        "fecha_vencimiento": date(2027, 1, 1),
        "estatus": "activa",
        "prima_mensual": 500.0,
    })
    assert r["ok"], r.get("error")
    return r["data"]


def _plantilla(id_producto: int, tag: str = "PB"):
    uid = _uid(tag)
    r = ProductoBeneficioController.create_producto_beneficio({
        "id_producto": id_producto,
        "nombre_beneficio": f"Beneficio {uid}",
        "descripcion": "Cobertura test",
        "monto_cobertura": 100000.0,
        "incluido_base": True,
    })
    assert r["ok"], r.get("error")
    return r["data"]


# ══════════════════════════════════════════════════════════════════════════════
# AGENTE — controller edge cases
# ══════════════════════════════════════════════════════════════════════════════


class TestAgenteController:
    def test_get_by_id_existente(self):
        ag = _agente()
        r = AgenteController.get_agente_by_id(ag.id_agente)
        assert r["ok"] is True
        assert r["data"].id_agente == ag.id_agente

    def test_get_by_id_no_existente(self):
        r = AgenteController.get_agente_by_id(999999)
        assert r["ok"] is False
        assert "no encontrado" in r["error"].lower()

    def test_get_all_devuelve_lista(self):
        _agente()
        _agente()
        r = AgenteController.get_all_agentes()
        assert r["ok"] is True
        assert len(r["data"]) >= 2

    def test_delete_existente(self):
        ag = _agente()
        r = AgenteController.delete_agente(ag.id_agente)
        assert r["ok"] is True

    def test_delete_no_existente(self):
        r = AgenteController.delete_agente(999999)
        assert r["ok"] is False

    def test_create_rol_invalido_rechazado(self):
        r = AgenteController.create_agente({
            "clave_agente": "bad-rol",
            "cedula": "1111111111",
            "nombre": "X",
            "apellido_paterno": "Y",
            "apellido_materno": "Z",
            "correo": "x@test.com",
            "telefono": "5500000000",
            "rol": "superadmin",
            "password": "Test1234",
        })
        assert r["ok"] is False

    def test_create_clave_duplicada_rechazada(self):
        ag = _agente()
        r = AgenteController.create_agente({
            "clave_agente": ag.clave_agente,
            "cedula": "9999999999",
            "nombre": "Dup",
            "apellido_paterno": "A",
            "apellido_materno": "B",
            "correo": "unique@test.com",
            "telefono": "5500000000",
            "rol": "agente",
            "password": "Test1234",
        })
        assert r["ok"] is False
        assert "clave" in r["error"].lower()

    def test_create_correo_duplicado_rechazado(self):
        ag = _agente()
        r = AgenteController.create_agente({
            "clave_agente": "otra-clave",
            "cedula": "8888888888",
            "nombre": "Dup",
            "apellido_paterno": "A",
            "apellido_materno": "B",
            "correo": ag.correo,
            "telefono": "5500000000",
            "rol": "agente",
            "password": "Test1234",
        })
        assert r["ok"] is False
        assert "correo" in r["error"].lower()

    def test_update_correo_duplicado_rechazado(self):
        ag1 = _agente()
        ag2 = _agente()
        r = AgenteController.update_agente(ag2.id_agente, {"correo": ag1.correo})
        assert r["ok"] is False

    def test_update_password_debil_rechazado(self):
        ag = _agente()
        r = AgenteController.update_agente(ag.id_agente, {"password": "abc"})
        assert r["ok"] is False

    def test_update_no_existente(self):
        r = AgenteController.update_agente(999999, {"nombre": "Ghost"})
        assert r["ok"] is False

    def test_login_con_credenciales_correctas(self):
        ag = _agente()
        r = AuthController.login(ag.clave_agente, "Test1234")
        assert r["ok"] is True
        assert r["data"].id_agente == ag.id_agente

    def test_login_con_password_incorrecta(self):
        ag = _agente()
        r = AuthController.login(ag.clave_agente, "WrongPass99")
        assert r["ok"] is False

    def test_login_con_clave_inexistente(self):
        r = AuthController.login("no-existe", "Test1234")
        assert r["ok"] is False


# ══════════════════════════════════════════════════════════════════════════════
# ASEGURADO — controller edge cases
# ══════════════════════════════════════════════════════════════════════════════


class TestAseguradoController:
    def test_get_by_id_existente(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        r = AseguradoController.get_asegurado_by_id(a.id_asegurado)
        assert r["ok"] is True
        assert r["data"].id_asegurado == a.id_asegurado

    def test_get_by_id_no_existente(self):
        r = AseguradoController.get_asegurado_by_id(999999)
        assert r["ok"] is False

    def test_get_all_devuelve_lista(self):
        ag = _agente()
        _asegurado(ag.id_agente)
        _asegurado(ag.id_agente)
        r = AseguradoController.get_all_asegurados()
        assert r["ok"] is True
        assert len(r["data"]) >= 2

    def test_search_por_nombre(self):
        ag = _agente()
        a = _asegurado(ag.id_agente, "SEARCH")
        r = AseguradoController.search_asegurados(a.nombre)
        assert r["ok"] is True
        ids = [x.id_asegurado for x in r["data"]]
        assert a.id_asegurado in ids

    def test_get_by_agente(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        r = AseguradoController.get_asegurados_by_agente(ag.id_agente)
        assert r["ok"] is True
        ids = [x.id_asegurado for x in r["data"]]
        assert a.id_asegurado in ids

    def test_get_by_agente_sin_asegurados(self):
        ag = _agente()
        r = AseguradoController.get_asegurados_by_agente(ag.id_agente)
        assert r["ok"] is True
        assert r["data"] == []

    def test_create_celular_no_numerico_rechazado(self):
        ag = _agente()
        r = AseguradoController.create_asegurado({
            "nombre": "Test",
            "apellido_paterno": "A",
            "apellido_materno": "B",
            "rfc": "TSTA900101AA1",
            "correo": "test@test.com",
            "celular": "55-ABCD-12",
            "calle": "Calle",
            "numero_exterior": "1",
            "colonia": "Col",
            "municipio": "Mun",
            "estado": "Edo",
            "codigo_postal": "00001",
            "id_agente_responsable": ag.id_agente,
        })
        assert r["ok"] is False

    def test_create_agente_inexistente_rechazado(self):
        r = AseguradoController.create_asegurado({
            "nombre": "Test",
            "apellido_paterno": "A",
            "apellido_materno": "B",
            "rfc": "TSTB900101AA1",
            "calle": "Calle",
            "numero_exterior": "1",
            "colonia": "Col",
            "municipio": "Mun",
            "estado": "Edo",
            "codigo_postal": "00001",
            "id_agente_responsable": 999999,
        })
        assert r["ok"] is False

    def test_delete_existente(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        r = AseguradoController.delete_asegurado(a.id_asegurado)
        assert r["ok"] is True

    def test_delete_no_existente(self):
        r = AseguradoController.delete_asegurado(999999)
        assert r["ok"] is False

    def test_soft_delete_oculta_en_get_all(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        AseguradoController.delete_asegurado(a.id_asegurado)
        r = AseguradoController.get_all_asegurados()
        ids = [x.id_asegurado for x in r["data"]]
        assert a.id_asegurado not in ids


# ══════════════════════════════════════════════════════════════════════════════
# PRODUCTO POLIZA — controller edge cases
# ══════════════════════════════════════════════════════════════════════════════


class TestProductoPolizaController:
    def test_create_nombre_vacio_rechazado(self):
        r = ProductoPolizaController.create_producto({
            "nombre": "",
            "tipo_seguro": "Vida",
            "prima_base": 500.0,
        })
        assert r["ok"] is False

    def test_create_prima_cero_rechazado(self):
        r = ProductoPolizaController.create_producto({
            "nombre": "Test",
            "tipo_seguro": "Vida",
            "prima_base": 0.0,
        })
        assert r["ok"] is False

    def test_create_prima_negativa_rechazado(self):
        r = ProductoPolizaController.create_producto({
            "nombre": "Test",
            "tipo_seguro": "GMM",
            "prima_base": -100.0,
        })
        assert r["ok"] is False

    def test_get_by_id_no_existente(self):
        r = ProductoPolizaController.get_producto_by_id(999999)
        assert r["ok"] is False

    def test_get_activos_solo_devuelve_activos(self):
        prod = _producto()
        ProductoPolizaController.delete_producto(prod.id_producto)
        r = ProductoPolizaController.get_productos_activos()
        assert r["ok"] is True
        ids = [x.id_producto for x in r["data"]]
        assert prod.id_producto not in ids

    def test_update_prima_negativa_rechazado(self):
        prod = _producto()
        r = ProductoPolizaController.update_producto(prod.id_producto, {"prima_base": -1.0})
        assert r["ok"] is False

    def test_delete_existente(self):
        prod = _producto()
        r = ProductoPolizaController.delete_producto(prod.id_producto)
        assert r["ok"] is True


# ══════════════════════════════════════════════════════════════════════════════
# PRODUCTO BENEFICIO — controller edge cases
# ══════════════════════════════════════════════════════════════════════════════


class TestProductoBeneficioController:
    def test_create_base_no_requiere_costo_extra(self):
        prod = _producto()
        r = ProductoBeneficioController.create_producto_beneficio({
            "id_producto": prod.id_producto,
            "nombre_beneficio": "Cobertura base",
            "descripcion": "Desc",
            "monto_cobertura": 100000.0,
            "incluido_base": True,
        })
        assert r["ok"] is True
        assert r["data"].costo_extra is None

    def test_create_opcional_requiere_costo_extra_positivo(self):
        prod = _producto()
        r_sin_costo = ProductoBeneficioController.create_producto_beneficio({
            "id_producto": prod.id_producto,
            "nombre_beneficio": "Opcional",
            "descripcion": "Desc",
            "monto_cobertura": 50000.0,
            "incluido_base": False,
            "costo_extra": 0.0,
        })
        assert r_sin_costo["ok"] is False

    def test_create_opcional_con_costo_valido(self):
        prod = _producto()
        r = ProductoBeneficioController.create_producto_beneficio({
            "id_producto": prod.id_producto,
            "nombre_beneficio": "Dental",
            "descripcion": "Cobertura dental",
            "monto_cobertura": 20000.0,
            "incluido_base": False,
            "costo_extra": 200.0,
        })
        assert r["ok"] is True
        assert r["data"].costo_extra == 200.0

    def test_create_monto_cero_rechazado(self):
        prod = _producto()
        r = ProductoBeneficioController.create_producto_beneficio({
            "id_producto": prod.id_producto,
            "nombre_beneficio": "Test",
            "descripcion": "Desc",
            "monto_cobertura": 0.0,
            "incluido_base": True,
        })
        assert r["ok"] is False

    def test_update_incluido_base_limpia_costo_extra(self):
        prod = _producto()
        r = ProductoBeneficioController.create_producto_beneficio({
            "id_producto": prod.id_producto,
            "nombre_beneficio": "Opcional",
            "descripcion": "Desc",
            "monto_cobertura": 30000.0,
            "incluido_base": False,
            "costo_extra": 150.0,
        })
        assert r["ok"] is True
        pb_id = r["data"].id_producto_beneficio

        r_upd = ProductoBeneficioController.update_producto_beneficio(
            pb_id, {"incluido_base": True}
        )
        assert r_upd["ok"] is True
        assert r_upd["data"].costo_extra is None

    def test_get_beneficios_by_producto(self):
        prod = _producto()
        _plantilla(prod.id_producto)
        _plantilla(prod.id_producto)
        r = ProductoBeneficioController.get_beneficios_by_producto(prod.id_producto)
        assert r["ok"] is True
        assert len(r["data"]) == 2

    def test_delete_existente(self):
        prod = _producto()
        pb = _plantilla(prod.id_producto)
        r = ProductoBeneficioController.delete_producto_beneficio(pb.id_producto_beneficio)
        assert r["ok"] is True


# ══════════════════════════════════════════════════════════════════════════════
# POLIZA — controller edge cases
# ══════════════════════════════════════════════════════════════════════════════


class TestPolizaController:
    def test_get_by_id_existente(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        r = PolizaController.get_poliza_by_id(pol.id_poliza)
        assert r["ok"] is True
        assert r["data"].id_poliza == pol.id_poliza

    def test_get_by_id_no_existente(self):
        r = PolizaController.get_poliza_by_id(999999)
        assert r["ok"] is False

    def test_create_prima_cero_rechazado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        r = PolizaController.create_poliza({
            "id_asegurado": a.id_asegurado,
            "id_producto": prod.id_producto,
            "numero_poliza": "POL-ZERO",
            "fecha_inicio": date(2026, 1, 1),
            "fecha_vencimiento": date(2027, 1, 1),
            "estatus": "activa",
            "prima_mensual": 0.0,
        })
        assert r["ok"] is False

    def test_create_fechas_invertidas_rechazado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        r = PolizaController.create_poliza({
            "id_asegurado": a.id_asegurado,
            "id_producto": prod.id_producto,
            "numero_poliza": "POL-INV",
            "fecha_inicio": date(2027, 1, 1),
            "fecha_vencimiento": date(2026, 1, 1),
            "estatus": "activa",
            "prima_mensual": 500.0,
        })
        assert r["ok"] is False

    def test_create_estatus_invalido_rechazado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        r = PolizaController.create_poliza({
            "id_asegurado": a.id_asegurado,
            "id_producto": prod.id_producto,
            "numero_poliza": "POL-BAD-STATUS",
            "fecha_inicio": date(2026, 1, 1),
            "fecha_vencimiento": date(2027, 1, 1),
            "estatus": "pendiente",
            "prima_mensual": 500.0,
        })
        assert r["ok"] is False

    def test_create_poliza_duplicada_rechazada(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        _poliza(a.id_asegurado, prod.id_producto)
        r = PolizaController.create_poliza({
            "id_asegurado": a.id_asegurado,
            "id_producto": prod.id_producto,
            "numero_poliza": "POL-DUP-02",
            "fecha_inicio": date(2026, 2, 1),
            "fecha_vencimiento": date(2027, 2, 1),
            "estatus": "activa",
            "prima_mensual": 600.0,
        })
        assert r["ok"] is False
        assert "activa" in r["error"].lower() or "póliza" in r["error"].lower()

    def test_create_numero_poliza_duplicado_rechazado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod1 = _producto()
        prod2 = _producto()
        pol = _poliza(a.id_asegurado, prod1.id_producto)
        r = PolizaController.create_poliza({
            "id_asegurado": a.id_asegurado,
            "id_producto": prod2.id_producto,
            "numero_poliza": pol.numero_poliza,
            "fecha_inicio": date(2026, 1, 1),
            "fecha_vencimiento": date(2027, 1, 1),
            "estatus": "activa",
            "prima_mensual": 500.0,
        })
        assert r["ok"] is False

    def test_get_polizas_by_asegurado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        r = PolizaController.get_polizas_by_asegurado(a.id_asegurado)
        assert r["ok"] is True
        assert any(p.id_poliza == pol.id_poliza for p in r["data"])

    def test_add_participante_valido(self):
        ag = _agente()
        a1 = _asegurado(ag.id_agente)
        a2 = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a1.id_asegurado, prod.id_producto)
        r = PolizaController.add_participante_to_poliza({
            "id_poliza": pol.id_poliza,
            "id_asegurado": a2.id_asegurado,
            "tipo_participante": "conyuge",
        })
        assert r["ok"] is True

    def test_add_participante_tipo_invalido(self):
        ag = _agente()
        a1 = _asegurado(ag.id_agente)
        a2 = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a1.id_asegurado, prod.id_producto)
        r = PolizaController.add_participante_to_poliza({
            "id_poliza": pol.id_poliza,
            "id_asegurado": a2.id_asegurado,
            "tipo_participante": "amigo",
        })
        assert r["ok"] is False

    def test_get_participantes_by_poliza(self):
        ag = _agente()
        a1 = _asegurado(ag.id_agente)
        a2 = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a1.id_asegurado, prod.id_producto)
        PolizaController.add_participante_to_poliza({
            "id_poliza": pol.id_poliza,
            "id_asegurado": a2.id_asegurado,
            "tipo_participante": "conyuge",
        })
        r = PolizaController.get_participantes_by_poliza(pol.id_poliza)
        assert r["ok"] is True
        ids = [p["id_asegurado"] for p in r["data"]]
        assert a1.id_asegurado in ids
        assert a2.id_asegurado in ids

    def test_get_available_polizas_for_participante(self):
        ag = _agente()
        a1 = _asegurado(ag.id_agente)
        a2 = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a1.id_asegurado, prod.id_producto)
        r = PolizaController.get_available_polizas_for_participante(a2.id_asegurado)
        assert r["ok"] is True
        ids = [p.id_poliza for p in r["data"]]
        assert pol.id_poliza in ids

    def test_update_cambio_estatus(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        r = PolizaController.update_poliza(pol.id_poliza, {"estatus": "cancelada"})
        assert r["ok"] is True
        assert r["data"].estatus == "cancelada"

    def test_delete_y_soft_delete(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        PolizaController.delete_poliza(pol.id_poliza)
        r = PolizaController.get_poliza_by_id(pol.id_poliza)
        assert r["ok"] is False


# ══════════════════════════════════════════════════════════════════════════════
# BENEFICIO — controller edge cases
# ══════════════════════════════════════════════════════════════════════════════


class TestBeneficioController:
    def test_get_by_id_no_existente(self):
        r = BeneficioController.get_beneficio_by_id(999999)
        assert r["ok"] is False

    def test_create_sin_plantilla_es_rechazado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        r = BeneficioController.create_beneficio({
            "id_poliza": pol.id_poliza,
            "id_producto_beneficio": None,
        })
        assert r["ok"] is False

    def test_create_poliza_inexistente_rechazado(self):
        r = BeneficioController.create_beneficio({
            "id_poliza": 999999,
            "id_producto_beneficio": 1,
        })
        assert r["ok"] is False

    def test_create_plantilla_diferente_producto_rechazado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod1 = _producto()
        prod2 = _producto()
        pol = _poliza(a.id_asegurado, prod1.id_producto)
        pb_otro = _plantilla(prod2.id_producto)
        r = BeneficioController.create_beneficio({
            "id_poliza": pol.id_poliza,
            "id_producto_beneficio": pb_otro.id_producto_beneficio,
        })
        assert r["ok"] is False

    def test_get_beneficios_by_poliza(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        pb = _plantilla(prod.id_producto)
        BeneficioController.create_beneficio({
            "id_poliza": pol.id_poliza,
            "id_producto_beneficio": pb.id_producto_beneficio,
        })
        r = BeneficioController.get_beneficios_by_poliza(pol.id_poliza)
        assert r["ok"] is True
        assert len(r["data"]) >= 1

    def test_update_monto_override_valido(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        pb = _plantilla(prod.id_producto)
        r_create = BeneficioController.create_beneficio({
            "id_poliza": pol.id_poliza,
            "id_producto_beneficio": pb.id_producto_beneficio,
        })
        b_id = r_create["data"].id_beneficio
        r = BeneficioController.update_beneficio(b_id, {"monto_override": 200000.0})
        assert r["ok"] is True

    def test_delete_existente(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        pb = _plantilla(prod.id_producto)
        r_create = BeneficioController.create_beneficio({
            "id_poliza": pol.id_poliza,
            "id_producto_beneficio": pb.id_producto_beneficio,
        })
        r = BeneficioController.delete_beneficio(r_create["data"].id_beneficio)
        assert r["ok"] is True


# ══════════════════════════════════════════════════════════════════════════════
# BENEFICIARIO — controller edge cases
# ══════════════════════════════════════════════════════════════════════════════


class TestBeneficiarioController:
    def test_get_by_id_no_existente(self):
        r = BeneficiarioController.get_beneficiario_by_id(999999)
        assert r["ok"] is False

    def test_create_valido(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        r = BeneficiarioController.create_beneficiario({
            "id_asegurado": a.id_asegurado,
            "id_poliza": pol.id_poliza,
            "nombre_completo": "Maria Test",
            "parentesco": "Conyuge",
            "porcentaje_participacion": 60.0,
            "telefono": "5511112233",
        })
        assert r["ok"] is True

    def test_create_poliza_de_otro_asegurado_rechazado(self):
        ag = _agente()
        a1 = _asegurado(ag.id_agente)
        a2 = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a1.id_asegurado, prod.id_producto)
        r = BeneficiarioController.create_beneficiario({
            "id_asegurado": a2.id_asegurado,
            "id_poliza": pol.id_poliza,
            "nombre_completo": "Alguien",
            "parentesco": "Hijo",
            "porcentaje_participacion": 50.0,
        })
        assert r["ok"] is False

    def test_create_supera_100_porcentaje_rechazado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        BeneficiarioController.create_beneficiario({
            "id_asegurado": a.id_asegurado,
            "id_poliza": pol.id_poliza,
            "nombre_completo": "Ben 1",
            "parentesco": "Hijo",
            "porcentaje_participacion": 70.0,
        })
        r = BeneficiarioController.create_beneficiario({
            "id_asegurado": a.id_asegurado,
            "id_poliza": pol.id_poliza,
            "nombre_completo": "Ben 2",
            "parentesco": "Hijo",
            "porcentaje_participacion": 50.0,
        })
        assert r["ok"] is False
        assert "100" in r["error"]

    def test_get_beneficiarios_by_asegurado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        BeneficiarioController.create_beneficiario({
            "id_asegurado": a.id_asegurado,
            "id_poliza": pol.id_poliza,
            "nombre_completo": "Ben test",
            "parentesco": "Hijo",
            "porcentaje_participacion": 40.0,
        })
        r = BeneficiarioController.get_beneficiarios_by_asegurado(a.id_asegurado)
        assert r["ok"] is True
        assert len(r["data"]) == 1

    def test_update_porcentaje_valido(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        r_c = BeneficiarioController.create_beneficiario({
            "id_asegurado": a.id_asegurado,
            "id_poliza": pol.id_poliza,
            "nombre_completo": "Ben upd",
            "parentesco": "Conyuge",
            "porcentaje_participacion": 50.0,
        })
        r = BeneficiarioController.update_beneficiario(
            r_c["data"].id_beneficiario, {"porcentaje_participacion": 80.0}
        )
        assert r["ok"] is True
        assert r["data"].porcentaje_participacion == 80.0

    def test_delete_existente(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        prod = _producto()
        pol = _poliza(a.id_asegurado, prod.id_producto)
        r_c = BeneficiarioController.create_beneficiario({
            "id_asegurado": a.id_asegurado,
            "id_poliza": pol.id_poliza,
            "nombre_completo": "Ben del",
            "parentesco": "Hijo",
            "porcentaje_participacion": 30.0,
        })
        r = BeneficiarioController.delete_beneficiario(r_c["data"].id_beneficiario)
        assert r["ok"] is True


# ══════════════════════════════════════════════════════════════════════════════
# SEGUIMIENTO — controller edge cases
# ══════════════════════════════════════════════════════════════════════════════


class TestSeguimientoController:
    def _base_payload(self, id_asegurado, id_agente):
        return {
            "id_asegurado": id_asegurado,
            "id_agente": id_agente,
            "tipo_contacto": "llamada",
            "observaciones": "Recordatorio de pago",
            "resultado": "pendiente",
            "fecha_hora": datetime(2026, 5, 1, 10, 0, 0),
        }

    def test_create_valido(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        r = SeguimientoController.create_seguimiento(self._base_payload(a.id_asegurado, ag.id_agente))
        assert r["ok"] is True

    def test_get_by_id_existente(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        r_c = SeguimientoController.create_seguimiento(self._base_payload(a.id_asegurado, ag.id_agente))
        r = SeguimientoController.get_seguimiento_by_id(r_c["data"].id_seguimiento)
        assert r["ok"] is True

    def test_get_by_id_no_existente(self):
        r = SeguimientoController.get_seguimiento_by_id(999999)
        assert r["ok"] is False

    def test_create_tipo_contacto_invalido(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        payload = self._base_payload(a.id_asegurado, ag.id_agente)
        payload["tipo_contacto"] = "correo_invalido"
        r = SeguimientoController.create_seguimiento(payload)
        assert r["ok"] is False

    def test_create_resultado_invalido(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        payload = self._base_payload(a.id_asegurado, ag.id_agente)
        payload["resultado"] = "incompleto"
        r = SeguimientoController.create_seguimiento(payload)
        assert r["ok"] is False

    def test_create_observaciones_vacias_rechazado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        payload = self._base_payload(a.id_asegurado, ag.id_agente)
        payload["observaciones"] = ""
        r = SeguimientoController.create_seguimiento(payload)
        assert r["ok"] is False

    def test_create_asegurado_inexistente_rechazado(self):
        ag = _agente()
        r = SeguimientoController.create_seguimiento({
            "id_asegurado": 999999,
            "id_agente": ag.id_agente,
            "tipo_contacto": "visita",
            "observaciones": "Test",
            "resultado": "resuelto",
            "fecha_hora": datetime(2026, 1, 1, 9, 0, 0),
        })
        assert r["ok"] is False
        assert "asegurado" in r["error"].lower()

    def test_create_agente_inexistente_rechazado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        r = SeguimientoController.create_seguimiento({
            "id_asegurado": a.id_asegurado,
            "id_agente": 999999,
            "tipo_contacto": "mensaje",
            "observaciones": "Test",
            "resultado": "sin_respuesta",
            "fecha_hora": datetime(2026, 1, 1, 9, 0, 0),
        })
        assert r["ok"] is False
        assert "agente" in r["error"].lower()

    def test_get_by_asegurado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        SeguimientoController.create_seguimiento(self._base_payload(a.id_asegurado, ag.id_agente))
        SeguimientoController.create_seguimiento({
            **self._base_payload(a.id_asegurado, ag.id_agente),
            "tipo_contacto": "mensaje",
        })
        r = SeguimientoController.get_seguimientos_by_asegurado(a.id_asegurado)
        assert r["ok"] is True
        assert len(r["data"]) == 2

    def test_update_resultado(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        r_c = SeguimientoController.create_seguimiento(self._base_payload(a.id_asegurado, ag.id_agente))
        r = SeguimientoController.update_seguimiento(r_c["data"].id_seguimiento, {"resultado": "resuelto"})
        assert r["ok"] is True
        assert r["data"].resultado == "resuelto"

    def test_update_tipo_invalido(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        r_c = SeguimientoController.create_seguimiento(self._base_payload(a.id_asegurado, ag.id_agente))
        r = SeguimientoController.update_seguimiento(
            r_c["data"].id_seguimiento, {"tipo_contacto": "humo"}
        )
        assert r["ok"] is False

    def test_delete_existente(self):
        ag = _agente()
        a = _asegurado(ag.id_agente)
        r_c = SeguimientoController.create_seguimiento(self._base_payload(a.id_asegurado, ag.id_agente))
        r = SeguimientoController.delete_seguimiento(r_c["data"].id_seguimiento)
        assert r["ok"] is True

    def test_delete_no_existente(self):
        r = SeguimientoController.delete_seguimiento(999999)
        assert r["ok"] is False
