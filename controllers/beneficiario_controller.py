from services.beneficiario_service import BeneficiarioService


class BeneficiarioController:
    @staticmethod
    def create_beneficiario(data: dict) -> dict:
        try:
            return {"ok": True, "data": BeneficiarioService.create(data)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_beneficiario_by_id(id_beneficiario: int) -> dict:
        try:
            entity = BeneficiarioService.get_by_id(id_beneficiario)
            if not entity:
                return {"ok": False, "error": "Beneficiario no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_all_beneficiarios() -> dict:
        try:
            return {"ok": True, "data": BeneficiarioService.get_all()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def update_beneficiario(id_beneficiario: int, data: dict) -> dict:
        try:
            entity = BeneficiarioService.update(id_beneficiario, data)
            if not entity:
                return {"ok": False, "error": "Beneficiario no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def delete_beneficiario(id_beneficiario: int) -> dict:
        try:
            deleted = BeneficiarioService.delete(id_beneficiario)
            if not deleted:
                return {"ok": False, "error": "Beneficiario no encontrado"}
            return {"ok": True, "mensaje": "Beneficiario eliminado correctamente"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
