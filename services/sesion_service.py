from datetime import datetime

from models.sesion import Sesion
from repositories.sesion_repository import SesionRepository


class SesionService:
    @staticmethod
    def create(data: dict) -> Sesion:
        if "inicio_sesion" not in data:
            data["inicio_sesion"] = datetime.now()
        return SesionRepository.create(Sesion(**data))

    @staticmethod
    def get_by_id(id_sesion: int) -> Sesion | None:
        return SesionRepository.get_by_id(id_sesion)

    @staticmethod
    def get_all() -> list[Sesion]:
        return SesionRepository.get_all()

    @staticmethod
    def update(id_sesion: int, data: dict) -> Sesion | None:
        return SesionRepository.update(id_sesion, data)

    @staticmethod
    def delete(id_sesion: int) -> bool:
        return SesionRepository.delete(id_sesion)
