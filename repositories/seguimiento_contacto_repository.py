from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.seguimiento_contacto import SeguimientoContacto


class SeguimientoContactoRepository:
    @staticmethod
    def create(contacto: SeguimientoContacto) -> SeguimientoContacto:
        with create_session() as session:
            session.add(contacto)
            session.commit()
            session.refresh(contacto)
            return contacto

    @staticmethod
    def get_by_id(id_contacto: int) -> SeguimientoContacto | None:
        with create_session() as session:
            return session.exec(
                select(SeguimientoContacto).where(
                    SeguimientoContacto.id_contacto == id_contacto,
                    SeguimientoContacto.deleted_at == None,
                )
            ).first()

    @staticmethod
    def get_by_seguimiento(id_seguimiento: int) -> list[SeguimientoContacto]:
        with create_session() as session:
            return list(
                session.exec(
                    select(SeguimientoContacto).where(
                        SeguimientoContacto.id_seguimiento == id_seguimiento,
                        SeguimientoContacto.deleted_at == None,
                    ).order_by(SeguimientoContacto.fecha_hora.asc())
                ).all()
            )

    @staticmethod
    def get_all() -> list[SeguimientoContacto]:
        with create_session() as session:
            return list(
                session.exec(
                    select(SeguimientoContacto).where(SeguimientoContacto.deleted_at == None)
                ).all()
            )

    @staticmethod
    def update(id_contacto: int, updated_data: dict) -> SeguimientoContacto | None:
        with create_session() as session:
            entity = session.exec(
                select(SeguimientoContacto).where(
                    SeguimientoContacto.id_contacto == id_contacto,
                    SeguimientoContacto.deleted_at == None,
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
    def delete(id_contacto: int) -> bool:
        with create_session() as session:
            entity = session.exec(
                select(SeguimientoContacto).where(
                    SeguimientoContacto.id_contacto == id_contacto,
                    SeguimientoContacto.deleted_at == None,
                )
            ).first()
            if not entity:
                return False
            entity.deleted_at = datetime.now()
            entity.updated_at = datetime.now()
            session.add(entity)
            session.commit()
            return True
