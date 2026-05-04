from services.producto_beneficio_service import ProductoBeneficioService


class ProductoBeneficioController:
    @staticmethod
    def create_producto_beneficio(data: dict) -> dict:
        try:
            return {"ok": True, "data": ProductoBeneficioService.create(data)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_producto_beneficio_by_id(id_producto_beneficio: int) -> dict:
        try:
            entity = ProductoBeneficioService.get_by_id(id_producto_beneficio)
            if not entity:
                return {"ok": False, "error": "Beneficio de producto no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_all_producto_beneficios() -> dict:
        try:
            return {"ok": True, "data": ProductoBeneficioService.get_all()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_beneficios_by_producto(id_producto: int) -> dict:
        try:
            return {"ok": True, "data": ProductoBeneficioService.get_by_producto(id_producto)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def update_producto_beneficio(id_producto_beneficio: int, data: dict) -> dict:
        try:
            entity = ProductoBeneficioService.update(id_producto_beneficio, data)
            if not entity:
                return {"ok": False, "error": "Beneficio de producto no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def delete_producto_beneficio(id_producto_beneficio: int) -> dict:
        try:
            deleted = ProductoBeneficioService.delete(id_producto_beneficio)
            if not deleted:
                return {"ok": False, "error": "Beneficio de producto no encontrado"}
            return {"ok": True, "mensaje": "Beneficio de producto desactivado correctamente"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
