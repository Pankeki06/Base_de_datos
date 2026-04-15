from models.beneficio import Beneficio
from repositories.beneficio_repository import BeneficioRepository
from services.validators import validar_monto_positivo, validar_requerido


class BeneficioService:
    @staticmethod
    def create(data: dict) -> Beneficio:
        validar_requerido(data.get("nombre_beneficio", ""), "nombre_beneficio")
        validar_requerido(data.get("descripcion", ""), "descripcion")
        validar_monto_positivo(float(data.get("monto_cobertura", 0)), "monto_cobertura")
        return BeneficioRepository.create(Beneficio(**data))

    @staticmethod
    def get_by_id(id_beneficio: int) -> Beneficio | None:
        return BeneficioRepository.get_by_id(id_beneficio)

    @staticmethod
    def get_all() -> list[Beneficio]:
        return BeneficioRepository.get_all()

    @staticmethod
    def get_by_poliza(id_poliza: int) -> list[Beneficio]:
        return BeneficioRepository.get_by_poliza(id_poliza)

    @staticmethod
    def update(id_beneficio: int, data: dict) -> Beneficio | None:
        if "monto_cobertura" in data:
            validar_monto_positivo(float(data["monto_cobertura"]), "monto_cobertura")
        return BeneficioRepository.update(id_beneficio, data)

    @staticmethod
    def delete(id_beneficio: int) -> bool:
        return BeneficioRepository.delete(id_beneficio)
