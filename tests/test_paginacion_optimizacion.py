from datetime import date

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

import repositories.agente_repository as agente_repo
import repositories.asegurado_repository as asegurado_repo
import repositories.poliza_repository as poliza_repo
import repositories.producto_poliza_repository as producto_poliza_repo
from controllers.asegurado_controller import AseguradoController
from controllers.poliza_controller import PolizaController
from controllers.agente_controller import AgenteController
from controllers.producto_poliza_controller import ProductoPolizaController


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
    poliza_repo.create_session = _create_session
    producto_poliza_repo.create_session = _create_session
    yield


@pytest.fixture
def agente():
    result = AgenteController.create_agente({
        "clave_agente": "admin-paginacion",
        "cedula": "9999999999",
        "nombre": "Paginacion",
        "apellido_paterno": "Test",
        "apellido_materno": "Test",
        "correo": "paginacion@test.com",
        "telefono": "5550000000",
        "rol": "admin",
        "password": "Test1234",
    })
    assert result["ok"] is True
    return result["data"]


@pytest.fixture
def producto():
    result = ProductoPolizaController.create_producto({
        "nombre": "Producto Paginacion",
        "descripcion": "Producto para test de paginacion",
        "tipo_seguro": "Vida",
        "prima_base": 500.0,
    })
    assert result["ok"] is True
    return result["data"]


def _crear_asegurado(agente_id: int, nombre: str, rfc: str):
    return AseguradoController.create_asegurado({
        "nombre": nombre,
        "apellido_paterno": "Test",
        "apellido_materno": "Paginacion",
        "rfc": rfc,
        "correo": f"{nombre.lower().replace(' ', '')}@test.com",
        "celular": "5512345678",
        "calle": "Calle Test",
        "numero_exterior": "10",
        "colonia": "Centro",
        "municipio": "Monterrey",
        "estado": "Nuevo Leon",
        "codigo_postal": "64000",
        "id_agente_responsable": agente_id,
    })


def _crear_poliza(asegurado_id: int, producto_id: int, numero: str):
    return PolizaController.create_poliza({
        "id_asegurado": asegurado_id,
        "id_producto": producto_id,
        "numero_poliza": numero,
        "fecha_inicio": date(2026, 1, 1),
        "fecha_vencimiento": date(2027, 1, 1),
        "estatus": "activa",
        "prima_mensual": 500.0,
    })


def test_paginacion_asegurados_sin_titulares(agente, producto):
    """Sin pólizas, no debe haber titulares."""
    for i in range(5):
        res = _crear_asegurado(agente.id_agente, f"SinPoliza{i}", f"SIPL{i:02d}0101AA1")
        assert res["ok"] is True

    result = AseguradoController.get_titulares_by_agente_page(
        agente.id_agente, page=1, page_size=20
    )
    assert result["ok"] is True
    assert result["data"] == []
    assert result["total"] == 0


def test_paginacion_titulares_devuelve_solo_con_poliza(agente, producto):
    """Solo asegurados con pólizas deben aparecer como titulares."""
    asegurados = []
    for i in range(10):
        res = _crear_asegurado(agente.id_agente, f"Titular{i}", f"TITL{i:02d}0101AA1")
        assert res["ok"] is True
        asegurados.append(res["data"])

    # Crear pólizas solo para los primeros 5
    for i in range(5):
        res = _crear_poliza(asegurados[i].id_asegurado, producto.id_producto, f"PZ-TITL-{i:03d}")
        assert res["ok"] is True

    result = AseguradoController.get_titulares_by_agente_page(
        agente.id_agente, page=1, page_size=20
    )
    assert result["ok"] is True
    assert result["total"] == 5
    assert len(result["data"]) == 5
    # Todos deben tener pólizas
    for a in result["data"]:
        assert a.id_asegurado in {asegurados[i].id_asegurado for i in range(5)}


def test_paginacion_page_size(agente, producto):
    """Verificar que page_size respeta el límite."""
    asegurados = []
    for i in range(25):
        res = _crear_asegurado(agente.id_agente, f"Page{i}", f"PAGE{i:02d}0101AA1")
        assert res["ok"] is True
        asegurados.append(res["data"])
        res_pol = _crear_poliza(res["data"].id_asegurado, producto.id_producto, f"PZ-PAGE-{i:03d}")
        assert res_pol["ok"] is True

    result_p1 = AseguradoController.get_titulares_by_agente_page(
        agente.id_agente, page=1, page_size=10
    )
    assert result_p1["ok"] is True
    assert result_p1["total"] == 25
    assert len(result_p1["data"]) == 10

    result_p2 = AseguradoController.get_titulares_by_agente_page(
        agente.id_agente, page=2, page_size=10
    )
    assert result_p2["ok"] is True
    assert len(result_p2["data"]) == 10

    result_p3 = AseguradoController.get_titulares_by_agente_page(
        agente.id_agente, page=3, page_size=10
    )
    assert result_p3["ok"] is True
    assert len(result_p3["data"]) == 5


