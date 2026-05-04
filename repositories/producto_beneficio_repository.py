from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.producto_beneficio import ProductoBeneficio


class ProductoBeneficioRepository:
    @staticmethod
    def _not_deleted_filter():
        return ProductoBeneficio.deleted_at == None

    @staticmethod
    def create(producto_beneficio: ProductoBeneficio) -> ProductoBeneficio:
        with create_session() as session:
            session.add(producto_beneficio)
            session.commit()
            session.refresh(producto_beneficio)
            return producto_beneficio

    @staticmethod
    def get_by_id(id_producto_beneficio: int) -> ProductoBeneficio | None:
        with create_session() as session:
            return session.exec(
                select(ProductoBeneficio).where(
                    ProductoBeneficio.id_producto_beneficio == id_producto_beneficio,
                    ProductoBeneficioRepository._not_deleted_filter(),
                )
            ).first()

    @staticmethod
    def get_all() -> list[ProductoBeneficio]:
        with create_session() as session:
            return list(
                session.exec(
                    select(ProductoBeneficio).where(
                        ProductoBeneficioRepository._not_deleted_filter()
                    )
                ).all()
            )

    @staticmethod
    def get_by_producto(id_producto: int) -> list[ProductoBeneficio]:
        with create_session() as session:
            return list(
                session.exec(
                    select(ProductoBeneficio).where(
                        ProductoBeneficio.id_producto == id_producto,
                        ProductoBeneficio.activo == True,
                        ProductoBeneficioRepository._not_deleted_filter(),
                    )
                ).all()
            )

    @staticmethod
    def update(id_producto_beneficio: int, updated_data: dict) -> ProductoBeneficio | None:
        with create_session() as session:
            entity = session.exec(
                select(ProductoBeneficio).where(
                    ProductoBeneficio.id_producto_beneficio == id_producto_beneficio,
                    ProductoBeneficioRepository._not_deleted_filter(),
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
    def delete(id_producto_beneficio: int) -> bool:
        with create_session() as session:
            entity = session.exec(
                select(ProductoBeneficio).where(
                    ProductoBeneficio.id_producto_beneficio == id_producto_beneficio,
                    ProductoBeneficioRepository._not_deleted_filter(),
                )
            ).first()
            if not entity:
                return False
            entity.activo = False
            entity.deleted_at = datetime.now()
            entity.updated_at = datetime.now()
            session.add(entity)
            session.commit()
            return True
