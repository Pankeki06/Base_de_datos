from services.beneficio_service import BeneficioService


class BeneficioController:
    @staticmethod
    def create_beneficio(data: dict) -> dict:
        try:
            return {"ok": True, "data": BeneficioService.create(data)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_beneficio_by_id(id_beneficio: int) -> dict:
        try:
            entity = BeneficioService.get_by_id(id_beneficio)
            if not entity:
                return {"ok": False, "error": "Beneficio no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_all_beneficios() -> dict:
        try:
            return {"ok": True, "data": BeneficioService.get_all()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def update_beneficio(id_beneficio: int, data: dict) -> dict:
        try:
            entity = BeneficioService.update(id_beneficio, data)
            if not entity:
                return {"ok": False, "error": "Beneficio no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def delete_beneficio(id_beneficio: int) -> dict:
        try:
            deleted = BeneficioService.delete(id_beneficio)
            if not deleted:
                return {"ok": False, "error": "Beneficio no encontrado"}
            return {"ok": True, "mensaje": "Beneficio eliminado correctamente"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
