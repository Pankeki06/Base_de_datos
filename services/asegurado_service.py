from models.asegurado import Asegurado
from repositories.asegurado_repository import AseguradoRepository
from services.validators import validar_correo, validar_requerido, validar_rfc


class AseguradoService:
    @staticmethod
    def create(data: dict) -> Asegurado:
        validar_requerido(data.get("nombre", ""), "nombre")
        validar_requerido(data.get("apellido_paterno", ""), "apellido_paterno")
        validar_requerido(data.get("apellido_materno", ""), "apellido_materno")
        validar_requerido(data.get("calle", ""), "calle")
        validar_requerido(data.get("numero_exterior", ""), "numero_exterior")
        validar_requerido(data.get("colonia", ""), "colonia")
        validar_requerido(data.get("municipio", ""), "municipio")
        validar_requerido(data.get("estado", ""), "estado")
        validar_requerido(data.get("codigo_postal", ""), "codigo_postal")
        validar_rfc(data.get("rfc", ""))
        validar_correo(data.get("correo"))

        if AseguradoRepository.get_by_rfc(data["rfc"]):
            raise ValueError("El RFC ya está registrado.")
        return AseguradoRepository.create(Asegurado(**data))

    @staticmethod
    def get_by_id(id_asegurado: int) -> Asegurado | None:
        return AseguradoRepository.get_by_id(id_asegurado)

    @staticmethod
    def get_all() -> list[Asegurado]:
        return AseguradoRepository.get_all()

    @staticmethod
    def search(query: str) -> list[Asegurado]:
        return AseguradoRepository.search_by_nombre_or_rfc(query)

    @staticmethod
    def get_by_agente(id_agente: int) -> list[Asegurado]:
        return AseguradoRepository.get_by_agente(id_agente)

    @staticmethod
    def update(id_asegurado: int, data: dict) -> Asegurado | None:
        if "correo" in data:
            validar_correo(data.get("correo"))
        if "rfc" in data:
            validar_rfc(data["rfc"])
        return AseguradoRepository.update(id_asegurado, data)

    @staticmethod
    def delete(id_asegurado: int) -> bool:
        return AseguradoRepository.delete(id_asegurado)
