from services.seguimiento_contacto_service import SeguimientoContactoService


class SeguimientoContactoController:
    @staticmethod
    def create_contacto(data: dict) -> dict:
        try:
            return {"ok": True, "data": SeguimientoContactoService.create(data)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_contacto_by_id(id_contacto: int) -> dict:
        try:
            entity = SeguimientoContactoService.get_by_id(id_contacto)
            if not entity:
                return {"ok": False, "error": "Contacto no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_contactos_by_seguimiento(id_seguimiento: int) -> dict:
        """Obtiene todos los contactos de un folio de seguimiento."""
        try:
            return {
                "ok": True,
                "data": SeguimientoContactoService.get_by_seguimiento(id_seguimiento),
            }
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_all_contactos() -> dict:
        try:
            return {"ok": True, "data": SeguimientoContactoService.get_all()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def update_contacto(id_contacto: int, data: dict) -> dict:
        try:
            entity = SeguimientoContactoService.update(id_contacto, data)
            if not entity:
                return {"ok": False, "error": "Contacto no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def delete_contacto(id_contacto: int) -> dict:
        try:
            deleted = SeguimientoContactoService.delete(id_contacto)
            if not deleted:
                return {"ok": False, "error": "Contacto no encontrado"}
            return {"ok": True, "mensaje": "Contacto eliminado correctamente"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
