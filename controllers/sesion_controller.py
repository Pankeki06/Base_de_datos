from services.sesion_service import SesionService


class SesionController:
    @staticmethod
    def create_sesion(data: dict) -> dict:
        try:
            return {"ok": True, "data": SesionService.create(data)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_sesion_by_id(id_sesion: int) -> dict:
        try:
            entity = SesionService.get_by_id(id_sesion)
            if not entity:
                return {"ok": False, "error": "Sesión no encontrada"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_all_sesiones() -> dict:
        try:
            return {"ok": True, "data": SesionService.get_all()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def update_sesion(id_sesion: int, data: dict) -> dict:
        try:
            entity = SesionService.update(id_sesion, data)
            if not entity:
                return {"ok": False, "error": "Sesión no encontrada"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def delete_sesion(id_sesion: int) -> dict:
        try:
            deleted = SesionService.delete(id_sesion)
            if not deleted:
                return {"ok": False, "error": "Sesión no encontrada"}
            return {"ok": True, "mensaje": "Sesión eliminada correctamente"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
