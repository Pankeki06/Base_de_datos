from datetime import datetime

from sqlmodel import func, or_, select
from config.database import create_session
from models.agente import Agente


class AgenteRepository:
    @staticmethod
    def create_agente(agente: Agente) -> Agente:
        with create_session() as session:
            session.add(agente)
            session.commit()
            session.refresh(agente)
            return agente

    @staticmethod
    def get_agente_by_id(id_agente: int) -> Agente | None:
        with create_session() as session:
            statement = select(Agente).where(Agente.id_agente == id_agente, Agente.deleted_at == None)
            return session.exec(statement).first()

    @staticmethod
    def get_agente_by_clave(clave_agente: str) -> Agente | None:
        with create_session() as session:
            statement = select(Agente).where(Agente.clave_agente == clave_agente, Agente.deleted_at == None)
            return session.exec(statement).first()

    @staticmethod
    def get_agente_by_correo(correo: str) -> Agente | None:
        with create_session() as session:
            statement = select(Agente).where(Agente.correo == correo, Agente.deleted_at == None)
            return session.exec(statement).first()

    @staticmethod
    def get_all_agentes() -> list[Agente]:
        with create_session() as session:
            return session.exec(select(Agente).where(Agente.deleted_at == None)).all()

    @staticmethod
    def get_agentes_page(page: int = 1, page_size: int = 20, nombre_query: str = "") -> list[Agente]:
        with create_session() as session:
            offset = (page - 1) * page_size
            statement = select(Agente).where(Agente.deleted_at == None)
            if nombre_query:
                statement = statement.where(
                    or_(
                        Agente.nombre.ilike(f"%{nombre_query}%"),
                        Agente.apellido_paterno.ilike(f"%{nombre_query}%"),
                        Agente.apellido_materno.ilike(f"%{nombre_query}%"),
                    )
                )
            statement = statement.order_by(Agente.id_agente.desc()).offset(offset).limit(page_size)
            return session.exec(statement).all()

    @staticmethod
    def count_agentes(nombre_query: str = "") -> int:
        with create_session() as session:
            statement = select(func.count()).select_from(Agente).where(Agente.deleted_at == None)
            if nombre_query:
                statement = statement.where(
                    or_(
                        Agente.nombre.ilike(f"%{nombre_query}%"),
                        Agente.apellido_paterno.ilike(f"%{nombre_query}%"),
                        Agente.apellido_materno.ilike(f"%{nombre_query}%"),
                    )
                )
            total = session.exec(statement).one()
            return int(total or 0)

    @staticmethod
    def update_agente(id_agente: int, updated_data: dict) -> Agente | None:
        with create_session() as session:
            statement = select(Agente).where(Agente.id_agente == id_agente, Agente.deleted_at == None)
            agente = session.exec(statement).first()
            if not agente:
                return None
            for key, value in updated_data.items():
                setattr(agente, key, value)
            agente.updated_at = datetime.now()
            session.add(agente)
            session.commit()
            session.refresh(agente)
            return agente

    @staticmethod
    def delete_agente(id_agente: int) -> bool:
        with create_session() as session:
            statement = select(Agente).where(Agente.id_agente == id_agente, Agente.deleted_at == None)
            agente = session.exec(statement).first()
            if not agente:
                return False
            agente.deleted_at = datetime.now()
            agente.updated_at = datetime.now()
            session.add(agente)
            session.commit()
            return True

    @staticmethod
    def get_agentes_desactivados_page(page: int = 1, page_size: int = 20, nombre_query: str = "") -> list[Agente]:
        with create_session() as session:
            offset = (page - 1) * page_size
            statement = select(Agente).where(Agente.deleted_at != None)
            if nombre_query:
                statement = statement.where(
                    or_(
                        Agente.nombre.ilike(f"%{nombre_query}%"),
                        Agente.apellido_paterno.ilike(f"%{nombre_query}%"),
                        Agente.apellido_materno.ilike(f"%{nombre_query}%"),
                    )
                )
            statement = statement.order_by(Agente.deleted_at.desc()).offset(offset).limit(page_size)
            return session.exec(statement).all()

    @staticmethod
    def count_agentes_desactivados(nombre_query: str = "") -> int:
        with create_session() as session:
            statement = select(func.count()).select_from(Agente).where(Agente.deleted_at != None)
            if nombre_query:
                statement = statement.where(
                    or_(
                        Agente.nombre.ilike(f"%{nombre_query}%"),
                        Agente.apellido_paterno.ilike(f"%{nombre_query}%"),
                        Agente.apellido_materno.ilike(f"%{nombre_query}%"),
                    )
                )
            total = session.exec(statement).one()
            return int(total or 0)

    @staticmethod
    def reactivate_agente(id_agente: int) -> bool:
        with create_session() as session:
            statement = select(Agente).where(Agente.id_agente == id_agente, Agente.deleted_at != None)
            agente = session.exec(statement).first()
            if not agente:
                return False
            agente.deleted_at = None
            agente.updated_at = datetime.now()
            session.add(agente)
            session.commit()
            return True