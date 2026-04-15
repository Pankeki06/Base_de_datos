from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.beneficio import Beneficio


class BeneficioRepository:
    @staticmethod
    def create(beneficio: Beneficio) -> Beneficio:
        with create_session() as session:
            session.add(beneficio)
            session.commit()
            session.refresh(beneficio)
            return beneficio

    @staticmethod
    def get_by_id(id_beneficio: int) -> Beneficio | None:
        with create_session() as session:
            return session.exec(
                select(Beneficio).where(Beneficio.id_beneficio == id_beneficio, Beneficio.deleted_at == None)
            ).first()

    @staticmethod
    def get_all() -> list[Beneficio]:
        with create_session() as session:
            return session.exec(select(Beneficio).where(Beneficio.deleted_at == None)).all()

    @staticmethod
    def get_by_poliza(id_poliza: int) -> list[Beneficio]:
        with create_session() as session:
            statement = select(Beneficio).where(
                Beneficio.id_poliza == id_poliza, Beneficio.deleted_at == None
            )
            return list(session.exec(statement).all())

    @staticmethod
    def update(id_beneficio: int, updated_data: dict) -> Beneficio | None:
        with create_session() as session:
            entity = session.exec(
                select(Beneficio).where(Beneficio.id_beneficio == id_beneficio, Beneficio.deleted_at == None)
            ).first()
            if not entity:
                return None
            for key, value in updated_data.items():
                setattr(entity, key, value)
            session.add(entity)
            session.commit()
            session.refresh(entity)
            return entity

    @staticmethod
    def delete(id_beneficio: int) -> bool:
        with create_session() as session:
            entity = session.exec(
                select(Beneficio).where(Beneficio.id_beneficio == id_beneficio, Beneficio.deleted_at == None)
            ).first()
            if not entity:
                return False
            entity.vigente = False
            entity.deleted_at = datetime.now()
            session.add(entity)
            session.commit()
            return True
