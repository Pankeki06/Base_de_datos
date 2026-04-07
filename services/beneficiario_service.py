from models.beneficiario import Beneficiario
from repositories.beneficiario_repository import BeneficiarioRepository
from services.validators import validar_porcentaje, validar_requerido


class BeneficiarioService:
    @staticmethod
    def create(data: dict) -> Beneficiario:
        validar_requerido(data.get("nombre_completo", ""), "nombre_completo")
        validar_requerido(data.get("parentesco", ""), "parentesco")
        validar_porcentaje(float(data.get("porcentaje_participacion", 0)))
        return BeneficiarioRepository.create(Beneficiario(**data))

    @staticmethod
    def get_by_id(id_beneficiario: int) -> Beneficiario | None:
        return BeneficiarioRepository.get_by_id(id_beneficiario)

    @staticmethod
    def get_all() -> list[Beneficiario]:
        return BeneficiarioRepository.get_all()

    @staticmethod
    def update(id_beneficiario: int, data: dict) -> Beneficiario | None:
        if "porcentaje_participacion" in data:
            validar_porcentaje(float(data["porcentaje_participacion"]))
        return BeneficiarioRepository.update(id_beneficiario, data)

    @staticmethod
    def delete(id_beneficiario: int) -> bool:
        return BeneficiarioRepository.delete(id_beneficiario)
