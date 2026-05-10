from models.beneficio import Beneficio
from repositories.beneficio_repository import BeneficioRepository
from repositories.poliza_repository import PolizaRepository
from repositories.producto_beneficio_repository import ProductoBeneficioRepository
from services.validators import validar_monto_positivo, validar_requerido


class BeneficioService:
    @staticmethod
    def _normalize_optional_int(value):
        if value in (None, ""):
            return None
        return int(value)

    @staticmethod
    def _normalize_optional_float(value):
        if value in (None, ""):
            return None
        return float(value)

    @staticmethod
    def _validate_relations(
        id_poliza: int,
        id_asegurado: int | None,
        id_producto_beneficio: int | None,
    ) -> None:
        poliza = PolizaRepository.get_by_id(id_poliza)
        if not poliza:
            raise ValueError("La póliza asociada no existe o no está disponible.")

        if id_asegurado is not None:
            participantes = PolizaRepository.get_participantes_by_poliza(id_poliza)
            ids_validos = {p["id_asegurado"] for p in participantes}
            if id_asegurado not in ids_validos:
                raise ValueError(
                    "El asegurado seleccionado no pertenece a la póliza indicada."
                )

        if id_producto_beneficio is not None:
            plantilla = ProductoBeneficioRepository.get_by_id(id_producto_beneficio)
            if not plantilla:
                raise ValueError(
                    "La plantilla de beneficio seleccionada no existe o no está disponible."
                )
            if plantilla.id_producto != poliza.id_producto:
                raise ValueError(
                    "La plantilla de beneficio seleccionada no corresponde al producto de la póliza."
                )

    @staticmethod
    def create(data: dict) -> Beneficio:
        payload = data.copy()

        has_plantilla = bool(payload.get("id_producto_beneficio"))
        has_extra = bool(payload.get("nombre_beneficio_extra"))

        if has_plantilla:
            validar_requerido(payload.get("id_poliza"), "id_poliza")
            payload["id_poliza"] = int(payload["id_poliza"])
            payload["id_producto_beneficio"] = BeneficioService._normalize_optional_int(
                payload.get("id_producto_beneficio")
            )
            payload["id_asegurado"] = BeneficioService._normalize_optional_int(
                payload.get("id_asegurado")
            )

            plantilla = ProductoBeneficioRepository.get_by_id(payload["id_producto_beneficio"])
            if not plantilla:
                raise ValueError("La plantilla de beneficio seleccionada no existe o no está disponible.")

            payload["costo_aplicado"] = float(
                0.0 if plantilla.incluido_base else (plantilla.costo_extra or 0)
            )
            payload.pop("nombre_beneficio_extra", None)
            payload.pop("descripcion_extra", None)

            payload["monto_override"] = BeneficioService._normalize_optional_float(
                payload.get("monto_override")
            )
            if payload["monto_override"] is not None:
                validar_monto_positivo(payload["monto_override"], "monto_override")
            payload["vigente"] = bool(payload.get("vigente", True))

            BeneficioService._validate_relations(
                payload["id_poliza"],
                payload.get("id_asegurado"),
                payload.get("id_producto_beneficio"),
            )
            return BeneficioRepository.create(Beneficio(**payload))

        elif has_extra:
            validar_requerido(payload.get("id_poliza"), "id_poliza")
            validar_requerido(payload.get("nombre_beneficio_extra", ""), "nombre_beneficio_extra")
            validar_requerido(payload.get("descripcion_extra", ""), "descripcion_extra")
            payload["id_poliza"] = int(payload["id_poliza"])
            payload["id_asegurado"] = BeneficioService._normalize_optional_int(
                payload.get("id_asegurado")
            )
            payload["id_producto_beneficio"] = None
            payload["costo_aplicado"] = float(payload.get("costo_aplicado", 0))
            payload["monto_override"] = BeneficioService._normalize_optional_float(
                payload.get("monto_override")
            )
            payload["vigente"] = bool(payload.get("vigente", True))

            BeneficioService._validate_relations(
                payload["id_poliza"],
                payload.get("id_asegurado"),
                None,
            )
            return BeneficioRepository.create(Beneficio(**payload))
        else:
            raise ValueError("Debe especificar id_producto_beneficio o nombre_beneficio_extra.")

    @staticmethod
    def get_by_id(id_beneficio: int) -> Beneficio | None:
        return BeneficioRepository.get_by_id(id_beneficio)

    @staticmethod
    def get_all() -> list[Beneficio]:
        return BeneficioRepository.get_all()

    @staticmethod
    def get_by_poliza(id_poliza: int, *, include_inactive: bool = False) -> list[Beneficio]:
        return BeneficioRepository.get_by_poliza(id_poliza, include_inactive=include_inactive)

    @staticmethod
    def update(id_beneficio: int, data: dict) -> Beneficio | None:
        entity = BeneficioRepository.get_by_id(id_beneficio)
        if not entity:
            return None

        payload = data.copy()
        if "id_asegurado_poliza" in payload:
            payload["id_asegurado"] = payload.pop("id_asegurado_poliza")
        allowed_fields = {"id_asegurado", "monto_override", "vigente", "nombre_beneficio_extra", "descripcion_extra"}
        unknown_fields = set(payload.keys()) - allowed_fields
        if unknown_fields:
            raise ValueError(
                "Solo se permite editar: id_asegurado, monto_override, vigente, "
                "nombre_beneficio_extra y descripcion_extra."
            )

        effective_id_poliza = int(entity.id_poliza)
        effective_id_asegurado = BeneficioService._normalize_optional_int(
            payload.get("id_asegurado", entity.id_asegurado)
        )
        effective_id_producto_beneficio = BeneficioService._normalize_optional_int(
            entity.id_producto_beneficio
        )

        if "monto_override" in payload:
            payload["monto_override"] = BeneficioService._normalize_optional_float(
                payload.get("monto_override")
            )
            if payload["monto_override"] is not None:
                validar_monto_positivo(payload["monto_override"], "monto_override")

        if "vigente" in payload:
            payload["vigente"] = bool(payload["vigente"])

        BeneficioService._validate_relations(
            effective_id_poliza,
            effective_id_asegurado,
            effective_id_producto_beneficio,
        )

        if "id_asegurado" in payload:
            payload["id_asegurado"] = effective_id_asegurado

        return BeneficioRepository.update(id_beneficio, payload)

    @staticmethod
    def delete(id_beneficio: int) -> bool:
        return BeneficioRepository.delete(id_beneficio)
