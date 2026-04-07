from datetime import datetime

from sqlmodel import select
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