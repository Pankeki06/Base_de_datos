from models.producto_beneficio import ProductoBeneficio
from repositories.producto_beneficio_repository import ProductoBeneficioRepository
from services.validators import validar_monto_positivo, validar_requerido


class ProductoBeneficioService:
    @staticmethod
    def _normalize_optional_float(value):
        if value in (None, ""):
            return None
        return float(value)

    @staticmethod
    def create(data: dict) -> ProductoBeneficio:
        validar_requerido(data.get("nombre_beneficio", ""), "nombre_beneficio")
        validar_requerido(data.get("descripcion", ""), "descripcion")
        validar_monto_positivo(float(data.get("monto_cobertura", 0)), "monto_cobertura")
        payload = data.copy()
        payload["costo_extra"] = ProductoBeneficioService._normalize_optional_float(
            payload.get("costo_extra")
        )
        payload["incluido_base"] = bool(payload.get("incluido_base", True))
        if payload["incluido_base"]:
            payload["costo_extra"] = None
        elif payload["costo_extra"] is not None:
            validar_monto_positivo(payload["costo_extra"], "costo_extra")
        return ProductoBeneficioRepository.create(ProductoBeneficio(**payload))

    @staticmethod
    def get_by_id(id_producto_beneficio: int) -> ProductoBeneficio | None:
        return ProductoBeneficioRepository.get_by_id(id_producto_beneficio)

    @staticmethod
    def get_all() -> list[ProductoBeneficio]:
        return ProductoBeneficioRepository.get_all()

    @staticmethod
    def get_by_producto(id_producto: int) -> list[ProductoBeneficio]:
        return ProductoBeneficioRepository.get_by_producto(id_producto)

    @staticmethod
    def update(id_producto_beneficio: int, data: dict) -> ProductoBeneficio | None:
        payload = data.copy()
        if "monto_cobertura" in payload:
            validar_monto_positivo(float(payload["monto_cobertura"]), "monto_cobertura")
        if "costo_extra" in payload:
            payload["costo_extra"] = ProductoBeneficioService._normalize_optional_float(
                payload.get("costo_extra")
            )
            if payload["costo_extra"] is not None:
                validar_monto_positivo(payload["costo_extra"], "costo_extra")
        if payload.get("incluido_base") is True:
            payload["costo_extra"] = None
        return ProductoBeneficioRepository.update(id_producto_beneficio, payload)

    @staticmethod
    def delete(id_producto_beneficio: int) -> bool:
        return ProductoBeneficioRepository.delete(id_producto_beneficio)
