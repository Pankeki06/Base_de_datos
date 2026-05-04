from models.poliza import Poliza
from repositories.poliza_repository import PolizaRepository
from repositories.producto_beneficio_repository import ProductoBeneficioRepository
from services.validators import validar_enum, validar_monto_positivo, validar_rango_fechas, validar_requerido


class PolizaService:
    _TIPOS_PARTICIPANTE_VALIDOS = {"titular", "conyuge", "hijo", "dependiente"}

    @staticmethod
    def _normalize_selected_beneficios(
        id_producto: int,
        beneficios_seleccionados,
    ) -> list[int] | None:
        if beneficios_seleccionados is None:
            return None
        if not isinstance(beneficios_seleccionados, (list, tuple, set)):
            raise ValueError("Los beneficios seleccionados deben enviarse como lista.")

        selected_ids: list[int] = []
        for beneficio_id in beneficios_seleccionados:
            if beneficio_id in (None, ""):
                continue
            selected_ids.append(int(beneficio_id))

        selected_ids = list(dict.fromkeys(selected_ids))
        if not selected_ids:
            return []

        beneficios_producto = ProductoBeneficioRepository.get_by_producto(id_producto)
        ids_validos = {
            beneficio.id_producto_beneficio
            for beneficio in beneficios_producto
        }
        ids_invalidos = set(selected_ids) - ids_validos
        if ids_invalidos:
            raise ValueError(
                "Los beneficios seleccionados no pertenecen al producto o no están activos."
            )
        return selected_ids

    @staticmethod
    def create(data: dict) -> Poliza:
        if not data.get("id_asegurado"):
            raise ValueError("El campo id_asegurado es requerido.")
        validar_requerido(data.get("numero_poliza", ""), "numero_poliza")
        estatus = str(data.get("estatus", "")).strip().lower()
        validar_enum(estatus, "estatus", {"activa", "cancelada", "vencida"})
        validar_monto_positivo(float(data.get("prima_mensual", 0)), "prima_mensual")
        validar_rango_fechas(data["fecha_inicio"], data["fecha_vencimiento"])
        if not data.get("id_producto"):
            raise ValueError("El campo id_producto es requerido.")

        poliza_existente = PolizaRepository.get_active_for_asegurado_producto(
            int(data["id_asegurado"]),
            int(data["id_producto"]),
        )
        if poliza_existente:
            raise ValueError("El asegurado ya cuenta con una póliza activa de este producto.")

        if PolizaRepository.get_by_numero(data["numero_poliza"]):
            raise ValueError("El número de póliza ya está registrado.")
        payload = data.copy()
        payload["estatus"] = estatus
        selected_beneficios = PolizaService._normalize_selected_beneficios(
            int(payload["id_producto"]),
            payload.pop("beneficios_seleccionados", None),
        )
        return PolizaRepository.create(
            Poliza(**payload),
            selected_producto_beneficio_ids=selected_beneficios,
        )

    @staticmethod
    def get_by_id(id_poliza: int) -> Poliza | None:
        return PolizaRepository.get_by_id(id_poliza)

    @staticmethod
    def get_all() -> list[Poliza]:
        return PolizaRepository.get_all()

    @staticmethod
    def get_by_asegurado(id_asegurado: int) -> list[Poliza]:
        return PolizaRepository.get_by_asegurado(id_asegurado)

    @staticmethod
    def get_participantes_by_poliza(id_poliza: int) -> list[dict]:
        return PolizaRepository.get_participantes_by_poliza(id_poliza)

    @staticmethod
    def get_participaciones_by_asegurado(id_asegurado: int) -> list[dict]:
        return PolizaRepository.get_participaciones_by_asegurado(id_asegurado)

    @staticmethod
    def get_available_for_participante(id_asegurado: int) -> list[Poliza]:
        return PolizaRepository.get_available_for_participante(id_asegurado)

    @staticmethod
    def add_participante(data: dict):
        if not data.get("id_poliza"):
            raise ValueError("El campo id_poliza es requerido.")
        if not data.get("id_asegurado"):
            raise ValueError("El campo id_asegurado es requerido.")

        tipo = str(data.get("tipo_participante", "dependiente")).strip().lower()
        if tipo not in PolizaService._TIPOS_PARTICIPANTE_VALIDOS:
            raise ValueError("Tipo de participante inválido.")

        return PolizaRepository.add_participante(
            id_poliza=int(data["id_poliza"]),
            id_asegurado=int(data["id_asegurado"]),
            tipo_participante=tipo,
        )

    @staticmethod
    def update(id_poliza: int, data: dict) -> Poliza | None:
        payload = data.copy()
        fecha_inicio = data.get("fecha_inicio")
        fecha_vencimiento = data.get("fecha_vencimiento")
        if fecha_inicio and fecha_vencimiento:
            validar_rango_fechas(fecha_inicio, fecha_vencimiento)
        if "prima_mensual" in payload:
            validar_monto_positivo(float(payload["prima_mensual"]), "prima_mensual")
        if "estatus" in payload:
            payload["estatus"] = str(payload["estatus"]).strip().lower()
            validar_enum(payload["estatus"], "estatus", {"activa", "cancelada", "vencida"})
        return PolizaRepository.update(id_poliza, payload)

    @staticmethod
    def delete(id_poliza: int) -> bool:
        return PolizaRepository.delete(id_poliza)
