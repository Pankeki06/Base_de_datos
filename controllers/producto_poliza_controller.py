from services.producto_poliza_service import ProductoPolizaService


class ProductoPolizaController:
    @staticmethod
    def create_producto(data: dict) -> dict:
        try:
            return {"ok": True, "data": ProductoPolizaService.create(data)}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_producto_by_id(id_producto: int) -> dict:
        try:
            entity = ProductoPolizaService.get_by_id(id_producto)
            if not entity:
                return {"ok": False, "error": "Producto no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_all_productos() -> dict:
        try:
            return {"ok": True, "data": ProductoPolizaService.get_all()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def get_productos_activos() -> dict:
        try:
            return {"ok": True, "data": ProductoPolizaService.get_activos()}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def update_producto(id_producto: int, data: dict) -> dict:
        try:
            entity = ProductoPolizaService.update(id_producto, data)
            if not entity:
                return {"ok": False, "error": "Producto no encontrado"}
            return {"ok": True, "data": entity}
        except Exception as e:
            return {"ok": False, "error": str(e)}

    @staticmethod
    def delete_producto(id_producto: int) -> dict:
        try:
            deleted = ProductoPolizaService.delete(id_producto)
            if not deleted:
                return {"ok": False, "error": "Producto no encontrado"}
            return {"ok": True, "mensaje": "Producto desactivado correctamente"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
