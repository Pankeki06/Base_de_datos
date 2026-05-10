from models.seguimiento import Seguimiento
from repositories.agente_repository import AgenteRepository
from repositories.asegurado_repository import AseguradoRepository
from repositories.seguimiento_repository import SeguimientoRepository
from services.validators import validar_requerido


class SeguimientoService:
    @staticmethod
    def create(data: dict) -> Seguimiento:
        validar_requerido(data.get("folio", ""), "folio")
        validar_requerido(data.get("asunto", ""), "asunto")

        if not AseguradoRepository.get_by_id(int(data.get("id_asegurado", 0) or 0)):
            raise ValueError("El asegurado seleccionado no existe.")
        if not AgenteRepository.get_agente_by_id(int(data.get("id_agente", 0) or 0)):
            raise ValueError("El agente seleccionado no existe.")

        payload = data.copy()
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
        if "folio" in payload:
            validar_requerido(payload.get("folio", ""), "folio")
        if "asunto" in payload:
            validar_requerido(payload.get("asunto", ""), "asunto")
        return SeguimientoRepository.update(id_seguimiento, payload)

    @staticmethod
    def delete(id_seguimiento: int) -> bool:
        return SeguimientoRepository.delete(id_seguimiento)
