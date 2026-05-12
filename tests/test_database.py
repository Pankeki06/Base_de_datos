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
import repositories.seguimiento_contacto_repository as seguimiento_contacto_repo
import repositories.seguimiento_repository as seguimiento_repo
from controllers.agente_controller import AgenteController
from controllers.asegurado_controller import AseguradoController
from controllers.auth_controller import AuthController
from controllers.beneficiario_controller import BeneficiarioController
from controllers.beneficio_controller import BeneficioController
from controllers.poliza_controller import PolizaController
from controllers.producto_beneficio_controller import ProductoBeneficioController
from controllers.producto_poliza_controller import ProductoPolizaController
from controllers.seguimiento_contacto_controller import SeguimientoContactoController
from controllers.seguimiento_controller import SeguimientoController
from models.agente import Agente


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
    seguimiento_contacto_repo.create_session = _create_session
    seguimiento_repo.create_session = _create_session
    yield


def test_flujo_backend_completo():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "admin1",
            "cedula": "0000000001",
            "nombre": "Alex",
            "apellido_paterno": "Diaz",
            "apellido_materno": "Lopez",
            "correo": "alex@test.com",
            "telefono": "5551112233",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    login_ok = AuthController.login("admin1", "Test1234")
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

    producto_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Vida Básico",
            "descripcion": "Plan de vida de prueba",
            "tipo_seguro": "Vida",
            "prima_base": 650.0,
        }
    )
    assert producto_result["ok"] is True
    producto = producto_result["data"]

    poliza_result = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_producto": producto.id_producto,
            "numero_poliza": "PZ-0001",
            "fecha_inicio": date(2026, 1, 1),
            "fecha_vencimiento": date(2027, 1, 1),
            "estatus": "activa",
            "prima_mensual": 1200.50,
        }
    )
    assert poliza_result["ok"] is True
    poliza = poliza_result["data"]

    plantilla_result = ProductoBeneficioController.create_producto_beneficio(
        {
            "id_producto": producto.id_producto,
            "nombre_beneficio": "Cobertura hospitalaria",
            "descripcion": "Cobertura por internamiento",
            "monto_cobertura": 200000.0,
            "incluido_base": True,
        }
    )
    assert plantilla_result["ok"] is True
    plantilla = plantilla_result["data"]

    beneficio_result = BeneficioController.create_beneficio(
        {
            "id_poliza": poliza.id_poliza,
            "id_producto_beneficio": plantilla.id_producto_beneficio,
        }
    )
    assert beneficio_result["ok"] is True
    beneficio = beneficio_result["data"]
    assert beneficio.costo_aplicado == 0.0

    beneficiario_result = BeneficiarioController.create_beneficiario(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_poliza": poliza.id_poliza,
            "nombre_completo": "Maria Soto",
            "parentesco": "Conyuge",
            "porcentaje_participacion": 60.0,
            "telefono": "5511111111",
        }
    )
    assert beneficiario_result["ok"] is True
    beneficiario = beneficiario_result["data"]
    assert beneficiario.id_poliza == poliza.id_poliza

    seguimiento_result = SeguimientoController.create_seguimiento(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_agente": agente.id_agente,
            "folio": "FOL-001",
            "asunto": "Recordatorio de pago",
        }
    )
    assert seguimiento_result["ok"] is True
    seguimiento = seguimiento_result["data"]

    assert AgenteController.update_agente(agente.id_agente, {"nombre": "Alexis"})["ok"] is True
    assert AseguradoController.update_asegurado(asegurado.id_asegurado, {"municipio": "Guadalupe"})["ok"] is True
    assert PolizaController.update_poliza(poliza.id_poliza, {"estatus": "vencida"})["ok"] is True
    assert BeneficioController.update_beneficio(beneficio.id_beneficio, {"monto_override": 250000.0})["ok"] is True
    assert (
        BeneficiarioController.update_beneficiario(
            beneficiario.id_beneficiario, {"porcentaje_participacion": 70.0}
        )["ok"]
        is True
    )
    assert SeguimientoController.update_seguimiento(seguimiento.id_seguimiento, {"asunto": "Nuevo asunto"})["ok"] is True

    assert BeneficiarioController.delete_beneficiario(beneficiario.id_beneficiario)["ok"] is True
    assert BeneficioController.delete_beneficio(beneficio.id_beneficio)["ok"] is True
    assert SeguimientoController.delete_seguimiento(seguimiento.id_seguimiento)["ok"] is True
    assert PolizaController.delete_poliza(poliza.id_poliza)["ok"] is True
    assert AseguradoController.delete_asegurado(asegurado.id_asegurado)["ok"] is True
    assert AgenteController.delete_agente(agente.id_agente)["ok"] is True


def test_create_poliza_devuelve_id_accesible_fuera_de_sesion():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "ag-poliza-detached",
            "cedula": "0000000199",
            "nombre": "Poliza",
            "apellido_paterno": "Detached",
            "apellido_materno": "Test",
            "correo": "poliza-detached@test.com",
            "telefono": "5551110099",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    asegurado_result = AseguradoController.create_asegurado(
        {
            "nombre": "Laura",
            "apellido_paterno": "Sesion",
            "apellido_materno": "Prueba",
            "rfc": "SEPL900101AA2",
            "correo": "laura.sesion@test.com",
            "celular": "5512345600",
            "calle": "Calle Uno",
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

    producto_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto Detached",
            "descripcion": "Producto para probar retorno de poliza",
            "tipo_seguro": "Vida",
            "prima_base": 500.0,
        }
    )
    assert producto_result["ok"] is True
    producto = producto_result["data"]

    poliza_result = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_producto": producto.id_producto,
            "numero_poliza": "PZ-DETACHED-01",
            "fecha_inicio": date(2026, 1, 1),
            "fecha_vencimiento": date(2027, 1, 1),
            "estatus": "activa",
            "prima_mensual": 500.0,
        }
    )
    assert poliza_result["ok"] is True

    poliza = poliza_result["data"]
    assert poliza.id_poliza is not None

    fetched_poliza = PolizaController.get_poliza_by_id(poliza.id_poliza)
    assert fetched_poliza["ok"] is True
    assert fetched_poliza["data"].numero_poliza == "PZ-DETACHED-01"


def test_create_poliza_rechaza_producto_activo_duplicado_para_el_mismo_asegurado():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "ag-poliza-duplicada",
            "cedula": "0000000205",
            "nombre": "Poliza",
            "apellido_paterno": "Duplicada",
            "apellido_materno": "Test",
            "correo": "poliza-duplicada@test.com",
            "telefono": "5551110205",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    asegurado_result = AseguradoController.create_asegurado(
        {
            "nombre": "Helena",
            "apellido_paterno": "Cobertura",
            "apellido_materno": "Unica",
            "rfc": "HECU900101AA1",
            "correo": "helena.cobertura@test.com",
            "celular": "5512345605",
            "calle": "Calle Uno",
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

    producto_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto Unico",
            "descripcion": "Producto para evitar duplicados activos",
            "tipo_seguro": "Vida",
            "prima_base": 700.0,
        }
    )
    assert producto_result["ok"] is True
    producto = producto_result["data"]

    primera_poliza = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_producto": producto.id_producto,
            "numero_poliza": "PZ-DUP-01",
            "fecha_inicio": date(2026, 2, 1),
            "fecha_vencimiento": date(2027, 2, 1),
            "estatus": "activa",
            "prima_mensual": 700.0,
        }
    )
    assert primera_poliza["ok"] is True

    poliza_duplicada = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_producto": producto.id_producto,
            "numero_poliza": "PZ-DUP-02",
            "fecha_inicio": date(2026, 3, 1),
            "fecha_vencimiento": date(2027, 3, 1),
            "estatus": "activa",
            "prima_mensual": 710.0,
        }
    )
    assert poliza_duplicada["ok"] is False
    assert "ya cuenta con una póliza activa de este producto" in poliza_duplicada["error"]


def test_create_poliza_copia_solo_beneficios_base_activos():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "ag-poliza-beneficios",
            "cedula": "0000000200",
            "nombre": "Beneficios",
            "apellido_paterno": "Base",
            "apellido_materno": "Test",
            "correo": "poliza-beneficios@test.com",
            "telefono": "5551110100",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    asegurado_result = AseguradoController.create_asegurado(
        {
            "nombre": "Roberto",
            "apellido_paterno": "Poliza",
            "apellido_materno": "Beneficios",
            "rfc": "POBR900101AA1",
            "correo": "roberto.poliza@test.com",
            "celular": "5512345610",
            "calle": "Calle Dos",
            "numero_exterior": "20",
            "numero_interior": "4",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert asegurado_result["ok"] is True
    asegurado = asegurado_result["data"]

    producto_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto con Beneficios Base",
            "descripcion": "Producto para probar copia automatica de beneficios",
            "tipo_seguro": "Gastos Medicos",
            "prima_base": 1200.0,
        }
    )
    assert producto_result["ok"] is True
    producto = producto_result["data"]

    beneficio_base_result = ProductoBeneficioController.create_producto_beneficio(
        {
            "id_producto": producto.id_producto,
            "nombre_beneficio": "Hospitalizacion base",
            "descripcion": "Cobertura incluida desde el producto",
            "monto_cobertura": 250000.0,
            "incluido_base": True,
        }
    )
    assert beneficio_base_result["ok"] is True
    beneficio_base = beneficio_base_result["data"]

    beneficio_opcional_result = ProductoBeneficioController.create_producto_beneficio(
        {
            "id_producto": producto.id_producto,
            "nombre_beneficio": "Dental opcional",
            "descripcion": "Cobertura opcional no incluida por defecto",
            "monto_cobertura": 15000.0,
            "incluido_base": False,
        }
    )
    assert beneficio_opcional_result["ok"] is True

    beneficio_desactivable_result = ProductoBeneficioController.create_producto_beneficio(
        {
            "id_producto": producto.id_producto,
            "nombre_beneficio": "Vision desactivada",
            "descripcion": "Cobertura base retirada antes de emitir la poliza",
            "monto_cobertura": 10000.0,
            "incluido_base": True,
        }
    )
    assert beneficio_desactivable_result["ok"] is True

    delete_result = ProductoBeneficioController.delete_producto_beneficio(
        beneficio_desactivable_result["data"].id_producto_beneficio
    )
    assert delete_result["ok"] is True

    poliza_result = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_producto": producto.id_producto,
            "numero_poliza": "PZ-BENEF-01",
            "fecha_inicio": date(2026, 2, 1),
            "fecha_vencimiento": date(2027, 2, 1),
            "estatus": "activa",
            "prima_mensual": 1200.0,
        }
    )
    assert poliza_result["ok"] is True
    poliza = poliza_result["data"]

    beneficios_result = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
    assert beneficios_result["ok"] is True

    beneficios = beneficios_result["data"]
    assert len(beneficios) == 1
    assert beneficios[0].id_producto_beneficio == beneficio_base.id_producto_beneficio
    assert beneficios[0].costo_aplicado == 0.0
    assert beneficios[0].id_asegurado is None
    assert beneficios[0].monto_override is None


