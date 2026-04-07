"""Controlador para operaciones sobre pólizas."""

from services.poliza_service import PolizaService


class PolizaController:
    @staticmethod
    def create_poliza(data: dict) -> dict:
        try:
            return {"ok": True, "data": PolizaService.create(data)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_poliza_by_id(id_poliza: int) -> dict:
        try:
            entity = PolizaService.get_by_id(id_poliza)
            if not entity:
                return {"ok": False, "error": "Póliza no encontrada"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_all_polizas() -> dict:
        try:
            return {"ok": True, "data": PolizaService.get_all()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def update_poliza(id_poliza: int, data: dict) -> dict:
        try:
            entity = PolizaService.update(id_poliza, data)
            if not entity:
                return {"ok": False, "error": "Póliza no encontrada"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def delete_poliza(id_poliza: int) -> dict:
        try:
            deleted = PolizaService.delete(id_poliza)
            if not deleted:
                return {"ok": False, "error": "Póliza no encontrada"}
            return {"ok": True, "mensaje": "Póliza eliminada correctamente"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
