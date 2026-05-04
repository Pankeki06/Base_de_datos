from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.beneficiario import Beneficiario


class BeneficiarioRepository:
    @staticmethod
    def create(beneficiario: Beneficiario) -> Beneficiario:
        with create_session() as session:
            session.add(beneficiario)
            session.commit()
            session.refresh(beneficiario)
            return beneficiario

    @staticmethod
    def get_by_id(id_beneficiario: int) -> Beneficiario | None:
        with create_session() as session:
            return session.exec(
                select(Beneficiario).where(Beneficiario.id_beneficiario == id_beneficiario, Beneficiario.deleted_at == None)
            ).first()

    @staticmethod
    def get_all() -> list[Beneficiario]:
        with create_session() as session:
            return session.exec(select(Beneficiario).where(Beneficiario.deleted_at == None)).all()

    @staticmethod
    def get_by_asegurado(id_asegurado: int) -> list[Beneficiario]:
        with create_session() as session:
            statement = select(Beneficiario).where(
                Beneficiario.id_asegurado == id_asegurado,
                Beneficiario.deleted_at == None,
            )
            return list(session.exec(statement).all())

    @staticmethod
    def get_total_porcentaje_by_asegurado(
        id_asegurado: int,
        *,
        id_poliza: int | None = None,
        exclude_id: int | None = None,
    ) -> float:
        with create_session() as session:
            statement = select(Beneficiario).where(
                Beneficiario.id_asegurado == id_asegurado,
                Beneficiario.deleted_at == None,
            )
            if id_poliza is not None:
                statement = statement.where(Beneficiario.id_poliza == id_poliza)
            if exclude_id is not None:
                statement = statement.where(Beneficiario.id_beneficiario != exclude_id)
            beneficiarios = session.exec(statement).all()
            return float(sum(beneficiario.porcentaje_participacion for beneficiario in beneficiarios))

    @staticmethod
    def update(id_beneficiario: int, updated_data: dict) -> Beneficiario | None:
        with create_session() as session:
            entity = session.exec(
                select(Beneficiario).where(Beneficiario.id_beneficiario == id_beneficiario, Beneficiario.deleted_at == None)
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
    def delete(id_beneficiario: int) -> bool:
        with create_session() as session:
            entity = session.exec(
                select(Beneficiario).where(Beneficiario.id_beneficiario == id_beneficiario, Beneficiario.deleted_at == None)
            ).first()
            if not entity:
                return False
            entity.deleted_at = datetime.now()
            session.add(entity)
            session.commit()
            return True
