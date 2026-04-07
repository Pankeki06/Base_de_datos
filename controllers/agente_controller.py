from repositories.agente_repository import AgenteRepository
from models.agente import Agente
from datetime import datetime

class AgenteController:

    @staticmethod
    def create_agente(agente_data: dict) -> dict:
        try:
            agente = Agente(**agente_data)
            resultado = AgenteRepository.create_agente(agente)
            return {"ok": True, "data": resultado}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_agente_by_id(id_agente: int) -> dict:
        try:
            agente = AgenteRepository.get_agente_by_id(id_agente)
            if not agente:
                return {"ok": False, "error": "Agente no encontrado"}
            return {"ok": True, "data": agente}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_all_agentes() -> dict:
        try:
            agentes = AgenteRepository.get_all_agentes()
            if not agentes:
                return {"ok": False, "error": "No hay agentes registrados"}
            return {"ok": True, "data": agentes}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def update_agente(id_agente: int, updated_data: dict) -> dict:
        try:
            agente = AgenteRepository.update_agente(id_agente, updated_data)
            if not agente:
                return {"ok": False, "error": "Agente no encontrado"}
            return {"ok": True, "data": agente}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def delete_agente(id_agente: int) -> dict:
        try:
            eliminado = AgenteRepository.delete_agente(id_agente)

            if not eliminado:
                return {"ok": False, "error": "Agente no encontrado"}

            return {"ok": True, "mensaje": "Agente eliminado correctamente"}

        except Exception as e:
            return {"ok": False, "error": str(e)}