def test_create_poliza_respeta_beneficios_seleccionados_del_catalogo():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "ag-poliza-beneficios-select",
            "cedula": "0000000201",
            "nombre": "Beneficios",
            "apellido_paterno": "Seleccion",
            "apellido_materno": "Test",
            "correo": "poliza-beneficios-select@test.com",
            "telefono": "5551110101",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    asegurado_result = AseguradoController.create_asegurado(
        {
            "nombre": "Carla",
            "apellido_paterno": "Poliza",
            "apellido_materno": "Seleccion",
            "rfc": "POSE900101AA1",
            "correo": "carla.poliza@test.com",
            "celular": "5512345611",
            "calle": "Calle Tres",
            "numero_exterior": "30",
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

    producto_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto con Seleccion",
            "descripcion": "Producto para probar seleccion previa de beneficios",
            "tipo_seguro": "Vida",
            "prima_base": 850.0,
        }
    )
    assert producto_result["ok"] is True
    producto = producto_result["data"]

    beneficio_base_result = ProductoBeneficioController.create_producto_beneficio(
        {
            "id_producto": producto.id_producto,
            "nombre_beneficio": "Hospitalizacion base",
            "descripcion": "Cobertura base del producto",
            "monto_cobertura": 150000.0,
            "incluido_base": True,
        }
    )
    assert beneficio_base_result["ok"] is True

    beneficio_opcional_result = ProductoBeneficioController.create_producto_beneficio(
        {
            "id_producto": producto.id_producto,
            "nombre_beneficio": "Dental opcional",
            "descripcion": "Cobertura opcional seleccionable",
            "monto_cobertura": 18000.0,
            "costo_extra": 135.0,
            "incluido_base": False,
        }
    )
    assert beneficio_opcional_result["ok"] is True
    beneficio_opcional = beneficio_opcional_result["data"]
    assert beneficio_opcional.costo_extra == 135.0

    poliza_result = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_producto": producto.id_producto,
            "numero_poliza": "PZ-BENEF-SEL-01",
            "fecha_inicio": date(2026, 3, 1),
            "fecha_vencimiento": date(2027, 3, 1),
            "estatus": "activa",
            "prima_mensual": 850.0,
            "beneficios_seleccionados": [beneficio_opcional.id_producto_beneficio],
        }
    )
    assert poliza_result["ok"] is True
    poliza = poliza_result["data"]

    beneficios_result = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
    assert beneficios_result["ok"] is True

    beneficios = beneficios_result["data"]
    assert len(beneficios) == 1
    assert beneficios[0].id_producto_beneficio == beneficio_opcional.id_producto_beneficio
    assert beneficios[0].costo_aplicado == 135.0


def test_producto_beneficio_base_descarta_costo_extra_y_opcional_lo_conserva():
    producto_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto Costos",
            "descripcion": "Producto para validar costos extra",
            "tipo_seguro": "Gastos Medicos",
            "prima_base": 990.0,
        }
    )
    assert producto_result["ok"] is True
    producto = producto_result["data"]

    base_result = ProductoBeneficioController.create_producto_beneficio(
        {
            "id_producto": producto.id_producto,
            "nombre_beneficio": "Base sin costo",
            "descripcion": "Debe limpiar costo extra por ser base",
            "monto_cobertura": 50000.0,
            "costo_extra": 88.0,
            "incluido_base": True,
        }
    )
    assert base_result["ok"] is True
    assert base_result["data"].costo_extra is None

    opcional_result = ProductoBeneficioController.create_producto_beneficio(
        {
            "id_producto": producto.id_producto,
            "nombre_beneficio": "Opcional con costo",
            "descripcion": "Debe conservar costo extra",
            "monto_cobertura": 18000.0,
            "costo_extra": 125.0,
            "incluido_base": False,
        }
    )
    assert opcional_result["ok"] is True
    assert opcional_result["data"].costo_extra == 125.0


def test_validaciones_basicas():
    duplicado = AgenteController.create_agente(
        {
            "clave_agente": "ag001",
            "cedula": "0000000002",
            "nombre": "Uno",
            "apellido_paterno": "A",
            "apellido_materno": "B",
            "correo": "uno@test.com",
            "rol": "agente",
            "password": "Test1234",
        }
    )
    assert duplicado["ok"] is True

    repetido = AgenteController.create_agente(
        {
            "clave_agente": "ag001",
            "cedula": "0000000003",
            "nombre": "Dos",
            "apellido_paterno": "C",
            "apellido_materno": "D",
            "correo": "dos@test.com",
            "rol": "agente",
            "password": "Test1234",
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


def test_login_rechaza_password_almacenado_en_texto_plano():
    agente_repo.AgenteRepository.create_agente(
        Agente(
            clave_agente="legacy-plain",
            cedula="0000000300",
            nombre="Legacy",
            apellido_paterno="Plain",
            apellido_materno="Text",
            correo="legacy-plain@test.com",
            telefono="5550000300",
            rol="admin",
            password="1234",
        )
    )

    login_result = AuthController.login("legacy-plain", "1234")
    assert login_result["ok"] is False
    assert login_result["error"] == "Clave o contraseña incorrecta."


def test_reglas_dominio_validan_telefonos_y_porcentajes_de_beneficiarios():
    agente_invalido = AgenteController.create_agente(
        {
            "clave_agente": "ag-phone-invalid",
            "cedula": "0000000400",
            "nombre": "Telefono",
            "apellido_paterno": "Invalido",
            "apellido_materno": "Test",
            "correo": "ag-phone-invalid@test.com",
            "telefono": "55ABCD",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_invalido["ok"] is False

    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "ag-domain-rules",
            "cedula": "0000000401",
            "nombre": "Dominio",
            "apellido_paterno": "Reglas",
            "apellido_materno": "Test",
            "correo": "ag-domain-rules@test.com",
            "telefono": "5551110401",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    asegurado_invalido = AseguradoController.create_asegurado(
        {
            "nombre": "Celular",
            "apellido_paterno": "Invalido",
            "apellido_materno": "Test",
            "rfc": "CEIN900101AA1",
            "correo": "celular-invalido@test.com",
            "celular": "12345",
            "calle": "Calle Uno",
            "numero_exterior": "1",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert asegurado_invalido["ok"] is False

    asegurado_result = AseguradoController.create_asegurado(
        {
            "nombre": "Beneficiario",
            "apellido_paterno": "Valido",
            "apellido_materno": "Test",
            "rfc": "BEVA900101AA1",
            "correo": "beneficiario-valido@test.com",
            "celular": "5512345678",
            "calle": "Calle Dos",
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

    producto_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto Reglas Beneficiarios",
            "descripcion": "Producto para validar reglas de beneficiarios",
            "tipo_seguro": "Vida",
            "prima_base": 500.0,
        }
    )
    assert producto_result["ok"] is True
    producto = producto_result["data"]

    poliza_result = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_producto": producto.id_producto,
            "numero_poliza": "PZ-RULES-001",
            "fecha_inicio": date(2026, 1, 1),
            "fecha_vencimiento": date(2027, 1, 1),
            "estatus": "activa",
            "prima_mensual": 500.0,
        }
    )
    assert poliza_result["ok"] is True
    poliza = poliza_result["data"]

    beneficiario_telefono_invalido = BeneficiarioController.create_beneficiario(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_poliza": poliza.id_poliza,
            "nombre_completo": "Telefono Malo",
            "parentesco": "Hermano",
            "porcentaje_participacion": 20.0,
            "telefono": "55AABB",
        }
    )
    assert beneficiario_telefono_invalido["ok"] is False

    beneficiario_uno = BeneficiarioController.create_beneficiario(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_poliza": poliza.id_poliza,
            "nombre_completo": "Persona Uno",
            "parentesco": "Conyuge",
            "porcentaje_participacion": 60.0,
            "telefono": "5511111111",
        }
    )
    assert beneficiario_uno["ok"] is True

    beneficiario_dos = BeneficiarioController.create_beneficiario(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_poliza": poliza.id_poliza,
            "nombre_completo": "Persona Dos",
            "parentesco": "Hijo",
            "porcentaje_participacion": 40.0,
            "telefono": "5522222222",
        }
    )
    assert beneficiario_dos["ok"] is True

    beneficiario_excedido = BeneficiarioController.create_beneficiario(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_poliza": poliza.id_poliza,
            "nombre_completo": "Persona Tres",
            "parentesco": "Madre",
            "porcentaje_participacion": 10.0,
            "telefono": "5533333333",
        }
    )
    assert beneficiario_excedido["ok"] is False
    assert "no puede exceder 100" in beneficiario_excedido["error"]

    update_excedido = BeneficiarioController.update_beneficiario(
        beneficiario_dos["data"].id_beneficiario,
        {"porcentaje_participacion": 50.0},
    )
    assert update_excedido["ok"] is False
    assert "no puede exceder 100" in update_excedido["error"]


