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
    def _validate_relations(
        id_poliza: int,
        id_asegurado_poliza: int | None,
        id_producto_beneficio: int | None,
    ) -> None:
        poliza = PolizaRepository.get_by_id(id_poliza)
        if not poliza:
            raise ValueError("La póliza asociada no existe o no está disponible.")

        if id_asegurado_poliza is not None:
            participante = PolizaRepository.get_participante_by_id(id_asegurado_poliza)
            if not participante or participante.id_poliza != poliza.id_poliza:
                raise ValueError(
                    "El participante seleccionado no pertenece a la póliza indicada."
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
    def _normalize_optional_float(value):
        if value in (None, ""):
            return None
        return float(value)

    @staticmethod
    def create(data: dict) -> Beneficio:
        validar_requerido(data.get("id_poliza"), "id_poliza")
        validar_requerido(data.get("id_producto_beneficio"), "id_producto_beneficio")

        payload = data.copy()
        payload["id_poliza"] = int(payload["id_poliza"])
        payload["id_asegurado_poliza"] = BeneficioService._normalize_optional_int(
            payload.get("id_asegurado_poliza")
        )
        payload["id_producto_beneficio"] = BeneficioService._normalize_optional_int(
            payload.get("id_producto_beneficio")
        )

        plantilla = ProductoBeneficioRepository.get_by_id(payload["id_producto_beneficio"])
        if not plantilla:
            raise ValueError("La plantilla de beneficio seleccionada no existe o no está disponible.")

        payload["nombre_beneficio"] = plantilla.nombre_beneficio
        payload["descripcion"] = plantilla.descripcion
        payload["monto_cobertura"] = float(plantilla.monto_cobertura or 0)
        payload["monto_override"] = BeneficioService._normalize_optional_float(
            payload.get("monto_override")
        )
        if payload["monto_override"] is not None:
            validar_monto_positivo(payload["monto_override"], "monto_override")
        payload["vigente"] = bool(payload.get("vigente", True))

        BeneficioService._validate_relations(
            payload["id_poliza"],
            payload.get("id_asegurado_poliza"),
            payload.get("id_producto_beneficio"),
        )
        return BeneficioRepository.create(Beneficio(**payload))

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
        allowed_fields = {"id_asegurado_poliza", "monto_override", "vigente"}
        unknown_fields = set(payload.keys()) - allowed_fields
        if unknown_fields:
            raise ValueError(
                "Solo se permite editar: id_asegurado_poliza, monto_override y vigente."
            )

        effective_id_poliza = int(entity.id_poliza)
        effective_id_asegurado_poliza = BeneficioService._normalize_optional_int(
            payload.get("id_asegurado_poliza", entity.id_asegurado_poliza)
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
            effective_id_asegurado_poliza,
            effective_id_producto_beneficio,
        )

        if "id_asegurado_poliza" in payload:
            payload["id_asegurado_poliza"] = effective_id_asegurado_poliza

        return BeneficioRepository.update(id_beneficio, payload)

    @staticmethod
    def delete(id_beneficio: int) -> bool:
        return BeneficioRepository.delete(id_beneficio)
