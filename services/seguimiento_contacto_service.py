from datetime import datetime

from models.seguimiento_contacto import SeguimientoContacto
from repositories.seguimiento_contacto_repository import SeguimientoContactoRepository
from repositories.seguimiento_repository import SeguimientoRepository
from services.validators import validar_enum, validar_requerido

_INICIADO_POR_VALIDOS = {"agente", "asegurado"}
_TIPO_CONTACTO_VALIDOS = {"llamada", "visita", "mensaje"}
_RESULTADO_VALIDOS = {"resuelto", "pendiente", "sin_respuesta"}

_EDITABLES = {"iniciado_por", "tipo_contacto", "observaciones", "resultado", "fecha_hora"}


class SeguimientoContactoService:
    @staticmethod
    def create(data: dict) -> SeguimientoContacto:
        validar_requerido(data.get("id_seguimiento"), "id_seguimiento")
        validar_requerido(data.get("observaciones"), "observaciones")
        validar_enum(data.get("iniciado_por", ""), "iniciado_por", _INICIADO_POR_VALIDOS)
        validar_enum(data.get("tipo_contacto", ""), "tipo_contacto", _TIPO_CONTACTO_VALIDOS)
        validar_enum(data.get("resultado", ""), "resultado", _RESULTADO_VALIDOS)

        if not SeguimientoRepository.get_by_id(int(data["id_seguimiento"])):
            raise ValueError("El seguimiento seleccionado no existe.")

        payload = data.copy()
        if isinstance(payload.get("fecha_hora"), str):
            payload["fecha_hora"] = datetime.fromisoformat(payload["fecha_hora"])

        return SeguimientoContactoRepository.create(SeguimientoContacto(**payload))

    @staticmethod
    def get_by_id(id_contacto: int) -> SeguimientoContacto | None:
        return SeguimientoContactoRepository.get_by_id(id_contacto)

    @staticmethod
    def get_all() -> list[SeguimientoContacto]:
        return SeguimientoContactoRepository.get_all()

    @staticmethod
    def get_by_seguimiento(id_seguimiento: int) -> list[SeguimientoContacto]:
        return SeguimientoContactoRepository.get_by_seguimiento(id_seguimiento)

    @staticmethod
    def update(id_contacto: int, data: dict) -> SeguimientoContacto | None:
        payload = {}
        for key in _EDITABLES:
            if key in data:
                value = data[key]
                if key == "iniciado_por":
                    validar_enum(value, "iniciado_por", _INICIADO_POR_VALIDOS)
                elif key == "tipo_contacto":
                    validar_enum(value, "tipo_contacto", _TIPO_CONTACTO_VALIDOS)
                elif key == "resultado":
                    validar_enum(value, "resultado", _RESULTADO_VALIDOS)
                elif key == "observaciones":
                    validar_requerido(value, "observaciones")
                elif key == "fecha_hora" and isinstance(value, str):
                    value = datetime.fromisoformat(value)
                payload[key] = value
        return SeguimientoContactoRepository.update(id_contacto, payload)

    @staticmethod
    def delete(id_contacto: int) -> bool:
        return SeguimientoContactoRepository.delete(id_contacto)
