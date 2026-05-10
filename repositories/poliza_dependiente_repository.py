from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.poliza_dependiente import PolizaDependiente


class PolizaDependienteRepository:
    @staticmethod
    def create(relacion: PolizaDependiente) -> PolizaDependiente:
        with create_session() as session:
            session.add(relacion)
            session.commit()
            session.refresh(relacion)
            return relacion

    @staticmethod
    def get_by_id(id_poliza_dependiente: int) -> PolizaDependiente | None:
        with create_session() as session:
            return session.exec(
                select(PolizaDependiente).where(
                    PolizaDependiente.id_poliza_dependiente == id_poliza_dependiente,
                    PolizaDependiente.deleted_at == None,
                )
            ).first()

    @staticmethod
    def get_by_poliza(id_poliza: int) -> list[PolizaDependiente]:
        with create_session() as session:
            return list(
                session.exec(
                    select(PolizaDependiente).where(
                        PolizaDependiente.id_poliza == id_poliza,
                        PolizaDependiente.deleted_at == None,
                    )
                ).all()
            )

    @staticmethod
    def get_by_asegurado(id_asegurado: int) -> list[PolizaDependiente]:
        with create_session() as session:
            return list(
                session.exec(
                    select(PolizaDependiente).where(
                        PolizaDependiente.id_asegurado == id_asegurado,
                        PolizaDependiente.deleted_at == None,
                    )
                ).all()
            )

    @staticmethod
    def get_by_poliza_and_asegurado(id_poliza: int, id_asegurado: int) -> PolizaDependiente | None:
        with create_session() as session:
            return session.exec(
                select(PolizaDependiente).where(
                    PolizaDependiente.id_poliza == id_poliza,
                    PolizaDependiente.id_asegurado == id_asegurado,
                )
            ).first()

    @staticmethod
    def update(id_poliza_dependiente: int, updated_data: dict) -> PolizaDependiente | None:
        with create_session() as session:
            entity = session.exec(
                select(PolizaDependiente).where(
                    PolizaDependiente.id_poliza_dependiente == id_poliza_dependiente,
                    PolizaDependiente.deleted_at == None,
                )
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
    def delete(id_poliza_dependiente: int) -> bool:
        with create_session() as session:
            entity = session.exec(
                select(PolizaDependiente).where(
                    PolizaDependiente.id_poliza_dependiente == id_poliza_dependiente,
                    PolizaDependiente.deleted_at == None,
                )
            ).first()
            if not entity:
                return False
            entity.deleted_at = datetime.now()
            entity.updated_at = datetime.now()
            session.add(entity)
            session.commit()
            return True
