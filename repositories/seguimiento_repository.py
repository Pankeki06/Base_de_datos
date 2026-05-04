from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.seguimiento import Seguimiento


class SeguimientoRepository:
    @staticmethod
    def create(seguimiento: Seguimiento) -> Seguimiento:
        with create_session() as session:
            session.add(seguimiento)
            session.commit()
            session.refresh(seguimiento)
            return seguimiento

    @staticmethod
    def get_by_id(id_seguimiento: int) -> Seguimiento | None:
        with create_session() as session:
            return session.exec(
                select(Seguimiento).where(Seguimiento.id_seguimiento == id_seguimiento, Seguimiento.deleted_at == None)
            ).first()

    @staticmethod
    def get_all() -> list[Seguimiento]:
        with create_session() as session:
            return session.exec(select(Seguimiento).where(Seguimiento.deleted_at == None)).all()

    @staticmethod
    def get_by_asegurado(id_asegurado: int) -> list[Seguimiento]:
        with create_session() as session:
            statement = select(Seguimiento).where(
                Seguimiento.id_asegurado == id_asegurado,
                Seguimiento.deleted_at == None,
            ).order_by(Seguimiento.fecha_hora.desc())
            return list(session.exec(statement).all())

    @staticmethod
    def update(id_seguimiento: int, updated_data: dict) -> Seguimiento | None:
        with create_session() as session:
            entity = session.exec(
                select(Seguimiento).where(Seguimiento.id_seguimiento == id_seguimiento, Seguimiento.deleted_at == None)
            ).first()
            if not entity:
                return None
            for key, value in updated_data.items():
                setattr(entity, key, value)
            entity.updated_at = datetime.now()
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    @staticmethod
    def delete(id_seguimiento: int) -> bool:
        with create_session() as session:
            entity = session.exec(
                select(Seguimiento).where(Seguimiento.id_seguimiento == id_seguimiento, Seguimiento.deleted_at == None)
            ).first()
            if not entity:
                return False
            entity.deleted_at = datetime.now()
            session.add(entity)
            session.commit()
            return True
