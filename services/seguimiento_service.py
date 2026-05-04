from models.seguimiento import Seguimiento
from repositories.agente_repository import AgenteRepository
from repositories.asegurado_repository import AseguradoRepository
from repositories.seguimiento_repository import SeguimientoRepository
from services.validators import validar_enum, validar_requerido


class SeguimientoService:
    _TIPOS_CONTACTO_VALIDOS = {"llamada", "mensaje", "visita"}
    _RESULTADOS_VALIDOS = {"pendiente", "resuelto", "sin_respuesta"}

    @staticmethod
    def create(data: dict) -> Seguimiento:
        tipo_contacto = str(data.get("tipo_contacto", "")).strip().lower()
        resultado = str(data.get("resultado", "")).strip().lower()

        validar_enum(tipo_contacto, "tipo_contacto", SeguimientoService._TIPOS_CONTACTO_VALIDOS)
        validar_requerido(data.get("observaciones", ""), "observaciones")
        validar_enum(resultado, "resultado", SeguimientoService._RESULTADOS_VALIDOS)

        if not AseguradoRepository.get_by_id(int(data.get("id_asegurado", 0) or 0)):
            raise ValueError("El asegurado seleccionado no existe.")
        if not AgenteRepository.get_agente_by_id(int(data.get("id_agente", 0) or 0)):
            raise ValueError("El agente seleccionado no existe.")

        payload = data.copy()
        payload["tipo_contacto"] = tipo_contacto
        payload["resultado"] = resultado
        return SeguimientoRepository.create(Seguimiento(**payload))

    @staticmethod
    def get_by_id(id_seguimiento: int) -> Seguimiento | None:
        return SeguimientoRepository.get_by_id(id_seguimiento)

    @staticmethod
    def get_all() -> list[Seguimiento]:
        return SeguimientoRepository.get_all()

    @staticmethod
    def get_by_asegurado(id_asegurado: int) -> list[Seguimiento]:
        return SeguimientoRepository.get_by_asegurado(id_asegurado)

    @staticmethod
    def update(id_seguimiento: int, data: dict) -> Seguimiento | None:
        payload = data.copy()
        if "tipo_contacto" in payload:
            payload["tipo_contacto"] = str(payload["tipo_contacto"]).strip().lower()
            validar_enum(
                payload["tipo_contacto"],
                "tipo_contacto",
                SeguimientoService._TIPOS_CONTACTO_VALIDOS,
            )
        if "resultado" in payload:
            payload["resultado"] = str(payload["resultado"]).strip().lower()
            validar_enum(
                payload["resultado"],
                "resultado",
                SeguimientoService._RESULTADOS_VALIDOS,
            )
        if "observaciones" in payload:
            validar_requerido(payload.get("observaciones", ""), "observaciones")
        return SeguimientoRepository.update(id_seguimiento, payload)

    @staticmethod
    def delete(id_seguimiento: int) -> bool:
        return SeguimientoRepository.delete(id_seguimiento)
