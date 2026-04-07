from datetime import date, datetime

import pytest
from sqlalchemy.pool import StaticPool
from sqlmodel import SQLModel, Session, create_engine

import repositories.agente_repository as agente_repo
import repositories.asegurado_repository as asegurado_repo
import repositories.beneficiario_repository as beneficiario_repo
import repositories.beneficio_repository as beneficio_repo
import repositories.poliza_repository as poliza_repo
import repositories.seguimiento_repository as seguimiento_repo
import repositories.sesion_repository as sesion_repo
from controllers.agente_controller import AgenteController
from controllers.asegurado_controller import AseguradoController
from controllers.auth_controller import AuthController
from controllers.beneficiario_controller import BeneficiarioController
from controllers.beneficio_controller import BeneficioController
from controllers.poliza_controller import PolizaController
from controllers.seguimiento_controller import SeguimientoController
from controllers.sesion_controller import SesionController


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
    seguimiento_repo.create_session = _create_session
    sesion_repo.create_session = _create_session
    yield


def test_flujo_backend_completo():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "admin1",
            "nombre": "Alex",
            "apellido_paterno": "Diaz",
            "apellido_materno": "Lopez",
            "correo": "alex@test.com",
            "telefono": "5551112233",
            "rol": "admin",
            "password": "1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    login_ok = AuthController.login("admin1", "1234")
    assert login_ok["ok"] is True
    assert login_ok["data"].id_agente == agente.id_agente

    login_fail = AuthController.login("admin1", "wrong")
    assert login_fail["ok"] is False

    asegurado_result = AseguradoController.create_asegurado(
        {
            "nombre": "Carlos",
            "apellido_paterno": "Ramirez",
            "apellido_materno": "Soto",
            "rfc": "ABCD900101EF1",
            "correo": "carlos@test.com",
            "celular": "5512345678",
            "calle": "Av Principal",
            "numero_exterior": "10",
            "numero_interior": "2",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert asegurado_result["ok"] is True
    asegurado = asegurado_result["data"]

    poliza_result = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "numero_poliza": "PZ-0001",
            "tipo_seguro": "Vida",
            "fecha_inicio": date(2026, 1, 1),
            "fecha_vencimiento": date(2027, 1, 1),
            "estatus": "activa",
            "prima_mensual": 1200.50,
        }
    )
    assert poliza_result["ok"] is True
    poliza = poliza_result["data"]

    beneficio_result = BeneficioController.create_beneficio(
        {
            "id_poliza": poliza.id_poliza,
            "nombre_beneficio": "Cobertura hospitalaria",
            "descripcion": "Cobertura por internamiento",
            "monto_cobertura": 200000.0,
        }
    )
    assert beneficio_result["ok"] is True
    beneficio = beneficio_result["data"]

    beneficiario_result = BeneficiarioController.create_beneficiario(
        {
            "id_asegurado": asegurado.id_asegurado,
            "nombre_completo": "Maria Soto",
            "parentesco": "Conyuge",
            "porcentaje_participacion": 60.0,
            "telefono": "5511111111",
        }
    )
    assert beneficiario_result["ok"] is True
    beneficiario = beneficiario_result["data"]

    seguimiento_result = SeguimientoController.create_seguimiento(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_agente": agente.id_agente,
            "tipo_contacto": "llamada",
            "observaciones": "Recordatorio de pago",
            "resultado": "pendiente",
            "fecha_hora": datetime(2026, 4, 1, 12, 30, 0),
        }
    )
    assert seguimiento_result["ok"] is True
    seguimiento = seguimiento_result["data"]

    sesion_result = SesionController.create_sesion({"id_agente": agente.id_agente})
    assert sesion_result["ok"] is True
    sesion = sesion_result["data"]

    assert AgenteController.update_agente(agente.id_agente, {"nombre": "Alexis"})["ok"] is True
    assert AseguradoController.update_asegurado(asegurado.id_asegurado, {"municipio": "Guadalupe"})["ok"] is True
    assert PolizaController.update_poliza(poliza.id_poliza, {"estatus": "vencida"})["ok"] is True
    assert BeneficioController.update_beneficio(beneficio.id_beneficio, {"monto_cobertura": 250000.0})["ok"] is True
    assert (
        BeneficiarioController.update_beneficiario(
            beneficiario.id_beneficiario, {"porcentaje_participacion": 70.0}
        )["ok"]
        is True
    )
    assert SeguimientoController.update_seguimiento(seguimiento.id_seguimiento, {"resultado": "resuelto"})["ok"] is True
    assert SesionController.update_sesion(sesion.id_sesion, {"fin_sesion": datetime.now()})["ok"] is True

    assert AgenteController.delete_agente(agente.id_agente)["ok"] is True
    assert AseguradoController.delete_asegurado(asegurado.id_asegurado)["ok"] is True
    assert PolizaController.delete_poliza(poliza.id_poliza)["ok"] is True
    assert BeneficioController.delete_beneficio(beneficio.id_beneficio)["ok"] is True
    assert BeneficiarioController.delete_beneficiario(beneficiario.id_beneficiario)["ok"] is True
    assert SeguimientoController.delete_seguimiento(seguimiento.id_seguimiento)["ok"] is True
    assert SesionController.delete_sesion(sesion.id_sesion)["ok"] is True


def test_validaciones_basicas():
    duplicado = AgenteController.create_agente(
        {
            "clave_agente": "ag001",
            "nombre": "Uno",
            "apellido_paterno": "A",
            "apellido_materno": "B",
            "correo": "uno@test.com",
            "rol": "agente",
            "password": "1234",
        }
    )
    assert duplicado["ok"] is True

    repetido = AgenteController.create_agente(
        {
            "clave_agente": "ag001",
            "nombre": "Dos",
            "apellido_paterno": "C",
            "apellido_materno": "D",
            "correo": "dos@test.com",
            "rol": "agente",
            "password": "1234",
        }
    )
    assert repetido["ok"] is False

    rfc_invalido = AseguradoController.create_asegurado(
        {
            "nombre": "Error",
            "apellido_paterno": "RFC",
            "apellido_materno": "Bad",
            "rfc": "123",
            "correo": "ok@test.com",
            "calle": "x",
            "numero_exterior": "1",
            "colonia": "x",
            "municipio": "x",
            "estado": "x",
            "codigo_postal": "00000",
        }
    )
    assert rfc_invalido["ok"] is False