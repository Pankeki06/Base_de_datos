from datetime import datetime

from sqlmodel import select

from config.database import create_session
from models.producto_poliza import ProductoPoliza


class ProductoPolizaRepository:
    @staticmethod
    def _not_deleted_filter():
        return ProductoPoliza.deleted_at == None

    @staticmethod
    def create(producto: ProductoPoliza) -> ProductoPoliza:
        with create_session() as session:
            session.add(producto)
            session.commit()
            session.refresh(producto)
            return producto

    @staticmethod
    def get_by_id(id_producto: int) -> ProductoPoliza | None:
        with create_session() as session:
            return session.exec(
                select(ProductoPoliza).where(
                    ProductoPoliza.id_producto == id_producto,
                    ProductoPolizaRepository._not_deleted_filter(),
                )
            ).first()

    @staticmethod
    def get_all() -> list[ProductoPoliza]:
        with create_session() as session:
            return list(
                session.exec(
                    select(ProductoPoliza).where(
                        ProductoPolizaRepository._not_deleted_filter()
                    )
                ).all()
            )

    @staticmethod
    def get_activos() -> list[ProductoPoliza]:
        with create_session() as session:
            return list(
                session.exec(
                    select(ProductoPoliza).where(
                        ProductoPoliza.activo == True,
                        ProductoPolizaRepository._not_deleted_filter(),
                    )
                ).all()
            )

    @staticmethod
    def update(id_producto: int, updated_data: dict) -> ProductoPoliza | None:
        with create_session() as session:
            entity = session.exec(
                select(ProductoPoliza).where(
                    ProductoPoliza.id_producto == id_producto,
                    ProductoPolizaRepository._not_deleted_filter(),
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
    def delete(id_producto: int) -> bool:
        with create_session() as session:
            entity = session.exec(
                select(ProductoPoliza).where(
                    ProductoPoliza.id_producto == id_producto,
                    ProductoPolizaRepository._not_deleted_filter(),
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