def test_beneficiarios_validan_vinculo_y_porcentaje_por_poliza():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "ag-benef-poliza",
            "cedula": "0000000600",
            "nombre": "Benef",
            "apellido_paterno": "Poliza",
            "apellido_materno": "Test",
            "correo": "benef-poliza@test.com",
            "telefono": "5551110600",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    asegurado_result = AseguradoController.create_asegurado(
        {
            "nombre": "Claudia",
            "apellido_paterno": "Benef",
            "apellido_materno": "Poliza",
            "rfc": "CLBP900101AA1",
            "correo": "claudia.benef@test.com",
            "celular": "5512345680",
            "calle": "Calle Tres",
            "numero_exterior": "15",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert asegurado_result["ok"] is True
    asegurado = asegurado_result["data"]

    otro_asegurado_result = AseguradoController.create_asegurado(
        {
            "nombre": "Diego",
            "apellido_paterno": "Ajeno",
            "apellido_materno": "Poliza",
            "rfc": "DIAP900101AA1",
            "correo": "diego.ajeno@test.com",
            "celular": "5512345681",
            "calle": "Calle Cuatro",
            "numero_exterior": "16",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert otro_asegurado_result["ok"] is True
    otro_asegurado = otro_asegurado_result["data"]

    producto_a_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Vida Benef A",
            "descripcion": "Producto A para beneficiarios por poliza",
            "tipo_seguro": "Vida",
            "prima_base": 500.0,
        }
    )
    assert producto_a_result["ok"] is True
    producto_a = producto_a_result["data"]

    producto_b_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Vida Benef B",
            "descripcion": "Producto B para beneficiarios por poliza",
            "tipo_seguro": "Gastos",
            "prima_base": 700.0,
        }
    )
    assert producto_b_result["ok"] is True
    producto_b = producto_b_result["data"]

    poliza_a_result = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_producto": producto_a.id_producto,
            "numero_poliza": "BEN-POL-001",
            "fecha_inicio": date(2026, 1, 1),
            "fecha_vencimiento": date(2027, 1, 1),
            "estatus": "activa",
            "prima_mensual": 800.0,
        }
    )
    assert poliza_a_result["ok"] is True
    poliza_a = poliza_a_result["data"]

    poliza_b_result = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_producto": producto_b.id_producto,
            "numero_poliza": "BEN-POL-002",
            "fecha_inicio": date(2026, 2, 1),
            "fecha_vencimiento": date(2027, 2, 1),
            "estatus": "activa",
            "prima_mensual": 900.0,
        }
    )
    assert poliza_b_result["ok"] is True
    poliza_b = poliza_b_result["data"]

    poliza_ajena_result = PolizaController.create_poliza(
        {
            "id_asegurado": otro_asegurado.id_asegurado,
            "id_producto": producto_a.id_producto,
            "numero_poliza": "BEN-POL-003",
            "fecha_inicio": date(2026, 3, 1),
            "fecha_vencimiento": date(2027, 3, 1),
            "estatus": "activa",
            "prima_mensual": 950.0,
        }
    )
    assert poliza_ajena_result["ok"] is True
    poliza_ajena = poliza_ajena_result["data"]

    beneficiario_uno = BeneficiarioController.create_beneficiario(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_poliza": poliza_a.id_poliza,
            "nombre_completo": "Persona Uno",
            "parentesco": "Conyuge",
            "porcentaje_participacion": 60.0,
            "telefono": "5511111111",
        }
    )
    assert beneficiario_uno["ok"] is True

    beneficiario_dos = BeneficiarioController.create_beneficiario(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_poliza": poliza_a.id_poliza,
            "nombre_completo": "Persona Dos",
            "parentesco": "Hijo",
            "porcentaje_participacion": 40.0,
            "telefono": "5522222222",
        }
    )
    assert beneficiario_dos["ok"] is True

    beneficiario_excedido = BeneficiarioController.create_beneficiario(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_poliza": poliza_a.id_poliza,
            "nombre_completo": "Persona Tres",
            "parentesco": "Madre",
            "porcentaje_participacion": 10.0,
            "telefono": "5533333333",
        }
    )
    assert beneficiario_excedido["ok"] is False
    assert "no puede exceder 100" in beneficiario_excedido["error"]

    beneficiario_otra_poliza = BeneficiarioController.create_beneficiario(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_poliza": poliza_b.id_poliza,
            "nombre_completo": "Persona Cuatro",
            "parentesco": "Madre",
            "porcentaje_participacion": 100.0,
            "telefono": "5544444444",
        }
    )
    assert beneficiario_otra_poliza["ok"] is True

    update_excedido = BeneficiarioController.update_beneficiario(
        beneficiario_dos["data"].id_beneficiario,
        {"porcentaje_participacion": 50.0},
    )
    assert update_excedido["ok"] is False
    assert "no puede exceder 100" in update_excedido["error"]

    poliza_ajena_error = BeneficiarioController.create_beneficiario(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_poliza": poliza_ajena.id_poliza,
            "nombre_completo": "Persona Ajena",
            "parentesco": "Hermana",
            "porcentaje_participacion": 10.0,
            "telefono": "5555555555",
        }
    )
    assert poliza_ajena_error["ok"] is False
    assert "no está vinculado" in poliza_ajena_error["error"].lower() or "vinculada" in poliza_ajena_error["error"].lower()


def test_poliza_y_seguimiento_validan_enums_del_schema():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "ag-schema-enums",
            "cedula": "0000000500",
            "nombre": "Schema",
            "apellido_paterno": "Enums",
            "apellido_materno": "Test",
            "correo": "schema-enums@test.com",
            "telefono": "5551110500",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    asegurado_result = AseguradoController.create_asegurado(
        {
            "nombre": "Poliza",
            "apellido_paterno": "Enum",
            "apellido_materno": "Test",
            "rfc": "POEN900101AA1",
            "correo": "poliza-enum@test.com",
            "celular": "5512345688",
            "calle": "Calle Tres",
            "numero_exterior": "30",
            "numero_interior": "1",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert asegurado_result["ok"] is True
    asegurado = asegurado_result["data"]

    producto_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto Enum Schema",
            "descripcion": "Producto para validar enums",
            "tipo_seguro": "Vida",
            "prima_base": 800.0,
        }
    )
    assert producto_result["ok"] is True
    producto = producto_result["data"]

    poliza_invalida = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_producto": producto.id_producto,
            "numero_poliza": "PZ-ENUM-01",
            "fecha_inicio": date(2026, 3, 1),
            "fecha_vencimiento": date(2027, 3, 1),
            "estatus": "pausada",
            "prima_mensual": 800.0,
        }
    )
    assert poliza_invalida["ok"] is False
    assert "estatus" in poliza_invalida["error"]

    seguimiento_valido = SeguimientoController.create_seguimiento(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_agente": agente.id_agente,
            "folio": "FOL-ENUM-001",
            "asunto": "Seguimiento de prueba",
        }
    )
    assert seguimiento_valido["ok"] is True
    assert seguimiento_valido["data"].folio == "FOL-ENUM-001"


def test_beneficio_soft_delete_usa_deleted_at_y_vigente():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "ag-soft-delete",
            "cedula": "0000000099",
            "nombre": "Soft",
            "apellido_paterno": "Delete",
            "apellido_materno": "Test",
            "correo": "softdelete@test.com",
            "telefono": "5550000099",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    asegurado_result = AseguradoController.create_asegurado(
        {
            "nombre": "Laura",
            "apellido_paterno": "Prueba",
            "apellido_materno": "Delete",
            "rfc": "LAPR900101AA1",
            "correo": "laura@test.com",
            "celular": "5511111111",
            "calle": "Calle Uno",
            "numero_exterior": "10",
            "numero_interior": "1",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert asegurado_result["ok"] is True

    producto_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto Soft Delete",
            "descripcion": "Producto para validar borrado logico",
            "tipo_seguro": "Vida",
            "prima_base": 750.0,
        }
    )
    assert producto_result["ok"] is True
    producto = producto_result["data"]

    poliza_result = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado_result["data"].id_asegurado,
            "id_producto": producto.id_producto,
            "numero_poliza": "PZ-SOFT-001",
            "fecha_inicio": date(2026, 1, 1),
            "fecha_vencimiento": date(2027, 1, 1),
            "estatus": "activa",
            "prima_mensual": 950.0,
        }
    )
    assert poliza_result["ok"] is True

    polizas = PolizaController.get_all_polizas()
    assert polizas["ok"] is True
    poliza = next(p for p in polizas["data"] if p.numero_poliza == "PZ-SOFT-001")

    plantilla_result = ProductoBeneficioController.create_producto_beneficio(
        {
            "id_producto": producto.id_producto,
            "nombre_beneficio": "Hospitalizacion",
            "descripcion": "Cobertura hospitalaria basica",
            "monto_cobertura": 150000.0,
            "incluido_base": True,
        }
    )
    assert plantilla_result["ok"] is True
    plantilla = plantilla_result["data"]

    beneficio_result = BeneficioController.create_beneficio(
        {
            "id_poliza": poliza.id_poliza,
            "id_producto_beneficio": plantilla.id_producto_beneficio,
        }
    )
    assert beneficio_result["ok"] is True
    beneficio = beneficio_result["data"]

    listado_previo = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
    assert listado_previo["ok"] is True
    assert len(listado_previo["data"]) == 1

    borrado = BeneficioController.delete_beneficio(beneficio.id_beneficio)
    assert borrado["ok"] is True

    listado_posterior = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
    assert listado_posterior["ok"] is True
    assert listado_posterior["data"] == []

    with beneficio_repo.create_session() as session:
        persisted = session.get(beneficio_repo.Beneficio, beneficio.id_beneficio)
        assert persisted is not None
        assert persisted.deleted_at is not None
        assert persisted.vigente is False


