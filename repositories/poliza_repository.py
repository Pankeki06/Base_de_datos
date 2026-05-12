from datetime import datetime

from sqlmodel import func, select

from config.database import create_session
from models.asegurado import Asegurado
from models.beneficiario import Beneficiario
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
                .where(
                    Poliza.id_asegurado == id_asegurado,
                    Poliza.id_producto == id_producto,
                    Poliza.estatus == "activa",
                    Poliza.deleted_at == None,
                )
            )
            return session.exec(statement).first()

    @staticmethod
    def get_participantes_by_poliza(id_poliza: int) -> list[dict]:
        """Retorna titular + dependientes de una póliza."""
        with create_session() as session:
            poliza = session.exec(
                select(Poliza).where(Poliza.id_poliza == id_poliza, Poliza.deleted_at == None)
            ).first()
            if not poliza:
                return []

            # Titular
            asegurado = session.exec(
                select(Asegurado).where(Asegurado.id_asegurado == poliza.id_asegurado, Asegurado.deleted_at == None)
            ).first()

            participantes = []
            if asegurado:
                nombre = f"{asegurado.nombre} {asegurado.apellido_paterno} {asegurado.apellido_materno}".strip()
                participantes.append({
                    "id_asegurado": asegurado.id_asegurado,
                    "tipo_asegurado": "titular",
                    "parentesco": "titular",
                    "nombre_completo": nombre,
                    "rfc": asegurado.rfc,
                    "correo": asegurado.correo,
                    "celular": asegurado.celular,
                })

            # Dependientes (asegurados con id_poliza = esta póliza y tipo != titular)
            dependientes = session.exec(
                select(Asegurado).where(
                    Asegurado.id_poliza == id_poliza,
                    Asegurado.tipo_asegurado != "titular",
                    Asegurado.deleted_at == None,
                )
            ).all()

            for a in dependientes:
                nombre = f"{a.nombre} {a.apellido_paterno} {a.apellido_materno}".strip()
                participantes.append({
                    "id_asegurado": a.id_asegurado,
                    "tipo_asegurado": a.tipo_asegurado,
                    "parentesco": a.tipo_asegurado,  # conyuge, hijo, dependiente
                    "nombre_completo": nombre,
                    "rfc": a.rfc,
                    "correo": a.correo,
                    "celular": a.celular,
                })

            return participantes

    @staticmethod
    def get_participaciones_by_asegurado(id_asegurado: int) -> list[dict]:
        """Retorna todas las pólizas donde el asegurado participa (como titular o dependiente)."""
        with create_session() as session:
            participaciones = []

            # Como titular
            polizas_como_titular = session.exec(
                select(Poliza).where(
                    Poliza.id_asegurado == id_asegurado,
                    Poliza.deleted_at == None,
                )
            ).all()
            for p in polizas_como_titular:
                participaciones.append({
                    "id_poliza": p.id_poliza,
                    "numero_poliza": p.numero_poliza,
                    "estatus_poliza": p.estatus,
                    "tipo_asegurado": "titular",
                    "parentesco": "titular",
                })

            # Como dependiente (buscar en asegurado donde id_poliza != NULL)
            asegurado_dependiente = session.exec(
                select(Asegurado).where(
                    Asegurado.id_asegurado == id_asegurado,
                    Asegurado.id_poliza != None,
                    Asegurado.deleted_at == None,
                )
            ).first()
            
            if asegurado_dependiente:
                poliza = session.exec(
                    select(Poliza).where(
                        Poliza.id_poliza == asegurado_dependiente.id_poliza,
                        Poliza.deleted_at == None,
                    )
                ).first()
                if poliza:
                    participaciones.append({
                        "id_poliza": poliza.id_poliza,
                        "numero_poliza": poliza.numero_poliza,
                        "estatus_poliza": poliza.estatus,
                        "tipo_asegurado": asegurado_dependiente.tipo_asegurado,
                        "parentesco": asegurado_dependiente.tipo_asegurado,
                    })

            return participaciones

    @staticmethod
    def get_available_for_participante(id_asegurado: int) -> list[Poliza]:
        """Retorna pólizas disponibles para vincular a un asegurado como dependiente."""
        with create_session() as session:
            linked_poliza_ids = set()

            # Ya es titular de estas pólizas
            titular_ids = session.exec(
                select(Poliza.id_poliza).where(
                    Poliza.id_asegurado == id_asegurado,
                    Poliza.deleted_at == None,
                )
            ).all()
            linked_poliza_ids.update(titular_ids)

            # Ya es dependiente de alguna póliza
            asegurado = session.exec(
                select(Asegurado).where(
                    Asegurado.id_asegurado == id_asegurado,
                    Asegurado.id_poliza != None,
                    Asegurado.deleted_at == None,
                )
            ).first()
            if asegurado and asegurado.id_poliza:
                linked_poliza_ids.add(asegurado.id_poliza)

            # Productos ya cubiertos (para evitar duplicados)
            productos_activos_cubiertos = set()
            productos_titular = session.exec(
                select(Poliza.id_producto).where(
                    Poliza.id_asegurado == id_asegurado,
                    Poliza.deleted_at == None,
                    Poliza.estatus == "activa",
                )
            ).all()
            productos_activos_cubiertos.update(productos_titular)

            if asegurado and asegurado.id_poliza:
                poliza_dependiente = session.exec(
                    select(Poliza).where(
                        Poliza.id_poliza == asegurado.id_poliza,
                        Poliza.deleted_at == None,
                    )
                ).first()
                if poliza_dependiente and poliza_dependiente.estatus == "activa":
                    productos_activos_cubiertos.add(poliza_dependiente.id_producto)

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
                if p.id_poliza not in linked_poliza_ids and p.id_producto not in productos_activos_cubiertos
            ]

    @staticmethod
    def add_participante(id_poliza: int, id_asegurado: int, tipo_asegurado: str) -> Asegurado:
        """Vincula un asegurado como dependiente de una póliza."""
        with create_session() as session:
            poliza = session.exec(
                select(Poliza).where(
                    Poliza.id_poliza == id_poliza,
                    Poliza.deleted_at == None,
                )
            ).first()
            if not poliza:
                raise ValueError("La póliza seleccionada no existe o no está disponible.")

            if poliza.id_asegurado == id_asegurado:
                raise ValueError("El asegurado ya es el titular de esta póliza.")

            asegurado = session.exec(
                select(Asegurado).where(
                    Asegurado.id_asegurado == id_asegurado,
                    Asegurado.deleted_at == None,
                )
            ).first()
            if not asegurado:
                raise ValueError("El asegurado no existe o no está disponible.")

            if asegurado.id_poliza is not None and asegurado.id_poliza != id_poliza:
                raise ValueError("El asegurado ya está vinculado a otra póliza.")

            # Actualizar el asegurado como dependiente
            asegurado.tipo_asegurado = tipo_asegurado
            asegurado.id_poliza = id_poliza
            asegurado.updated_at = datetime.now()
            session.add(asegurado)
            session.commit()
            session.refresh(asegurado)
            return asegurado

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
            
            # Cascade a beneficios
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
            
            # Cascade a beneficiarios
            beneficiarios = session.exec(
                select(Beneficiario).where(
                    Beneficiario.id_poliza == id_poliza,
                    Beneficiario.deleted_at == None,
                )
            ).all()
            for b in beneficiarios:
                b.deleted_at = now
                session.add(b)
            
            # Cascade: desvincular dependientes (limpiar id_poliza)
            dependientes = session.exec(
                select(Asegurado).where(
                    Asegurado.id_poliza == id_poliza,
                    Asegurado.deleted_at == None,
                )
            ).all()
            for d in dependientes:
                d.id_poliza = None
                d.tipo_asegurado = "titular"  # Resetear a titular
                d.updated_at = now
                session.add(d)
            
            session.commit()
            return True
