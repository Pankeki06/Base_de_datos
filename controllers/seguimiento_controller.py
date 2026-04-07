"""Controlador para el seguimiento de asegurados."""

from services.seguimiento_service import SeguimientoService


class SeguimientoController:
    @staticmethod
    def create_seguimiento(data: dict) -> dict:
        try:
            return {"ok": True, "data": SeguimientoService.create(data)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_seguimiento_by_id(id_seguimiento: int) -> dict:
        try:
            entity = SeguimientoService.get_by_id(id_seguimiento)
            if not entity:
                return {"ok": False, "error": "Seguimiento no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_all_seguimientos() -> dict:
        try:
            return {"ok": True, "data": SeguimientoService.get_all()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def update_seguimiento(id_seguimiento: int, data: dict) -> dict:
        try:
            entity = SeguimientoService.update(id_seguimiento, data)
            if not entity:
                return {"ok": False, "error": "Seguimiento no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def delete_seguimiento(id_seguimiento: int) -> dict:
        try:
            deleted = SeguimientoService.delete(id_seguimiento)
            if not deleted:
                return {"ok": False, "error": "Seguimiento no encontrado"}
            return {"ok": True, "mensaje": "Seguimiento eliminado correctamente"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