def test_catalogos_soft_delete_conservan_activo_y_deleted_at():
    producto_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Catalogo Desactivable",
            "descripcion": "Producto para validar catalogo",
            "tipo_seguro": "Vida",
            "prima_base": 800.0,
        }
    )
    assert producto_result["ok"] is True
    producto = producto_result["data"]

    with producto_beneficio_repo.create_session() as session:
        producto_beneficio = producto_beneficio_repo.ProductoBeneficio(
            id_producto=producto.id_producto,
            nombre_beneficio="Cobertura Base",
            descripcion="Cobertura del catalogo",
            monto_cobertura=50000.0,
            incluido_base=True,
        )
        session.add(producto_beneficio)
        session.commit()
        session.refresh(producto_beneficio)
        id_producto_beneficio = producto_beneficio.id_producto_beneficio

    activos_antes = ProductoPolizaController.get_productos_activos()
    assert activos_antes["ok"] is True
    assert any(p.id_producto == producto.id_producto for p in activos_antes["data"])

    beneficios_antes = producto_beneficio_repo.ProductoBeneficioRepository.get_by_producto(producto.id_producto)
    assert len(beneficios_antes) == 1

    borrado_producto = ProductoPolizaController.delete_producto(producto.id_producto)
    assert borrado_producto["ok"] is True

    borrado_beneficio = producto_beneficio_repo.ProductoBeneficioRepository.delete(id_producto_beneficio)
    assert borrado_beneficio is True

    activos_despues = ProductoPolizaController.get_productos_activos()
    assert activos_despues["ok"] is True
    assert all(p.id_producto != producto.id_producto for p in activos_despues["data"])

    beneficios_despues = producto_beneficio_repo.ProductoBeneficioRepository.get_by_producto(producto.id_producto)
    assert beneficios_despues == []

    with producto_poliza_repo.create_session() as session:
        persisted_producto = session.get(producto_poliza_repo.ProductoPoliza, producto.id_producto)
        assert persisted_producto is not None
        assert persisted_producto.activo is False
        assert persisted_producto.deleted_at is not None

    with producto_beneficio_repo.create_session() as session:
        persisted_beneficio = session.get(
            producto_beneficio_repo.ProductoBeneficio,
            id_producto_beneficio,
        )
        assert persisted_beneficio is not None
        assert persisted_beneficio.activo is False
        assert persisted_beneficio.deleted_at is not None


