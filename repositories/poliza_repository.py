from datetime import datetime

from sqlmodel import func, select

from config.database import create_session
from models.asegurado import Asegurado
from models.asegurado_poliza import AseguradoPoliza
from models.beneficio import Beneficio
from models.poliza import Poliza
from models.producto_beneficio import ProductoBeneficio


class PolizaRepository:
    @staticmethod
    def count_by_agente_responsable(id_agente: int) -> int:
        with create_session() as session:
            statement = (
                select(func.count())
                .select_from(Poliza)
                .join(Asegurado, Asegurado.id_asegurado == Poliza.id_asegurado)
                .where(
                    Asegurado.id_agente_responsable == id_agente,
                    Asegurado.deleted_at == None,
                    Poliza.deleted_at == None,
                )
            )
            total = session.exec(statement).one()
            return int(total or 0)

    @staticmethod
    def create(
        poliza: Poliza,
        selected_producto_beneficio_ids: list[int] | None = None,
    ) -> Poliza:
        with create_session() as session:
            session.add(poliza)
            session.flush()

            # Mantiene sincronizada la relacion de personas cubiertas
            # para que siempre exista titular al crear una poliza.
            titular = session.exec(
                select(AseguradoPoliza).where(
                    AseguradoPoliza.id_poliza == poliza.id_poliza,
                    AseguradoPoliza.id_asegurado == poliza.id_asegurado,
                    AseguradoPoliza.deleted_at == None,
                )
            ).first()
            if not titular:
                session.add(
                    AseguradoPoliza(
                        id_poliza=poliza.id_poliza,
                        id_asegurado=poliza.id_asegurado,
                        tipo_participante="titular",
                    )
                )

            beneficios_query = select(ProductoBeneficio).where(
                ProductoBeneficio.id_producto == poliza.id_producto,
                ProductoBeneficio.activo == True,
                ProductoBeneficio.deleted_at == None,
            )
            if selected_producto_beneficio_ids is None:
                beneficios_a_copiar = list(
                    session.exec(
                        beneficios_query.where(ProductoBeneficio.incluido_base == True)
                    ).all()
                )
            elif selected_producto_beneficio_ids:
                beneficios_a_copiar = list(
                    session.exec(
                        beneficios_query.where(
                            ProductoBeneficio.id_producto_beneficio.in_(selected_producto_beneficio_ids)
                        )
                    ).all()
                )
            else:
                beneficios_a_copiar = []

            if beneficios_a_copiar:
                session.add_all(
                    [
                        Beneficio(
                            id_poliza=poliza.id_poliza,
                            id_producto_beneficio=beneficio.id_producto_beneficio,
                            nombre_beneficio=beneficio.nombre_beneficio,
                            descripcion=beneficio.descripcion,
                            monto_cobertura=beneficio.monto_cobertura,
                            costo_aplicado=(
                                0.0
                                if getattr(beneficio, "incluido_base", True)
                                else float(getattr(beneficio, "costo_extra", 0) or 0)
                            ),
                        )
                        for beneficio in beneficios_a_copiar
                    ]
                )

            session.commit()
            session.refresh(poliza)
            session.expunge(poliza)
            return poliza

    @staticmethod
    def get_by_id(id_poliza: int) -> Poliza | None:
        with create_session() as session:
            return session.exec(select(Poliza).where(Poliza.id_poliza == id_poliza, Poliza.deleted_at == None)).first()

    @staticmethod
    def get_by_numero(numero_poliza: str) -> Poliza | None:
        with create_session() as session:
            return session.exec(
                select(Poliza).where(Poliza.numero_poliza == numero_poliza, Poliza.deleted_at == None)
            ).first()

    @staticmethod
    def get_all() -> list[Poliza]:
        with create_session() as session:
            return session.exec(select(Poliza).where(Poliza.deleted_at == None)).all()

    @staticmethod
    def get_by_asegurado(id_asegurado: int) -> list[Poliza]:
        with create_session() as session:
            statement = select(Poliza).where(
                Poliza.id_asegurado == id_asegurado, Poliza.deleted_at == None
            )
            return list(session.exec(statement).all())

    @staticmethod
    def get_active_for_asegurado_producto(id_asegurado: int, id_producto: int) -> Poliza | None:
        with create_session() as session:
            statement = (
                select(Poliza)
                .join(AseguradoPoliza, AseguradoPoliza.id_poliza == Poliza.id_poliza)
                .where(
                    AseguradoPoliza.id_asegurado == id_asegurado,
                    AseguradoPoliza.deleted_at == None,
                    Poliza.id_producto == id_producto,
                    Poliza.estatus == "activa",
                    Poliza.deleted_at == None,
                )
            )
            return session.exec(statement).first()

    @staticmethod
    def get_participantes_by_poliza(id_poliza: int) -> list[dict]:
        with create_session() as session:
            statement = (
                select(AseguradoPoliza, Asegurado)
                .join(Asegurado, Asegurado.id_asegurado == AseguradoPoliza.id_asegurado)
                .where(
                    AseguradoPoliza.id_poliza == id_poliza,
                    AseguradoPoliza.deleted_at == None,
                    Asegurado.deleted_at == None,
                )
            )
            rows = session.exec(statement).all()

            participantes = []
            for ap, a in rows:
                nombre = f"{a.nombre} {a.apellido_paterno} {a.apellido_materno}".strip()
                participantes.append(
                    {
                        "id_asegurado_poliza": ap.id_asegurado_poliza,
                        "id_asegurado": a.id_asegurado,
                        "tipo_participante": ap.tipo_participante,
                        "nombre_completo": nombre,
                        "rfc": a.rfc,
                        "correo": a.correo,
                        "celular": a.celular,
                    }
                )

            return participantes

    @staticmethod
    def get_participante_by_id(id_asegurado_poliza: int) -> AseguradoPoliza | None:
        with create_session() as session:
            return session.exec(
                select(AseguradoPoliza).where(
                    AseguradoPoliza.id_asegurado_poliza == id_asegurado_poliza,
                    AseguradoPoliza.deleted_at == None,
                )
            ).first()

    @staticmethod
    def get_participaciones_by_asegurado(id_asegurado: int) -> list[dict]:
        with create_session() as session:
            statement = (
                select(AseguradoPoliza, Poliza)
                .join(Poliza, Poliza.id_poliza == AseguradoPoliza.id_poliza)
                .where(
                    AseguradoPoliza.id_asegurado == id_asegurado,
                    AseguradoPoliza.deleted_at == None,
                    Poliza.deleted_at == None,
                )
            )
            rows = session.exec(statement).all()

            participaciones = []
            for ap, poliza in rows:
                participaciones.append(
                    {
                        "id_poliza": poliza.id_poliza,
                        "numero_poliza": poliza.numero_poliza,
                        "estatus_poliza": poliza.estatus,
                        "tipo_participante": ap.tipo_participante,
                    }
                )

            return participaciones

    @staticmethod
    def get_available_for_participante(id_asegurado: int) -> list[Poliza]:
        with create_session() as session:
            linked_rows = session.exec(
                select(AseguradoPoliza.id_poliza).where(
                    AseguradoPoliza.id_asegurado == id_asegurado,
                    AseguradoPoliza.deleted_at == None,
                )
            ).all()
            linked_ids = set(linked_rows)

            productos_activos_cubiertos = set(
                session.exec(
                    select(Poliza.id_producto)
                    .join(AseguradoPoliza, AseguradoPoliza.id_poliza == Poliza.id_poliza)
                    .where(
                        AseguradoPoliza.id_asegurado == id_asegurado,
                        AseguradoPoliza.deleted_at == None,
                        Poliza.deleted_at == None,
                        Poliza.estatus == "activa",
                    )
                ).all()
            )

            polizas_activas = session.exec(
                select(Poliza).where(
                    Poliza.deleted_at == None,
                    Poliza.estatus == "activa",
                    Poliza.id_asegurado != id_asegurado,
                )
            ).all()

            return [
                p
                for p in polizas_activas
                if p.id_poliza not in linked_ids and p.id_producto not in productos_activos_cubiertos
            ]

    @staticmethod
    def add_participante(id_poliza: int, id_asegurado: int, tipo_participante: str) -> AseguradoPoliza:
        with create_session() as session:
            poliza = session.exec(
                select(Poliza).where(
                    Poliza.id_poliza == id_poliza,
                    Poliza.deleted_at == None,
                )
            ).first()
            if not poliza:
                raise ValueError("La póliza seleccionada no existe o no está disponible.")

            asegurado = session.exec(
                select(Asegurado).where(
                    Asegurado.id_asegurado == id_asegurado,
                    Asegurado.deleted_at == None,
                )
            ).first()
            if not asegurado:
                raise ValueError("El asegurado no existe o no está disponible.")

            current = session.exec(
                select(AseguradoPoliza).where(
                    AseguradoPoliza.id_poliza == id_poliza,
                    AseguradoPoliza.id_asegurado == id_asegurado,
                )
            ).first()

            if current and current.deleted_at is None:
                raise ValueError("El asegurado ya está vinculado a esta póliza.")

            if current:
                current.tipo_participante = tipo_participante
                current.deleted_at = None
                session.add(current)
                session.commit()
                session.refresh(current)
                return current

            relacion = AseguradoPoliza(
                id_poliza=id_poliza,
                id_asegurado=id_asegurado,
                tipo_participante=tipo_participante,
            )
            session.add(relacion)
            session.commit()
            session.refresh(relacion)
            return relacion

    @staticmethod
    def update(id_poliza: int, updated_data: dict) -> Poliza | None:
        with create_session() as session:
            entity = session.exec(select(Poliza).where(Poliza.id_poliza == id_poliza, Poliza.deleted_at == None)).first()
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
    def delete(id_poliza: int) -> bool:
        with create_session() as session:
            entity = session.exec(select(Poliza).where(Poliza.id_poliza == id_poliza, Poliza.deleted_at == None)).first()
            if not entity:
                return False
            now = datetime.now()
            entity.deleted_at = now
            entity.updated_at = now
            session.add(entity)
            # Cascade soft delete to all active beneficios of this poliza
            beneficios = session.exec(
                select(Beneficio).where(
                    Beneficio.id_poliza == id_poliza,
                    Beneficio.deleted_at == None,
                )
            ).all()
            for b in beneficios:
                b.deleted_at = now
                b.vigente = False
                session.add(b)
            session.commit()
            return True
