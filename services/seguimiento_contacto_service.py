from datetime import datetime

from models.seguimiento_contacto import SeguimientoContacto
from repositories.seguimiento_contacto_repository import SeguimientoContactoRepository
from repositories.seguimiento_repository import SeguimientoRepository
from services.validators import validar_requerido


class SeguimientoContactoService:
    @staticmethod
    def create(data: dict) -> SeguimientoContacto:
        validar_requerido(data.get("tipo_contacto", ""), "tipo_contacto")
        validar_requerido(data.get("resultado", ""), "resultado")
        validar_requerido(data.get("observaciones", ""), "observaciones")
        
        # Validar que el seguimiento existe
        id_seguimiento = int(data.get("id_seguimiento", 0))
        if not SeguimientoRepository.get_by_id(id_seguimiento):
            raise ValueError("El folio de seguimiento no existe.")
        
        payload = data.copy()
        return SeguimientoContactoRepository.create(SeguimientoContacto(**payload))

    @staticmethod
    def get_by_id(id_contacto: int) -> SeguimientoContacto | None:
        return SeguimientoContactoRepository.get_by_id(id_contacto)

    @staticmethod
    def get_by_seguimiento(id_seguimiento: int) -> list[SeguimientoContacto]:
        """Retorna todos los contactos de un folio, ordenados por fecha."""
        return SeguimientoContactoRepository.get_by_seguimiento(id_seguimiento)

    @staticmethod
    def get_all() -> list[SeguimientoContacto]:
        return SeguimientoContactoRepository.get_all()

    @staticmethod
    def update(id_contacto: int, data: dict) -> SeguimientoContacto | None:
        payload = data.copy()
        return SeguimientoContactoRepository.update(id_contacto, payload)

    @staticmethod
    def delete(id_contacto: int) -> bool:
        return SeguimientoContactoRepository.delete(id_contacto)
