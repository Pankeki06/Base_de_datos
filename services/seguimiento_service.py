from models.seguimiento import Seguimiento
from repositories.seguimiento_repository import SeguimientoRepository
from services.validators import validar_requerido


class SeguimientoService:
    @staticmethod
    def create(data: dict) -> Seguimiento:
        validar_requerido(data.get("tipo_contacto", ""), "tipo_contacto")
        validar_requerido(data.get("observaciones", ""), "observaciones")
        validar_requerido(data.get("resultado", ""), "resultado")
        return SeguimientoRepository.create(Seguimiento(**data))

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
        return SeguimientoRepository.update(id_seguimiento, data)

    @staticmethod
    def delete(id_seguimiento: int) -> bool:
        return SeguimientoRepository.delete(id_seguimiento)
