"""Controlador para operaciones sobre asegurados."""

from services.asegurado_service import AseguradoService


class AseguradoController:
    @staticmethod
    def create_asegurado(data: dict) -> dict:
        try:
            return {"ok": True, "data": AseguradoService.create(data)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_asegurado_by_id(id_asegurado: int) -> dict:
        try:
            entity = AseguradoService.get_by_id(id_asegurado)
            if not entity:
                return {"ok": False, "error": "Asegurado no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_all_asegurados() -> dict:
        try:
            return {"ok": True, "data": AseguradoService.get_all()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def search_asegurados(query: str) -> dict:
        try:
            return {"ok": True, "data": AseguradoService.search(query)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_asegurados_by_agente(id_agente: int) -> dict:
        try:
            return {"ok": True, "data": AseguradoService.get_by_agente(id_agente)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_asegurados_by_agente_page(id_agente: int, page: int = 1, page_size: int = 20) -> dict:
        try:
            asegurados = AseguradoService.get_by_agente_page(id_agente, page, page_size)
            total = AseguradoService.count_by_agente(id_agente)
            return {"ok": True, "data": asegurados, "total": total}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_titulares_by_agente_page(id_agente: int, page: int = 1, page_size: int = 20) -> dict:
        try:
            asegurados = AseguradoService.get_titulares_by_agente_page(id_agente, page, page_size)
            total = AseguradoService.count_titulares_by_agente(id_agente)
            return {"ok": True, "data": asegurados, "total": total}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def update_asegurado(id_asegurado: int, data: dict) -> dict:
        try:
            entity = AseguradoService.update(id_asegurado, data)
            if not entity:
                return {"ok": False, "error": "Asegurado no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def delete_asegurado(id_asegurado: int) -> dict:
        try:
            deleted = AseguradoService.delete(id_asegurado)
            if not deleted:
                return {"ok": False, "error": "Asegurado no encontrado"}
            return {"ok": True, "mensaje": "Asegurado eliminado correctamente"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
