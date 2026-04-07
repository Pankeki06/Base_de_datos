from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.poliza import Poliza


class PolizaRepository:
    @staticmethod
    def create(poliza: Poliza) -> Poliza:
        with create_session() as session:
            session.add(poliza)
            session.commit()
            session.refresh(poliza)
            return poliza

    @staticmethod
    def get_by_id(id_poliza: int) -> Poliza | None:
        with create_session() as session:
            return session.exec(select(Poliza).where(Poliza.id_poliza == id_poliza, Poliza.deleted_at == None)).first()

    @staticmethod
    def get_by_numero(numero_poliza: str) -> Poliza | None:
        with create_session() as session:
            return session.exec(
                select(Poliza).where(Poliza.numero_poliza == numero_poliza, Poliza.deleted_at == None)
            ).first()

    @staticmethod
    def get_all() -> list[Poliza]:
        with create_session() as session:
            return session.exec(select(Poliza).where(Poliza.deleted_at == None)).all()

    @staticmethod
    def update(id_poliza: int, updated_data: dict) -> Poliza | None:
        with create_session() as session:
            entity = session.exec(select(Poliza).where(Poliza.id_poliza == id_poliza, Poliza.deleted_at == None)).first()
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
    def delete(id_poliza: int) -> bool:
        with create_session() as session:
            entity = session.exec(select(Poliza).where(Poliza.id_poliza == id_poliza, Poliza.deleted_at == None)).first()
            if not entity:
                return False
            entity.deleted_at = datetime.now()
            entity.updated_at = datetime.now()
            session.add(entity)
            session.commit()
            return True
