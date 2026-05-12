from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.beneficio import Beneficio
from models.producto_beneficio import ProductoBeneficio


class BeneficioRepository:
    @staticmethod
    def _non_deleted_filters():
        return (Beneficio.deleted_at == None,)

    @staticmethod
    def _active_filters():
        return (*BeneficioRepository._non_deleted_filters(), Beneficio.vigente == True)

    @staticmethod
    def _enrich(beneficio: Beneficio, pb_row) -> None:
        """Enriquece el beneficio con datos del catálogo."""
        if pb_row:
            object.__setattr__(beneficio, "nombre_beneficio", pb_row.nombre_beneficio)
            object.__setattr__(beneficio, "descripcion", pb_row.descripcion)
            object.__setattr__(beneficio, "monto_cobertura", float(pb_row.monto_cobertura or 0))
        else:
            object.__setattr__(beneficio, "nombre_beneficio", None)
            object.__setattr__(beneficio, "descripcion", None)
            object.__setattr__(beneficio, "monto_cobertura", 0.0)

    @staticmethod
    def _enriched_query(*where_clauses):
        return (
            select(Beneficio, ProductoBeneficio)
            .join(
                ProductoBeneficio,
                ProductoBeneficio.id_producto_beneficio == Beneficio.id_producto_beneficio,
            )
            .where(*where_clauses)
        )

    @staticmethod
    def create(beneficio: Beneficio) -> Beneficio:
        with create_session() as session:
            session.add(beneficio)
            session.commit()
            session.refresh(beneficio)
            pb = session.get(ProductoBeneficio, beneficio.id_producto_beneficio)
            BeneficioRepository._enrich(beneficio, pb)
            return beneficio

    @staticmethod
    def get_by_id(id_beneficio: int) -> Beneficio | None:
        with create_session() as session:
            row = session.execute(
                BeneficioRepository._enriched_query(
                    Beneficio.id_beneficio == id_beneficio,
                    *BeneficioRepository._non_deleted_filters(),
                )
            ).first()
            if not row:
                return None
            beneficio, pb = row[0], row[1]
            BeneficioRepository._enrich(beneficio, pb)
            return beneficio

    @staticmethod
    def get_all() -> list[Beneficio]:
        with create_session() as session:
            rows = session.execute(
                BeneficioRepository._enriched_query(
                    *BeneficioRepository._active_filters()
                )
            ).all()
            result = []
            for row in rows:
                beneficio, pb = row[0], row[1]
                BeneficioRepository._enrich(beneficio, pb)
                result.append(beneficio)
            return result

    @staticmethod
    def get_by_poliza(id_poliza: int, *, include_inactive: bool = False) -> list[Beneficio]:
        with create_session() as session:
            filters = (
                BeneficioRepository._non_deleted_filters()
                if include_inactive
                else BeneficioRepository._active_filters()
            )
            rows = session.execute(
                BeneficioRepository._enriched_query(
                    Beneficio.id_poliza == id_poliza,
                    *filters,
                )
            ).all()
            result = []
            for row in rows:
                beneficio, pb = row[0], row[1]
                BeneficioRepository._enrich(beneficio, pb)
                result.append(beneficio)
            return result

    @staticmethod
    def update(id_beneficio: int, updated_data: dict) -> Beneficio | None:
        with create_session() as session:
            row = session.execute(
                BeneficioRepository._enriched_query(
                    Beneficio.id_beneficio == id_beneficio,
                    *BeneficioRepository._non_deleted_filters(),
                )
            ).first()
            if not row:
                return None
            entity, pb = row[0], row[1]
            for key, value in updated_data.items():
                setattr(entity, key, value)
            session.add(entity)
            session.commit()
            session.refresh(entity)
            pb = session.get(ProductoBeneficio, entity.id_producto_beneficio)
            BeneficioRepository._enrich(entity, pb)
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
