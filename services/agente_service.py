from models.agente import Agente
from repositories.agente_repository import AgenteRepository
from services.security import hash_password
from services.validators import validar_correo, validar_requerido


class AgenteService:
    @staticmethod
    def create(data: dict) -> Agente:
        validar_requerido(data.get("clave_agente", ""), "clave_agente")
        validar_requerido(data.get("nombre", ""), "nombre")
        validar_requerido(data.get("apellido_paterno", ""), "apellido_paterno")
        validar_requerido(data.get("apellido_materno", ""), "apellido_materno")
        validar_requerido(data.get("password", ""), "password")
        validar_correo(data.get("correo"))

        if AgenteRepository.get_agente_by_clave(data["clave_agente"]):
            raise ValueError("La clave de agente ya está registrada.")
        if AgenteRepository.get_agente_by_correo(data["correo"]):
            raise ValueError("El correo ya está registrado.")

        data = data.copy()
        data["password"] = hash_password(data["password"])
        agente = Agente(**data)
        return AgenteRepository.create_agente(agente)

    @staticmethod
    def get_by_id(id_agente: int) -> Agente | None:
        return AgenteRepository.get_agente_by_id(id_agente)

    @staticmethod
    def get_all() -> list[Agente]:
        return AgenteRepository.get_all_agentes()

    @staticmethod
    def update(id_agente: int, data: dict) -> Agente | None:
        payload = data.copy()
        if "correo" in payload:
            validar_correo(payload["correo"])
        if "password" in payload and payload["password"]:
            payload["password"] = hash_password(payload["password"])
        return AgenteRepository.update_agente(id_agente, payload)

    @staticmethod
    def delete(id_agente: int) -> bool:
        return AgenteRepository.delete_agente(id_agente)
