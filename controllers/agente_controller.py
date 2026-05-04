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
    def get_agentes_page(page: int = 1, page_size: int = 20, nombre_query: str = "") -> dict:
        try:
            items, total = AgenteService.get_page(
                page=page,
                page_size=page_size,
                nombre_query=nombre_query,
            )
            total_pages = (total + page_size - 1) // page_size if page_size else 1
            return {
                "ok": True,
                "data": items,
                "meta": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "total_pages": max(1, total_pages),
                },
            }
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

            return {"ok": True, "mensaje": "Agente desactivado correctamente"}

        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_agentes_desactivados_page(page: int = 1, page_size: int = 20, nombre_query: str = "") -> dict:
        try:
            items, total = AgenteService.get_page_desactivados(
                page=page,
                page_size=page_size,
                nombre_query=nombre_query,
            )
            total_pages = (total + page_size - 1) // page_size if page_size else 1
            return {
                "ok": True,
                "data": items,
                "meta": {
                    "page": page,
                    "page_size": page_size,
                    "total": total,
                    "total_pages": max(1, total_pages),
                },
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def reactivate_agente(id_agente: int) -> dict:
        try:
            ok = AgenteService.reactivate(id_agente)
            if not ok:
                return {"ok": False, "error": "Agente no encontrado"}
            return {"ok": True, "mensaje": "Agente reactivado correctamente"}
        except Exception as e:
            return {"ok": False, "error": str(e)}