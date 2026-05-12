from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.asegurado import Asegurado
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
        """Retorna beneficiarios de un asegurado (titular o dependiente)."""
        with create_session() as session:
            return list(
                session.exec(
                    select(Beneficiario).where(
                        Beneficiario.id_asegurado == id_asegurado,
                        Beneficiario.deleted_at == None,
                    )
                ).all()
            )

    @staticmethod
    def get_by_poliza(id_poliza: int) -> list[Beneficiario]:
        """Retorna todos los beneficiarios de una póliza (titular + dependientes)."""
        with create_session() as session:
            return list(
                session.exec(
                    select(Beneficiario).where(
                        Beneficiario.id_poliza == id_poliza,
                        Beneficiario.deleted_at == None,
                    )
                ).all()
            )

    @staticmethod
    def get_beneficiarios_titular(id_poliza: int) -> list[Beneficiario]:
        """Retorna beneficiarios del titular de una póliza."""
        with create_session() as session:
            # Buscar el titular de la póliza
            from models.poliza import Poliza
            poliza = session.exec(
                select(Poliza).where(Poliza.id_poliza == id_poliza)
            ).first()
            if not poliza:
                return []
            
            return list(
                session.exec(
                    select(Beneficiario).where(
                        Beneficiario.id_poliza == id_poliza,
                        Beneficiario.id_asegurado == poliza.id_asegurado,
                        Beneficiario.deleted_at == None,
                    )
                ).all()
            )

    @staticmethod
    def get_beneficiarios_dependiente(id_poliza: int, id_asegurado_dependiente: int) -> list[Beneficiario]:
        """Retorna beneficiarios de un dependiente específico en una póliza."""
        with create_session() as session:
            return list(
                session.exec(
                    select(Beneficiario).where(
                        Beneficiario.id_poliza == id_poliza,
                        Beneficiario.id_asegurado == id_asegurado_dependiente,
                        Beneficiario.deleted_at == None,
                    )
                ).all()
            )

    @staticmethod
    def get_total_porcentaje_by_poliza(
        id_poliza: int,
        *,
        exclude_id: int | None = None,
    ) -> float:
        """Suma de porcentajes de beneficiarios por póliza (todos: titular + dependientes)."""
        with create_session() as session:
            statement = select(Beneficiario).where(
                Beneficiario.id_poliza == id_poliza,
                Beneficiario.deleted_at == None,
            )
            if exclude_id is not None:
                statement = statement.where(Beneficiario.id_beneficiario != exclude_id)
            beneficiarios = session.exec(statement).all()
            return float(sum(b.porcentaje_participacion for b in beneficiarios))

    @staticmethod
    def get_total_porcentaje_by_asegurado(
        id_poliza: int,
        id_asegurado: int,
        *,
        exclude_id: int | None = None,
    ) -> float:
        """Suma de porcentajes de beneficiarios de un asegurado específico en una póliza."""
        with create_session() as session:
            statement = select(Beneficiario).where(
                Beneficiario.id_poliza == id_poliza,
                Beneficiario.id_asegurado == id_asegurado,
                Beneficiario.deleted_at == None,
            )
            if exclude_id is not None:
                statement = statement.where(Beneficiario.id_beneficiario != exclude_id)
            beneficiarios = session.exec(statement).all()
            return float(sum(b.porcentaje_participacion for b in beneficiarios))

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
