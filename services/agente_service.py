from models.agente import Agente
from repositories.agente_repository import AgenteRepository
from repositories.poliza_repository import PolizaRepository
from services.security import hash_password
from services.validators import validar_correo, validar_password, validar_requerido, validar_telefono


class AgenteService:
    @staticmethod
    def create(data: dict) -> Agente:
        validar_requerido(data.get("clave_agente", ""), "clave_agente")
        validar_requerido(data.get("cedula", ""), "cedula")
        validar_requerido(data.get("nombre", ""), "nombre")
        validar_requerido(data.get("apellido_paterno", ""), "apellido_paterno")
        validar_requerido(data.get("apellido_materno", ""), "apellido_materno")
        validar_requerido(data.get("rol", ""), "rol")
        validar_requerido(data.get("password", ""), "password")
        validar_password(data.get("password", ""))
        validar_correo(data.get("correo"))
        validar_telefono(data.get("telefono"), "telefono")
        if data.get("rol") not in {"admin", "agente"}:
            raise ValueError("El rol debe ser 'admin' o 'agente'.")

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
    def get_page(page: int = 1, page_size: int = 20, nombre_query: str = "") -> tuple[list[Agente], int]:
        page = max(1, int(page))
        page_size = max(1, int(page_size))
        query = (nombre_query or "").strip()
        items = AgenteRepository.get_agentes_page(page=page, page_size=page_size, nombre_query=query)
        total = AgenteRepository.count_agentes(nombre_query=query)
        return items, total

    @staticmethod
    def update(id_agente: int, data: dict) -> Agente | None:
        payload = data.copy()
        if "correo" in payload:
            validar_correo(payload["correo"])
            existing = AgenteRepository.get_agente_by_correo(payload["correo"])
            if existing and existing.id_agente != id_agente:
                raise ValueError("El correo ya está registrado por otro agente.")
        if "telefono" in payload:
            validar_telefono(payload.get("telefono"), "telefono")
        if "password" in payload and payload["password"]:
            validar_password(payload["password"])
            payload["password"] = hash_password(payload["password"])
        return AgenteRepository.update_agente(id_agente, payload)

    @staticmethod
    def delete(id_agente: int) -> bool:
        polizas_asignadas = PolizaRepository.count_by_agente_responsable(id_agente)
        if polizas_asignadas > 0:
            raise ValueError(
                "No se puede desactivar el agente porque tiene polizas asignadas. Reasigna esas polizas antes de continuar."
            )
        return AgenteRepository.delete_agente(id_agente)

    @staticmethod
    def get_page_desactivados(page: int = 1, page_size: int = 20, nombre_query: str = "") -> tuple[list, int]:
        page = max(1, int(page))
        page_size = max(1, int(page_size))
        query = (nombre_query or "").strip()
        items = AgenteRepository.get_agentes_desactivados_page(page=page, page_size=page_size, nombre_query=query)
        total = AgenteRepository.count_agentes_desactivados(nombre_query=query)
        return items, total

    @staticmethod
    def reactivate(id_agente: int) -> bool:
        return AgenteRepository.reactivate_agente(id_agente)
