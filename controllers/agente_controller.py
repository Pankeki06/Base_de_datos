from services.agente_service import AgenteService

class AgenteController:

    @staticmethod
    def create_agente(agente_data: dict) -> dict:
        try:
            resultado = AgenteService.create(agente_data)
            return {"ok": True, "data": resultado}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_agente_by_id(id_agente: int) -> dict:
        try:
            agente = AgenteService.get_by_id(id_agente)
            if not agente:
                return {"ok": False, "error": "Agente no encontrado"}
            return {"ok": True, "data": agente}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_all_agentes() -> dict:
        try:
            agentes = AgenteService.get_all()
            return {"ok": True, "data": agentes}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def update_agente(id_agente: int, updated_data: dict) -> dict:
        try:
            agente = AgenteService.update(id_agente, updated_data)
            if not agente:
                return {"ok": False, "error": "Agente no encontrado"}
            return {"ok": True, "data": agente}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def delete_agente(id_agente: int) -> dict:
        try:
            eliminado = AgenteService.delete(id_agente)

            if not eliminado:
                return {"ok": False, "error": "Agente no encontrado"}

            return {"ok": True, "mensaje": "Agente eliminado correctamente"}

        except Exception as e:
            return {"ok": False, "error": str(e)}