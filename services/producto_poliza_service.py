from models.producto_poliza import ProductoPoliza
from repositories.producto_poliza_repository import ProductoPolizaRepository
from services.validators import validar_monto_positivo, validar_requerido


class ProductoPolizaService:
    @staticmethod
    def create(data: dict) -> ProductoPoliza:
        validar_requerido(data.get("nombre", ""), "nombre")
        validar_requerido(data.get("tipo_seguro", ""), "tipo_seguro")
        validar_monto_positivo(float(data.get("prima_base", 0)), "prima_base")
        return ProductoPolizaRepository.create(ProductoPoliza(**data))

    @staticmethod
    def get_by_id(id_producto: int) -> ProductoPoliza | None:
        return ProductoPolizaRepository.get_by_id(id_producto)

    @staticmethod
    def get_all() -> list[ProductoPoliza]:
        return ProductoPolizaRepository.get_all()

    @staticmethod
    def get_activos() -> list[ProductoPoliza]:
        return ProductoPolizaRepository.get_activos()

    @staticmethod
    def update(id_producto: int, data: dict) -> ProductoPoliza | None:
        if "prima_base" in data:
            validar_monto_positivo(float(data["prima_base"]), "prima_base")
        return ProductoPolizaRepository.update(id_producto, data)

    @staticmethod
    def delete(id_producto: int) -> bool:
        return ProductoPolizaRepository.delete(id_producto)
