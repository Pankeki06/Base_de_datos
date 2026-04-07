from sqlmodel import select

from config.database import create_session
from models.sesion import Sesion


class SesionRepository:
    @staticmethod
    def create(sesion_data: Sesion) -> Sesion:
        with create_session() as session:
            session.add(sesion_data)
            session.commit()
            session.refresh(sesion_data)
            return sesion_data

    @staticmethod
    def get_by_id(id_sesion: int) -> Sesion | None:
        with create_session() as session:
            return session.exec(select(Sesion).where(Sesion.id_sesion == id_sesion)).first()

    @staticmethod
    def get_all() -> list[Sesion]:
        with create_session() as session:
            return session.exec(select(Sesion)).all()

    @staticmethod
    def update(id_sesion: int, updated_data: dict) -> Sesion | None:
        with create_session() as session:
            entity = session.exec(select(Sesion).where(Sesion.id_sesion == id_sesion)).first()
            if not entity:
                return None
            for key, value in updated_data.items():
                setattr(entity, key, value)
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    @staticmethod
    def delete(id_sesion: int) -> bool:
        with create_session() as session:
            entity = session.exec(select(Sesion).where(Sesion.id_sesion == id_sesion)).first()
            if not entity:
                return False
            session.delete(entity)
            session.commit()
            return True