def test_paginacion_page_2_distinta_de_page_1(agente, producto):
    """Las páginas deben devolver conjuntos distintos."""
    asegurados = []
    for i in range(15):
        res = _crear_asegurado(agente.id_agente, f"Page{i}", f"PAGE{i:02d}0101AA1")
        assert res["ok"] is True
        asegurados.append(res["data"])
        res_pol = _crear_poliza(res["data"].id_asegurado, producto.id_producto, f"PZ-PAGE-{i:03d}")
        assert res_pol["ok"] is True

    result_p1 = AseguradoController.get_titulares_by_agente_page(
        agente.id_agente, page=1, page_size=10
    )
    result_p2 = AseguradoController.get_titulares_by_agente_page(
        agente.id_agente, page=2, page_size=10
    )

    ids_p1 = {a.id_asegurado for a in result_p1["data"]}
    ids_p2 = {a.id_asegurado for a in result_p2["data"]}
    assert ids_p1.isdisjoint(ids_p2)


def test_polizas_batch_por_ids(agente, producto):
    """PolizaController.get_polizas_by_asegurado_ids debe cargar múltiples pólizas en batch."""
    asegurados = []
    for i in range(5):
        res = _crear_asegurado(agente.id_agente, f"Batch{i}", f"BACH{i:02d}0101AA1")
        assert res["ok"] is True
        asegurados.append(res["data"])
        res_pol = _crear_poliza(res["data"].id_asegurado, producto.id_producto, f"PZ-BACH-{i:03d}")
        assert res_pol["ok"] is True

    ids = [a.id_asegurado for a in asegurados]
    result = PolizaController.get_polizas_by_asegurado_ids(ids)
    assert result["ok"] is True
    assert len(result["data"]) == 5
    for p in result["data"]:
        assert p.id_asegurado in ids


def test_participaciones_batch_por_ids(agente, producto):
    """PolizaController.get_participaciones_by_asegurado_ids debe devolver participaciones de todos."""
    asegurados = []
    for i in range(5):
        res = _crear_asegurado(agente.id_agente, f"Part{i}", f"PART{i:02d}0101AA1")
        assert res["ok"] is True
        asegurados.append(res["data"])
        res_pol = _crear_poliza(res["data"].id_asegurado, producto.id_producto, f"PZ-PART-{i:03d}")
        assert res_pol["ok"] is True

    ids = [a.id_asegurado for a in asegurados]
    result = PolizaController.get_participaciones_by_asegurado_ids(ids)
    assert result["ok"] is True
    # Debe haber 5 participaciones como titulares
    assert len(result["data"]) == 5
    for part in result["data"]:
        assert part["id_asegurado"] in ids
        assert part["tipo_asegurado"] == "titular"


def test_participantes_batch_por_poliza_ids(agente, producto):
    """PolizaController.get_participantes_by_poliza_ids debe devolver participantes de todas las pólizas."""
    asegurados = []
    for i in range(3):
        res = _crear_asegurado(agente.id_agente, f"PartPol{i}", f"PTPL{i:02d}0101AA1")
        assert res["ok"] is True
        asegurados.append(res["data"])
        res_pol = _crear_poliza(res["data"].id_asegurado, producto.id_producto, f"PZ-PTPL-{i:03d}")
        assert res_pol["ok"] is True

    polizas_result = PolizaController.get_polizas_by_asegurado_ids([a.id_asegurado for a in asegurados])
    ids_poliza = [p.id_poliza for p in polizas_result["data"]]

    result = PolizaController.get_participantes_by_poliza_ids(ids_poliza)
    assert result["ok"] is True
    # 3 pólizas, cada una con al menos el titular
    participantes_por_poliza = {}
    for p in result["data"]:
        pid = p["id_poliza"]
        participantes_por_poliza.setdefault(pid, []).append(p)
    assert len(participantes_por_poliza) == 3
    for pid, parts in participantes_por_poliza.items():
        assert any(p["tipo_asegurado"] == "titular" for p in parts)
