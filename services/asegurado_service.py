from models.asegurado import Asegurado
from repositories.agente_repository import AgenteRepository
from repositories.asegurado_repository import AseguradoRepository
from services.validators import validar_correo, validar_requerido, validar_rfc, validar_telefono


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
        validar_telefono(data.get("celular"), "celular", 10, 10)

        if AseguradoRepository.get_by_rfc(data["rfc"]):
            raise ValueError("El RFC ya está registrado.")

        if data.get("id_agente_responsable") is not None:
            if not AgenteRepository.get_agente_by_id(data["id_agente_responsable"]):
                raise ValueError("El agente responsable no existe.")

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
    def get_by_agente_page(id_agente: int, page: int = 1, page_size: int = 20) -> list[Asegurado]:
        return AseguradoRepository.get_by_agente_page(id_agente, page, page_size)

    @staticmethod
    def count_by_agente(id_agente: int) -> int:
        return AseguradoRepository.count_by_agente(id_agente)

    @staticmethod
    def get_titulares_by_agente_page(id_agente: int, page: int = 1, page_size: int = 20) -> list[Asegurado]:
        return AseguradoRepository.get_titulares_by_agente_page(id_agente, page, page_size)

    @staticmethod
    def count_titulares_by_agente(id_agente: int) -> int:
        return AseguradoRepository.count_titulares_by_agente(id_agente)

    @staticmethod
    def update(id_asegurado: int, data: dict) -> Asegurado | None:
        if "correo" in data:
            validar_correo(data.get("correo"))
        if "rfc" in data:
            validar_rfc(data["rfc"])
            existing = AseguradoRepository.get_by_rfc(data["rfc"])
            if existing and existing.id_asegurado != id_asegurado:
                raise ValueError("El RFC ya está registrado por otro asegurado.")
        if "celular" in data:
            validar_telefono(data.get("celular"), "celular", 10, 10)
        if "id_agente_responsable" in data and data["id_agente_responsable"] is not None:
            if not AgenteRepository.get_agente_by_id(data["id_agente_responsable"]):
                raise ValueError("El agente responsable no existe.")
        return AseguradoRepository.update(id_asegurado, data)

    @staticmethod
    def delete(id_asegurado: int) -> bool:
        return AseguradoRepository.delete(id_asegurado)