def test_vincular_participante_actualiza_disponibles_y_relaciones():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "ag-participantes",
            "cedula": "0000000600",
            "nombre": "Participantes",
            "apellido_paterno": "Poliza",
            "apellido_materno": "Test",
            "correo": "participantes@test.com",
            "telefono": "5551110600",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    titular_result = AseguradoController.create_asegurado(
        {
            "nombre": "Roberto",
            "apellido_paterno": "Titular",
            "apellido_materno": "Test",
            "rfc": "ROTI900101AA1",
            "correo": "titular@test.com",
            "celular": "5512345601",
            "calle": "Calle Uno",
            "numero_exterior": "10",
            "numero_interior": "2",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert titular_result["ok"] is True
    titular = titular_result["data"]

    dependiente_result = AseguradoController.create_asegurado(
        {
            "nombre": "Camila",
            "apellido_paterno": "Dependiente",
            "apellido_materno": "Test",
            "rfc": "CADE900101AA1",
            "correo": "dependiente@test.com",
            "celular": "5512345602",
            "calle": "Calle Dos",
            "numero_exterior": "20",
            "numero_interior": "4",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert dependiente_result["ok"] is True
    dependiente = dependiente_result["data"]

    producto_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto Participantes",
            "descripcion": "Producto para validar vinculos familiares",
            "tipo_seguro": "Gastos Medicos Mayores",
            "prima_base": 950.0,
        }
    )
    assert producto_result["ok"] is True
    producto = producto_result["data"]

    poliza_result = PolizaController.create_poliza(
        {
            "id_asegurado": titular.id_asegurado,
            "id_producto": producto.id_producto,
            "numero_poliza": "PZ-PART-01",
            "fecha_inicio": date(2026, 5, 1),
            "fecha_vencimiento": date(2027, 5, 1),
            "estatus": "activa",
            "prima_mensual": 950.0,
        }
    )
    assert poliza_result["ok"] is True
    poliza = poliza_result["data"]

    disponibles_antes = PolizaController.get_available_polizas_for_participante(
        dependiente.id_asegurado
    )
    assert disponibles_antes["ok"] is True
    assert [p.id_poliza for p in disponibles_antes["data"]] == [poliza.id_poliza]

    vinculacion = PolizaController.add_participante_to_poliza(
        {
            "id_poliza": poliza.id_poliza,
            "id_asegurado": dependiente.id_asegurado,
            "tipo_participante": "hijo",
        }
    )
    assert vinculacion["ok"] is True
    assert vinculacion["data"].tipo_asegurado == "hijo"

    disponibles_despues = PolizaController.get_available_polizas_for_participante(
        dependiente.id_asegurado
    )
    assert disponibles_despues["ok"] is True
    assert disponibles_despues["data"] == []

    participaciones = PolizaController.get_participaciones_by_asegurado(
        dependiente.id_asegurado
    )
    assert participaciones["ok"] is True
    assert len(participaciones["data"]) == 1
    assert participaciones["data"][0]["id_poliza"] == poliza.id_poliza
    assert participaciones["data"][0]["parentesco"] == "hijo"

    participantes = PolizaController.get_participantes_by_poliza(poliza.id_poliza)
    assert participantes["ok"] is True
    tipos_por_asegurado = {
        row["id_asegurado"]: row["parentesco"] for row in participantes["data"]
    }
    assert tipos_por_asegurado[titular.id_asegurado] == "titular"
    assert tipos_por_asegurado[dependiente.id_asegurado] == "hijo"


def test_disponibles_para_vinculo_excluyen_productos_activos_ya_cubiertos():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "ag-vinculo-producto",
            "cedula": "0000000607",
            "nombre": "Cobertura",
            "apellido_paterno": "Disponible",
            "apellido_materno": "Test",
            "correo": "cobertura-disponible@test.com",
            "telefono": "5551110607",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    asegurado_result = AseguradoController.create_asegurado(
        {
            "nombre": "Lucia",
            "apellido_paterno": "Cobertura",
            "apellido_materno": "Activa",
            "rfc": "LUCA900101AA1",
            "correo": "lucia.cobertura@test.com",
            "celular": "5512345607",
            "calle": "Calle Uno",
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

    titular_a_result = AseguradoController.create_asegurado(
        {
            "nombre": "Mateo",
            "apellido_paterno": "Titular",
            "apellido_materno": "Uno",
            "rfc": "MATU900101AA1",
            "correo": "mateo.titular1@test.com",
            "celular": "5512345608",
            "calle": "Calle Dos",
            "numero_exterior": "20",
            "numero_interior": "4",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert titular_a_result["ok"] is True
    titular_a = titular_a_result["data"]

    titular_b_result = AseguradoController.create_asegurado(
        {
            "nombre": "Paola",
            "apellido_paterno": "Titular",
            "apellido_materno": "Dos",
            "rfc": "PATI900101AA1",
            "correo": "paola.titular2@test.com",
            "celular": "5512345606",
            "calle": "Calle Tres",
            "numero_exterior": "30",
            "numero_interior": "6",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert titular_b_result["ok"] is True
    titular_b = titular_b_result["data"]

    producto_a_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto A",
            "descripcion": "Cobertura activa ya contratada",
            "tipo_seguro": "Vida",
            "prima_base": 700.0,
        }
    )
    assert producto_a_result["ok"] is True
    producto_a = producto_a_result["data"]

    producto_b_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto B",
            "descripcion": "Cobertura alternativa disponible",
            "tipo_seguro": "Gastos Medicos Mayores",
            "prima_base": 920.0,
        }
    )
    assert producto_b_result["ok"] is True
    producto_b = producto_b_result["data"]

    poliza_propia_result = PolizaController.create_poliza(
        {
            "id_asegurado": asegurado.id_asegurado,
            "id_producto": producto_a.id_producto,
            "numero_poliza": "PZ-CUB-ACT-01",
            "fecha_inicio": date(2026, 5, 1),
            "fecha_vencimiento": date(2027, 5, 1),
            "estatus": "activa",
            "prima_mensual": 700.0,
        }
    )
    assert poliza_propia_result["ok"] is True

    poliza_mismo_producto_result = PolizaController.create_poliza(
        {
            "id_asegurado": titular_a.id_asegurado,
            "id_producto": producto_a.id_producto,
            "numero_poliza": "PZ-CUB-ACT-02",
            "fecha_inicio": date(2026, 6, 1),
            "fecha_vencimiento": date(2027, 6, 1),
            "estatus": "activa",
            "prima_mensual": 710.0,
        }
    )
    assert poliza_mismo_producto_result["ok"] is True

    poliza_otro_producto_result = PolizaController.create_poliza(
        {
            "id_asegurado": titular_b.id_asegurado,
            "id_producto": producto_b.id_producto,
            "numero_poliza": "PZ-CUB-DISP-03",
            "fecha_inicio": date(2026, 7, 1),
            "fecha_vencimiento": date(2027, 7, 1),
            "estatus": "activa",
            "prima_mensual": 920.0,
        }
    )
    assert poliza_otro_producto_result["ok"] is True
    poliza_otro_producto = poliza_otro_producto_result["data"]

    disponibles = PolizaController.get_available_polizas_for_participante(
        asegurado.id_asegurado
    )
    assert disponibles["ok"] is True
    assert [poliza.id_poliza for poliza in disponibles["data"]] == [
        poliza_otro_producto.id_poliza
    ]


def test_beneficio_valida_integridad_entre_poliza_participante_y_plantilla():
    agente_result = AgenteController.create_agente(
        {
            "clave_agente": "ag-beneficio-integridad",
            "cedula": "0000000601",
            "nombre": "Beneficio",
            "apellido_paterno": "Integridad",
            "apellido_materno": "Test",
            "correo": "beneficio-integridad@test.com",
            "telefono": "5551110601",
            "rol": "admin",
            "password": "Test1234",
        }
    )
    assert agente_result["ok"] is True
    agente = agente_result["data"]

    titular_uno_result = AseguradoController.create_asegurado(
        {
            "nombre": "Laura",
            "apellido_paterno": "Titular",
            "apellido_materno": "Uno",
            "rfc": "LATI900101AA1",
            "correo": "laura.titular@test.com",
            "celular": "5512345611",
            "calle": "Calle Uno",
            "numero_exterior": "10",
            "numero_interior": "1",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert titular_uno_result["ok"] is True
    titular_uno = titular_uno_result["data"]

    titular_dos_result = AseguradoController.create_asegurado(
        {
            "nombre": "Mario",
            "apellido_paterno": "Titular",
            "apellido_materno": "Dos",
            "rfc": "MATI900101AA1",
            "correo": "mario.titular@test.com",
            "celular": "5512345612",
            "calle": "Calle Dos",
            "numero_exterior": "20",
            "numero_interior": "2",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert titular_dos_result["ok"] is True
    titular_dos = titular_dos_result["data"]

    dependiente_result = AseguradoController.create_asegurado(
        {
            "nombre": "Camila",
            "apellido_paterno": "Dependiente",
            "apellido_materno": "Beneficio",
            "rfc": "CADE900102AA2",
            "correo": "camila.beneficio@test.com",
            "celular": "5512345613",
            "calle": "Calle Tres",
            "numero_exterior": "30",
            "numero_interior": "3",
            "colonia": "Centro",
            "municipio": "Monterrey",
            "estado": "Nuevo Leon",
            "codigo_postal": "64000",
            "id_agente_responsable": agente.id_agente,
        }
    )
    assert dependiente_result["ok"] is True
    dependiente = dependiente_result["data"]

    producto_uno_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto Beneficio A",
            "descripcion": "Producto base para validaciones",
            "tipo_seguro": "Vida",
            "prima_base": 500.0,
        }
    )
    assert producto_uno_result["ok"] is True
    producto_uno = producto_uno_result["data"]

    producto_dos_result = ProductoPolizaController.create_producto(
        {
            "nombre": "Producto Beneficio B",
            "descripcion": "Segundo producto para validaciones",
            "tipo_seguro": "Gastos Medicos Mayores",
            "prima_base": 900.0,
        }
    )
    assert producto_dos_result["ok"] is True
    producto_dos = producto_dos_result["data"]

    plantilla_otro_producto_result = ProductoBeneficioController.create_producto_beneficio(
        {
            "id_producto": producto_dos.id_producto,
            "nombre_beneficio": "Cobertura del otro producto",
            "descripcion": "Plantilla que no corresponde a la poliza principal",
            "monto_cobertura": 75000.0,
            "incluido_base": False,
        }
    )
    assert plantilla_otro_producto_result["ok"] is True
    plantilla_otro_producto = plantilla_otro_producto_result["data"]

    plantilla_producto_uno_result = ProductoBeneficioController.create_producto_beneficio(
        {
            "id_producto": producto_uno.id_producto,
            "nombre_beneficio": "Cobertura valida",
            "descripcion": "Beneficio correctamente relacionado",
            "monto_cobertura": 33000.0,
            "incluido_base": True,
        }
    )
    assert plantilla_producto_uno_result["ok"] is True
    plantilla_producto_uno = plantilla_producto_uno_result["data"]

    poliza_uno_result = PolizaController.create_poliza(
        {
            "id_asegurado": titular_uno.id_asegurado,
            "id_producto": producto_uno.id_producto,
            "numero_poliza": "PZ-BENEF-INT-01",
            "fecha_inicio": date(2026, 6, 1),
            "fecha_vencimiento": date(2027, 6, 1),
            "estatus": "activa",
            "prima_mensual": 500.0,
        }
    )
    assert poliza_uno_result["ok"] is True
    poliza_uno = poliza_uno_result["data"]

    poliza_dos_result = PolizaController.create_poliza(
        {
            "id_asegurado": titular_dos.id_asegurado,
            "id_producto": producto_dos.id_producto,
            "numero_poliza": "PZ-BENEF-INT-02",
            "fecha_inicio": date(2026, 7, 1),
            "fecha_vencimiento": date(2027, 7, 1),
            "estatus": "activa",
            "prima_mensual": 900.0,
        }
    )
    assert poliza_dos_result["ok"] is True
    poliza_dos = poliza_dos_result["data"]

    vinculacion_result = PolizaController.add_participante_to_poliza(
        {
            "id_poliza": poliza_dos.id_poliza,
            "id_asegurado": dependiente.id_asegurado,
            "tipo_participante": "hijo",
        }
    )
    assert vinculacion_result["ok"] is True
    participante_ajeno = vinculacion_result["data"]

    beneficio_participante_invalido = BeneficioController.create_beneficio(
        {
            "id_poliza": poliza_uno.id_poliza,
            "id_asegurado": participante_ajeno.id_asegurado,
            "id_producto_beneficio": plantilla_producto_uno.id_producto_beneficio,
        }
    )
    assert beneficio_participante_invalido["ok"] is False
    assert "no pertenece a la póliza" in beneficio_participante_invalido["error"]

    beneficio_plantilla_invalida = BeneficioController.create_beneficio(
        {
            "id_poliza": poliza_uno.id_poliza,
            "id_producto_beneficio": plantilla_otro_producto.id_producto_beneficio,
        }
    )
    assert beneficio_plantilla_invalida["ok"] is False
    assert "no corresponde al producto" in beneficio_plantilla_invalida["error"]

    beneficio_valido = BeneficioController.create_beneficio(
        {
            "id_poliza": poliza_uno.id_poliza,
            "id_producto_beneficio": plantilla_producto_uno.id_producto_beneficio,
        }
    )
    assert beneficio_valido["ok"] is True
    beneficio = beneficio_valido["data"]

    actualizacion_invalida = BeneficioController.update_beneficio(
        beneficio.id_beneficio,
        {
            "id_asegurado": participante_ajeno.id_asegurado,
        },
    )
    assert actualizacion_invalida["ok"] is False
    assert "no pertenece a la póliza" in actualizacion_invalida["error"]

    actualizacion_plantilla_invalida = BeneficioController.update_beneficio(
        beneficio.id_beneficio,
        {
            "id_producto_beneficio": plantilla_otro_producto.id_producto_beneficio,
        },
    )
    assert actualizacion_plantilla_invalida["ok"] is False
    assert "Solo se permite editar" in actualizacion_plantilla_invalida["error"]


# ---------------------------------------------------------------------------
# Helpers compartidos entre pruebas nuevas
# ---------------------------------------------------------------------------

def _make_agente(suffix: str = "A"):
    r = AgenteController.create_agente({
        "clave_agente": f"clave{suffix}",
        "cedula": f"CED{suffix}",
        "nombre": f"Agente{suffix}",
        "apellido_paterno": "Test",
        "apellido_materno": "Test",
        "correo": f"agente{suffix}@test.com",
        "telefono": "5500000000",
        "rol": "agente",
        "password": "Pass1234",
    })
    assert r["ok"] is True, r.get("error")
    return r["data"]


def _make_asegurado(suffix: str, agente_id: int):
    r = AseguradoController.create_asegurado({
        "nombre": f"Aseg{suffix}",
        "apellido_paterno": "Test",
        "apellido_materno": "Test",
        "rfc": "".join(chr(65 + ord(c) % 26) for c in suffix.upper())[:3].ljust(4, "T") + "010101AA1",
        "correo": f"aseg{suffix}@test.com",
        "celular": "5500000001",
        "calle": "Calle 1",
        "numero_exterior": "1",
        "colonia": "Col",
        "municipio": "Mun",
        "estado": "Edo",
        "codigo_postal": "00001",
        "id_agente_responsable": agente_id,
    })
    assert r["ok"] is True, r.get("error")
    return r["data"]


def _make_producto(suffix: str):
    r = ProductoPolizaController.create_producto({
        "nombre": f"Prod{suffix}",
        "descripcion": "Desc",
        "tipo_seguro": "Vida",
        "prima_base": 500.0,
    })
    assert r["ok"] is True, r.get("error")
    return r["data"]


def _make_poliza(asegurado_id: int, producto_id: int, numero: str):
    r = PolizaController.create_poliza({
        "id_asegurado": asegurado_id,
        "id_producto": producto_id,
        "numero_poliza": numero,
        "fecha_inicio": date(2026, 1, 1),
        "fecha_vencimiento": date(2027, 1, 1),
        "estatus": "activa",
        "prima_mensual": 500.0,
    })
    assert r["ok"] is True, r.get("error")
    return r["data"]


# ---------------------------------------------------------------------------
# Test: cascade soft delete poliza -> beneficios
# ---------------------------------------------------------------------------

def test_cascade_soft_delete_poliza_archiva_sus_beneficios():
    agente = _make_agente("CSC")
    asegurado = _make_asegurado("CSC", agente.id_agente)
    producto = _make_producto("CSC")

    plantilla_r = ProductoBeneficioController.create_producto_beneficio({
        "id_producto": producto.id_producto,
        "nombre_beneficio": "Ben cascade",
        "descripcion": "Desc",
        "monto_cobertura": 10000.0,
        "incluido_base": True,
    })
    assert plantilla_r["ok"] is True

    poliza = _make_poliza(asegurado.id_asegurado, producto.id_producto, "PZ-CSC-001")

    # Base benefit was auto-copied
    beneficios_r = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
    assert beneficios_r["ok"] is True
    assert len(beneficios_r["data"]) >= 1

    # Soft delete the poliza
    del_r = PolizaController.delete_poliza(poliza.id_poliza)
    assert del_r["ok"] is True

    # After deletion, beneficios must not be retrievable (cascade)
    beneficios_after = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
    assert beneficios_after["ok"] is True
    assert beneficios_after["data"] == []


# ---------------------------------------------------------------------------
# Test: poliza status transitions
# ---------------------------------------------------------------------------

def test_poliza_cambio_de_estatus():
    agente = _make_agente("EST")
    asegurado = _make_asegurado("EST", agente.id_agente)
    producto = _make_producto("EST")
    poliza = _make_poliza(asegurado.id_asegurado, producto.id_producto, "PZ-EST-001")

    assert poliza.estatus == "activa"

    r_cancel = PolizaController.update_poliza(poliza.id_poliza, {"estatus": "cancelada"})
    assert r_cancel["ok"] is True
    assert r_cancel["data"].estatus == "cancelada"

    r_venc = PolizaController.update_poliza(poliza.id_poliza, {"estatus": "vencida"})
    assert r_venc["ok"] is True
    assert r_venc["data"].estatus == "vencida"


# ---------------------------------------------------------------------------
# Test: duplicate RFC check in AseguradoService.update()
# ---------------------------------------------------------------------------

def test_asegurado_update_rechaza_rfc_duplicado():
    agente = _make_agente("RFC")
    a1 = _make_asegurado("RF1", agente.id_agente)
    a2 = _make_asegurado("RF2", agente.id_agente)

    r = AseguradoController.update_asegurado(a2.id_asegurado, {"rfc": a1.rfc})
    assert r["ok"] is False
    assert "RFC" in r["error"] or "rfc" in r["error"].lower()


# ---------------------------------------------------------------------------
# Test: duplicate email check in AgenteService.update()
# ---------------------------------------------------------------------------

def test_agente_update_rechaza_correo_duplicado():
    a1 = _make_agente("EML1")
    a2 = _make_agente("EML2")

    r = AgenteController.update_agente(a2.id_agente, {"correo": a1.correo})
    assert r["ok"] is False
    assert "correo" in r["error"].lower()


# ---------------------------------------------------------------------------
# Test: id_agente_responsable existence validation
# ---------------------------------------------------------------------------

def test_asegurado_create_rechaza_agente_inexistente():
    r = AseguradoController.create_asegurado({
        "nombre": "Sin",
        "apellido_paterno": "Agente",
        "apellido_materno": "Valido",
        "rfc": "SNAG010101AA1",
        "correo": "sin@agente.com",
        "celular": "5500000002",
        "calle": "Calle",
        "numero_exterior": "1",
        "colonia": "Col",
        "municipio": "Mun",
        "estado": "Edo",
        "codigo_postal": "00001",
        "id_agente_responsable": 99999,
    })
    assert r["ok"] is False
    assert "agente" in r["error"].lower()


# ---------------------------------------------------------------------------
# Test: porcentaje edge cases
# ---------------------------------------------------------------------------

def test_beneficiarios_porcentaje_exactamente_100_es_valido():
    agente = _make_agente("PCT")
    asegurado = _make_asegurado("PCT", agente.id_agente)
    producto = _make_producto("PCT")
    poliza = _make_poliza(asegurado.id_asegurado, producto.id_producto, "PZ-PCT-001")

    r1 = BeneficiarioController.create_beneficiario({
        "id_asegurado": asegurado.id_asegurado,
        "id_poliza": poliza.id_poliza,
        "nombre_completo": "Ben Uno",
        "parentesco": "Hijo",
        "porcentaje_participacion": 60.0,
    })
    assert r1["ok"] is True

    r2 = BeneficiarioController.create_beneficiario({
        "id_asegurado": asegurado.id_asegurado,
        "id_poliza": poliza.id_poliza,
        "nombre_completo": "Ben Dos",
        "parentesco": "Conyuge",
        "porcentaje_participacion": 40.0,
    })
    assert r2["ok"] is True


def test_beneficiarios_porcentaje_supera_100_es_rechazado():
    agente = _make_agente("OVR")
    asegurado = _make_asegurado("OVR", agente.id_agente)
    producto = _make_producto("OVR")
    poliza = _make_poliza(asegurado.id_asegurado, producto.id_producto, "PZ-OVR-001")

    r1 = BeneficiarioController.create_beneficiario({
        "id_asegurado": asegurado.id_asegurado,
        "id_poliza": poliza.id_poliza,
        "nombre_completo": "Ben A",
        "parentesco": "Hijo",
        "porcentaje_participacion": 80.0,
    })
    assert r1["ok"] is True

    r2 = BeneficiarioController.create_beneficiario({
        "id_asegurado": asegurado.id_asegurado,
        "id_poliza": poliza.id_poliza,
        "nombre_completo": "Ben B",
        "parentesco": "Conyuge",
        "porcentaje_participacion": 30.0,
    })
    assert r2["ok"] is False
    assert "100" in r2["error"]


def test_beneficiario_porcentaje_cero_es_rechazado():
    agente = _make_agente("ZER")
    asegurado = _make_asegurado("ZER", agente.id_agente)
    producto = _make_producto("ZER")
    poliza = _make_poliza(asegurado.id_asegurado, producto.id_producto, "PZ-ZER-001")

    r = BeneficiarioController.create_beneficiario({
        "id_asegurado": asegurado.id_asegurado,
        "id_poliza": poliza.id_poliza,
        "nombre_completo": "Ben Cero",
        "parentesco": "Hijo",
        "porcentaje_participacion": 0.0,
    })
    assert r["ok"] is False


# ──────────────────────────────────────────────────────────────────────────────
# Phase-B new tests: password strength, cascade asegurado→beneficiarios, FK checks
# ──────────────────────────────────────────────────────────────────────────────

def test_password_debil_es_rechazado():
    """Passwords that are too short, missing uppercase, or missing digits are rejected."""
    base = {
        "clave_agente": "pw-test",
        "cedula": "2000000001",
        "nombre": "PW",
        "apellido_paterno": "Test",
        "apellido_materno": "X",
        "correo": "pw-test@test.com",
        "telefono": "5500000000",
        "rol": "agente",
    }

    r_short = AgenteController.create_agente({**base, "password": "Ab1"})
    assert r_short["ok"] is False
    assert "8 caracteres" in r_short["error"]

    r_no_upper = AgenteController.create_agente({**base, "clave_agente": "pw-test2", "cedula": "2000000002",
                                                 "correo": "pw2@test.com", "password": "testpass1"})
    assert r_no_upper["ok"] is False
    assert "mayúscula" in r_no_upper["error"]

    r_no_digit = AgenteController.create_agente({**base, "clave_agente": "pw-test3", "cedula": "2000000003",
                                                 "correo": "pw3@test.com", "password": "Testpassword"})
    assert r_no_digit["ok"] is False
    assert "dígito" in r_no_digit["error"]


def test_cascade_soft_delete_asegurado_archiva_beneficiarios():
    """Soft-deleting an asegurado should also soft-delete their beneficiarios."""
    agente = _make_agente("CASC")
    asegurado = _make_asegurado("CASC", agente.id_agente)
    producto = _make_producto("CASC")
    poliza = _make_poliza(asegurado.id_asegurado, producto.id_producto, "PZ-CASC-001")

    r_ben = BeneficiarioController.create_beneficiario({
        "id_asegurado": asegurado.id_asegurado,
        "id_poliza": poliza.id_poliza,
        "nombre_completo": "Cascade Ben",
        "parentesco": "Conyuge",
        "porcentaje_participacion": 50.0,
    })
    assert r_ben["ok"] is True
    beneficiario_id = r_ben["data"].id_beneficiario

    AseguradoController.delete_asegurado(asegurado.id_asegurado)

    # beneficiario should now be gone (soft-deleted)
    from repositories.beneficiario_repository import BeneficiarioRepository
    ben_after = BeneficiarioRepository.get_by_id(beneficiario_id)
    assert ben_after is None


def test_seguimiento_create_rechaza_asegurado_inexistente():
    """SeguimientoService.create() rejects a non-existent id_asegurado."""
    agente = _make_agente("SEGFK")
    r = SeguimientoController.create_seguimiento({
        "folio": "FOL-FK01",
        "asunto": "Test",
        "id_asegurado": 999999,
        "id_agente": agente.id_agente,
    })
    assert r["ok"] is False
    assert "asegurado" in r["error"].lower()


def test_seguimiento_create_rechaza_agente_inexistente():
    """SeguimientoService.create() rejects a non-existent id_agente."""
    agente = _make_agente("SEGFK2")
    asegurado = _make_asegurado("SEGFK2", agente.id_agente)
    r = SeguimientoController.create_seguimiento({
        "folio": "FOL-FK02",
        "asunto": "Test",
        "id_asegurado": asegurado.id_asegurado,
        "id_agente": 999999,
    })
    assert r["ok"] is False
    assert "agente" in r["error"].lower()


# ──────────────────────────────────────────────────────────────────────────────
# Tests Schema v4: Seguimiento por folio + contactos
# ──────────────────────────────────────────────────────────────────────────────

def test_seguimiento_folio_con_contactos_flujo_completo():
    """Flujo completo: crear folio → agregar contactos → ver historial."""
    agente = _make_agente("FOL")
    asegurado = _make_asegurado("FOL", agente.id_agente)

    # 1. Crear folio
    r_folio = SeguimientoController.create_seguimiento({
        "folio": "SEG-2026-999",
        "asunto": "Renovación anual",
        "id_asegurado": asegurado.id_asegurado,
        "id_agente": agente.id_agente,
    })
    assert r_folio["ok"] is True
    folio = r_folio["data"]
    assert folio.folio == "SEG-2026-999"

    # 2. Agregar contacto 1 (agente → llamada)
    from datetime import datetime
    r_c1 = SeguimientoContactoController.create_contacto({
        "id_seguimiento": folio.id_seguimiento,
        "iniciado_por": "agente",
        "tipo_contacto": "llamada",
        "resultado": "pendiente",
        "observaciones": "Llamé para recordar vencimiento",
        "fecha_hora": datetime(2026, 1, 15, 10, 30),
    })
    assert r_c1["ok"] is True

    # 3. Agregar contacto 2 (asegurado → mensaje)
    r_c2 = SeguimientoContactoController.create_contacto({
        "id_seguimiento": folio.id_seguimiento,
        "iniciado_por": "asegurado",
        "tipo_contacto": "mensaje",
        "resultado": "resuelto",
        "observaciones": "Ya pagué la póliza, gracias",
        "fecha_hora": datetime(2026, 1, 16, 14, 20),
    })
    assert r_c2["ok"] is True

    # 4. Obtener folio con contactos
    r_historial = SeguimientoController.get_seguimiento_con_contactos(folio.id_seguimiento)
    assert r_historial["ok"] is True
    data = r_historial["data"]
    assert data["seguimiento"].folio == "SEG-2026-999"
    assert len(data["contactos"]) == 2
    assert data["contactos"][0].tipo_contacto == "llamada"
    assert data["contactos"][1].tipo_contacto == "mensaje"
    assert data["contactos"][1].resultado == "resuelto"

    # 5. Listar folios del asegurado con contactos
    r_lista = SeguimientoController.get_seguimientos_by_asegurado_con_contactos(
        asegurado.id_asegurado
    )
    assert r_lista["ok"] is True
    assert len(r_lista["data"]) == 1
    assert len(r_lista["data"][0]["contactos"]) == 2


def test_seguimiento_contacto_rechaza_folio_inexistente():
    """No se puede crear contacto sin folio válido."""
    from datetime import datetime
    r = SeguimientoContactoController.create_contacto({
        "id_seguimiento": 999999,
        "iniciado_por": "agente",
        "tipo_contacto": "llamada",
        "resultado": "pendiente",
        "observaciones": "Test",
        "fecha_hora": datetime.now(),
    })
    assert r["ok"] is False
    assert "folio" in r["error"].lower() or "no existe" in r["error"].lower()


# ──────────────────────────────────────────────────────────────────────────────
# Tests Schema v4: Dependientes en asegurado (tipo_asegurado + id_poliza)
# ──────────────────────────────────────────────────────────────────────────────

def test_dependiente_flujo_completo_v4():
    """Flujo v4: titular crea póliza → agrega dependiente → dependiente tiene beneficios."""
    agente = _make_agente("DEP")
    titular = _make_asegurado("DEP", agente.id_agente)
    producto = _make_producto("DEP")
    poliza = _make_poliza(titular.id_asegurado, producto.id_producto, "PZ-DEP-001")

    # Crear dependiente (conyuge)
    r_dep = AseguradoController.create_asegurado({
        "nombre": "Maria",
        "apellido_paterno": "Dependiente",
        "apellido_materno": "Test",
        "rfc": "DEPM010101AA1",
        "correo": "dep@test.com",
        "celular": "5500000000",
        "calle": "Calle Dep",
        "numero_exterior": "10",
        "colonia": "Col",
        "municipio": "Mun",
        "estado": "Edo",
        "codigo_postal": "00001",
        "id_agente_responsable": agente.id_agente,
    })
    assert r_dep["ok"] is True
    dependiente = r_dep["data"]

    # Vincular dependiente a póliza
    r_vinc = PolizaController.add_participante_to_poliza({
        "id_poliza": poliza.id_poliza,
        "id_asegurado": dependiente.id_asegurado,
        "tipo_participante": "conyuge",
    })
    assert r_vinc["ok"] is True
    assert r_vinc["data"].tipo_asegurado == "conyuge"
    assert r_vinc["data"].id_poliza == poliza.id_poliza

    # Verificar que participantes de la póliza incluyen al dependiente
    r_parts = PolizaController.get_participantes_by_poliza(poliza.id_poliza)
    assert r_parts["ok"] is True
    ids_asegurados = {p["id_asegurado"] for p in r_parts["data"]}
    assert titular.id_asegurado in ids_asegurados
    assert dependiente.id_asegurado in ids_asegurados

    # Verificar participaciones del dependiente
    r_part_dep = PolizaController.get_participaciones_by_asegurado(dependiente.id_asegurado)
    assert r_part_dep["ok"] is True
    assert len(r_part_dep["data"]) == 1
    assert r_part_dep["data"][0]["tipo_asegurado"] == "conyuge"


def test_beneficiario_dependiente_flujo_v4():
    """Crear beneficiario para un dependiente específico."""
    agente = _make_agente("BEND")
    titular = _make_asegurado("BEND", agente.id_agente)
    producto = _make_producto("BEND")
    poliza = _make_poliza(titular.id_asegurado, producto.id_producto, "PZ-BEND-001")

    # Crear y vincular dependiente
    r_dep = AseguradoController.create_asegurado({
        "nombre": "Hijo",
        "apellido_paterno": "Test",
        "apellido_materno": "V4",
        "rfc": "HITV010101AA1",
        "correo": "hijo@test.com",
        "celular": "5500000001",
        "calle": "Calle",
        "numero_exterior": "1",
        "colonia": "Col",
        "municipio": "Mun",
        "estado": "Edo",
        "codigo_postal": "00001",
        "id_agente_responsable": agente.id_agente,
    })
    dependiente = r_dep["data"]
    PolizaController.add_participante_to_poliza({
        "id_poliza": poliza.id_poliza,
        "id_asegurado": dependiente.id_asegurado,
        "tipo_participante": "hijo",
    })

    # Beneficiario del TITULAR
    r_ben_tit = BeneficiarioController.create_beneficiario({
        "id_asegurado": titular.id_asegurado,
        "id_poliza": poliza.id_poliza,
        "nombre_completo": "Esposa Titular",
        "parentesco": "Conyuge",
        "porcentaje_participacion": 100.0,
    })
    assert r_ben_tit["ok"] is True

    # Beneficiario del DEPENDIENTE
    r_ben_dep = BeneficiarioController.create_beneficiario({
        "id_asegurado": dependiente.id_asegurado,
        "id_poliza": poliza.id_poliza,
        "nombre_completo": "Abuelo del Hijo",
        "parentesco": "Abuelo",
        "porcentaje_participacion": 100.0,
    })
    assert r_ben_dep["ok"] is True
    assert r_ben_dep["data"].id_asegurado == dependiente.id_asegurado

    # Verificar que get_by_asegurado retorna los beneficiarios correctos
    r_bens_dep = BeneficiarioController.get_beneficiarios_by_asegurado(dependiente.id_asegurado)
    assert r_bens_dep["ok"] is True
    assert len(r_bens_dep["data"]) == 1
    assert r_bens_dep["data"][0].nombre_completo == "Abuelo del Hijo"


def test_beneficio_dependiente_flujo_v4():
    """Asignar beneficio específico a un dependiente dentro de la póliza."""
    agente = _make_agente("BFD")
    titular = _make_asegurado("BFD", agente.id_agente)
    producto = _make_producto("BFD")
    poliza = _make_poliza(titular.id_asegurado, producto.id_producto, "PZ-BFD-001")

    # Crear plantilla de beneficio
    plantilla_r = ProductoBeneficioController.create_producto_beneficio({
        "id_producto": producto.id_producto,
        "nombre_beneficio": "Cobertura dental",
        "descripcion": "Cobertura dental familiar",
        "monto_cobertura": 50000.0,
        "incluido_base": True,
    })
    assert plantilla_r["ok"] is True
    plantilla = plantilla_r["data"]

    # Beneficio para TITULAR (id_asegurado = None)
    r_ben_tit = BeneficioController.create_beneficio({
        "id_poliza": poliza.id_poliza,
        "id_producto_beneficio": plantilla.id_producto_beneficio,
    })
    assert r_ben_tit["ok"] is True
    assert r_ben_tit["data"].id_asegurado is None

    # Crear dependiente
    r_dep = AseguradoController.create_asegurado({
        "nombre": "Hijo",
        "apellido_paterno": "Dental",
        "apellido_materno": "Test",
        "rfc": "HIDT010101AA1",
        "correo": "hijo_dental@test.com",
        "celular": "5500000002",
        "calle": "Calle",
        "numero_exterior": "1",
        "colonia": "Col",
        "municipio": "Mun",
        "estado": "Edo",
        "codigo_postal": "00001",
        "id_agente_responsable": agente.id_agente,
    })
    dependiente = r_dep["data"]
    PolizaController.add_participante_to_poliza({
        "id_poliza": poliza.id_poliza,
        "id_asegurado": dependiente.id_asegurado,
        "tipo_participante": "hijo",
    })

    # Beneficio para DEPENDIENTE (id_asegurado = dependiente.id)
    r_ben_dep = BeneficioController.create_beneficio({
        "id_poliza": poliza.id_poliza,
        "id_producto_beneficio": plantilla.id_producto_beneficio,
        "id_asegurado": dependiente.id_asegurado,
    })
    assert r_ben_dep["ok"] is True
    assert r_ben_dep["data"].id_asegurado == dependiente.id_asegurado

    # Listar beneficios por póliza
    r_beneficios = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
    assert r_beneficios["ok"] is True
    assert len(r_beneficios["data"]) == 2


# ──────────────────────────────────────────────────────────────────────────────
# Tests Schema v4: Flujo end-to-end completo
# ──────────────────────────────────────────────────────────────────────────────

def test_flujo_completo_v4_end_to_end():
    """Flujo completo: agente → titular → póliza → dependiente → beneficio → beneficiario → seguimiento."""
    # 1. Agente
    agente_r = AgenteController.create_agente({
        "clave_agente": "e2e-agente",
        "cedula": "E2E0000001",
        "nombre": "End2End",
        "apellido_paterno": "Agente",
        "apellido_materno": "Test",
        "correo": "e2e@test.com",
        "telefono": "5500000000",
        "rol": "admin",
        "password": "TestPass123",
    })
    assert agente_r["ok"] is True
    agente = agente_r["data"]

    # 2. Titular
    titular_r = AseguradoController.create_asegurado({
        "nombre": "Juan",
        "apellido_paterno": "Titular",
        "apellido_materno": "E2E",
        "rfc": "JUTE010101AA1",
        "correo": "titular@test.com",
        "celular": "5500000001",
        "calle": "Calle Principal",
        "numero_exterior": "100",
        "colonia": "Centro",
        "municipio": "Monterrey",
        "estado": "Nuevo Leon",
        "codigo_postal": "64000",
        "id_agente_responsable": agente.id_agente,
    })
    assert titular_r["ok"] is True
    titular = titular_r["data"]
    assert titular.tipo_asegurado == "titular"
    assert titular.id_poliza is None

    # 3. Producto
    producto_r = ProductoPolizaController.create_producto({
        "nombre": "Plan Familiar E2E",
        "descripcion": "Plan completo",
        "tipo_seguro": "Vida",
        "prima_base": 1200.0,
    })
    assert producto_r["ok"] is True
    producto = producto_r["data"]

    # 4. Beneficio base del catálogo
    plantilla_r = ProductoBeneficioController.create_producto_beneficio({
        "id_producto": producto.id_producto,
        "nombre_beneficio": "Hospitalización",
        "descripcion": "Cobertura hospitalaria",
        "monto_cobertura": 1000000.0,
        "incluido_base": True,
    })
    assert plantilla_r["ok"] is True
    plantilla = plantilla_r["data"]

    # 5. Póliza
    poliza_r = PolizaController.create_poliza({
        "id_asegurado": titular.id_asegurado,
        "id_producto": producto.id_producto,
        "numero_poliza": "PZ-E2E-001",
        "fecha_inicio": date(2026, 1, 1),
        "fecha_vencimiento": date(2027, 1, 1),
        "estatus": "activa",
        "prima_mensual": 1200.0,
    })
    assert poliza_r["ok"] is True
    poliza = poliza_r["data"]

    # 6. Beneficio del catálogo se copió automáticamente
    beneficios_r = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
    assert beneficios_r["ok"] is True
    assert len(beneficios_r["data"]) == 1
    beneficio_base = beneficios_r["data"][0]
    assert beneficio_base.id_asegurado is None  # Aplica a titular

    # 7. Beneficiario del titular
    ben_tit_r = BeneficiarioController.create_beneficiario({
        "id_asegurado": titular.id_asegurado,
        "id_poliza": poliza.id_poliza,
        "nombre_completo": "Esposa del Titular",
        "parentesco": "Conyuge",
        "porcentaje_participacion": 100.0,
    })
    assert ben_tit_r["ok"] is True

    # 8. Dependiente (hijo)
    hijo_r = AseguradoController.create_asegurado({
        "nombre": "Pedro",
        "apellido_paterno": "Hijo",
        "apellido_materno": "E2E",
        "rfc": "PEHE010101AA1",
        "correo": "hijo@test.com",
        "celular": "5500000002",
        "calle": "Calle Principal",
        "numero_exterior": "100",
        "colonia": "Centro",
        "municipio": "Monterrey",
        "estado": "Nuevo Leon",
        "codigo_postal": "64000",
        "id_agente_responsable": agente.id_agente,
    })
    assert hijo_r["ok"] is True
    hijo = hijo_r["data"]

    # 9. Vincular hijo a póliza
    vinc_r = PolizaController.add_participante_to_poliza({
        "id_poliza": poliza.id_poliza,
        "id_asegurado": hijo.id_asegurado,
        "tipo_participante": "hijo",
    })
    assert vinc_r["ok"] is True
    assert vinc_r["data"].tipo_asegurado == "hijo"
    assert vinc_r["data"].id_poliza == poliza.id_poliza

    # 10. Beneficio específico para el hijo
    ben_hijo_r = BeneficioController.create_beneficio({
        "id_poliza": poliza.id_poliza,
        "id_producto_beneficio": plantilla.id_producto_beneficio,
        "id_asegurado": hijo.id_asegurado,
    })
    assert ben_hijo_r["ok"] is True
    assert ben_hijo_r["data"].id_asegurado == hijo.id_asegurado

    # 11. Beneficiario del hijo
    ben_hijo2_r = BeneficiarioController.create_beneficiario({
        "id_asegurado": hijo.id_asegurado,
        "id_poliza": poliza.id_poliza,
        "nombre_completo": "Abuelo Materno",
        "parentesco": "Abuelo",
        "porcentaje_participacion": 100.0,
    })
    assert ben_hijo2_r["ok"] is True

    # 12. Folio de seguimiento
    from datetime import datetime
    folio_r = SeguimientoController.create_seguimiento({
        "folio": "SEG-E2E-001",
        "asunto": "Revisión anual de póliza",
        "id_asegurado": titular.id_asegurado,
        "id_agente": agente.id_agente,
    })
    assert folio_r["ok"] is True
    folio = folio_r["data"]

    # 13. Contactos del folio
    c1_r = SeguimientoContactoController.create_contacto({
        "id_seguimiento": folio.id_seguimiento,
        "iniciado_por": "agente",
        "tipo_contacto": "llamada",
        "resultado": "pendiente",
        "observaciones": "Llamada inicial para agendar revisión",
        "fecha_hora": datetime(2026, 3, 1, 10, 0),
    })
    assert c1_r["ok"] is True

    c2_r = SeguimientoContactoController.create_contacto({
        "id_seguimiento": folio.id_seguimiento,
        "iniciado_por": "asegurado",
        "tipo_contacto": "mensaje",
        "resultado": "resuelto",
        "observaciones": "Confirmé fecha para el 15 de marzo",
        "fecha_hora": datetime(2026, 3, 2, 14, 30),
    })
    assert c2_r["ok"] is True

    # 14. Verificar historial completo
    hist_r = SeguimientoController.get_seguimiento_con_contactos(folio.id_seguimiento)
    assert hist_r["ok"] is True
    assert len(hist_r["data"]["contactos"]) == 2

    # 15. Soft delete de póliza debe archivar todo
    del_poliza = PolizaController.delete_poliza(poliza.id_poliza)
    assert del_poliza["ok"] is True

    # Verificar que beneficios quedaron soft-deleted
    ben_after = BeneficioController.get_beneficios_by_poliza(poliza.id_poliza)
    assert ben_after["ok"] is True
    assert len(ben_after["data"]) == 0

    # Verificar que dependiente quedó desvinculado
    from repositories.asegurado_repository import AseguradoRepository
    hijo_after = AseguradoRepository.get_by_id(hijo.id_asegurado)
    assert hijo_after.id_poliza is None
    assert hijo_after.tipo_asegurado == "titular"
