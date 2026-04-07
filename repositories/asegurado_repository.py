from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.asegurado import Asegurado


class AseguradoRepository:
    @staticmethod
    def create(asegurado: Asegurado) -> Asegurado:
        with create_session() as session:
            session.add(asegurado)
            session.commit()
            session.refresh(asegurado)
            return asegurado

    @staticmethod
    def get_by_id(id_asegurado: int) -> Asegurado | None:
        with create_session() as session:
            statement = select(Asegurado).where(Asegurado.id_asegurado == id_asegurado, Asegurado.deleted_at == None)
            return session.exec(statement).first()

    @staticmethod
    def get_by_rfc(rfc: str) -> Asegurado | None:
        with create_session() as session:
            return session.exec(select(Asegurado).where(Asegurado.rfc == rfc, Asegurado.deleted_at == None)).first()

    @staticmethod
    def get_all() -> list[Asegurado]:
        with create_session() as session:
            return session.exec(select(Asegurado).where(Asegurado.deleted_at == None)).all()

    @staticmethod
    def update(id_asegurado: int, updated_data: dict) -> Asegurado | None:
        with create_session() as session:
            entity = session.exec(
                select(Asegurado).where(Asegurado.id_asegurado == id_asegurado, Asegurado.deleted_at == None)
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
    def delete(id_asegurado: int) -> bool:
        with create_session() as session:
            entity = session.exec(
                select(Asegurado).where(Asegurado.id_asegurado == id_asegurado, Asegurado.deleted_at == None)
            ).first()
            if not entity:
                return False
            entity.activo = False
            entity.deleted_at = datetime.now()
            entity.updated_at = datetime.now()
            session.add(entity)
            session.commit()
            return True
