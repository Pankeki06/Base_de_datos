from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.beneficio import Beneficio


class BeneficioRepository:
    @staticmethod
    def _non_deleted_filters():
        return (Beneficio.deleted_at == None,)

    @staticmethod
    def _active_filters():
        return (*BeneficioRepository._non_deleted_filters(), Beneficio.vigente == True)

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
                select(Beneficio).where(
                    Beneficio.id_beneficio == id_beneficio,
                    *BeneficioRepository._non_deleted_filters(),
                )
            ).first()

    @staticmethod
    def get_all() -> list[Beneficio]:
        with create_session() as session:
            return session.exec(
                select(Beneficio).where(*BeneficioRepository._active_filters())
            ).all()

    @staticmethod
    def get_by_poliza(id_poliza: int, *, include_inactive: bool = False) -> list[Beneficio]:
        with create_session() as session:
            filters = (
                BeneficioRepository._non_deleted_filters()
                if include_inactive
                else BeneficioRepository._active_filters()
            )
            statement = select(Beneficio).where(
                Beneficio.id_poliza == id_poliza,
                *filters,
            )
            return list(session.exec(statement).all())

    @staticmethod
    def update(id_beneficio: int, updated_data: dict) -> Beneficio | None:
        with create_session() as session:
            entity = session.exec(
                select(Beneficio).where(
                    Beneficio.id_beneficio == id_beneficio,
                    *BeneficioRepository._non_deleted_filters(),
                )
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
                select(Beneficio).where(
                    Beneficio.id_beneficio == id_beneficio,
                    *BeneficioRepository._non_deleted_filters(),
                )
            ).first()
            if not entity:
                return False
            entity.deleted_at = datetime.now()
            entity.vigente = False
            session.add(entity)
            session.commit()
            return True
