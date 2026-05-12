from models.seguimiento import Seguimiento
from repositories.agente_repository import AgenteRepository
from repositories.asegurado_repository import AseguradoRepository
from repositories.seguimiento_contacto_repository import SeguimientoContactoRepository
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
    def get_by_id_con_contactos(id_seguimiento: int) -> dict | None:
        """Retorna el seguimiento con todos sus contactos."""
        seguimiento = SeguimientoRepository.get_by_id(id_seguimiento)
        if not seguimiento:
            return None
        contactos = SeguimientoContactoRepository.get_by_seguimiento(id_seguimiento)
        return {
            "seguimiento": seguimiento,
            "contactos": contactos,
        }

    @staticmethod
    def get_all() -> list[Seguimiento]:
        return SeguimientoRepository.get_all()

    @staticmethod
    def get_by_asegurado(id_asegurado: int) -> list[Seguimiento]:
        return SeguimientoRepository.get_by_asegurado(id_asegurado)

    @staticmethod
    def get_by_asegurado_con_contactos(id_asegurado: int) -> list[dict]:
        """Retorna todos los seguimientos de un asegurado con sus contactos."""
        seguimientos = SeguimientoRepository.get_by_asegurado(id_asegurado)
        resultado = []
        for seg in seguimientos:
            contactos = SeguimientoContactoRepository.get_by_seguimiento(seg.id_seguimiento)
            resultado.append({
                "seguimiento": seg,
                "contactos": contactos,
            })
        return resultado

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
        # Soft delete en cascada: primero contactos, luego el seguimiento
        from datetime import datetime
        contactos = SeguimientoContactoRepository.get_by_seguimiento(id_seguimiento)
        for contacto in contactos:
            SeguimientoContactoRepository.delete(contacto.id_contacto)
        return SeguimientoRepository.delete(id_seguimiento)
