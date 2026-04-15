from models.poliza import Poliza
from repositories.poliza_repository import PolizaRepository
from services.validators import validar_monto_positivo, validar_rango_fechas, validar_requerido


class PolizaService:
    @staticmethod
    def create(data: dict) -> Poliza:
        validar_requerido(data.get("numero_poliza", ""), "numero_poliza")
        validar_requerido(data.get("tipo_seguro", ""), "tipo_seguro")
        validar_requerido(data.get("estatus", ""), "estatus")
        validar_monto_positivo(float(data.get("prima_mensual", 0)), "prima_mensual")
        validar_rango_fechas(data["fecha_inicio"], data["fecha_vencimiento"])

        if PolizaRepository.get_by_numero(data["numero_poliza"]):
            raise ValueError("El número de póliza ya está registrado.")
        return PolizaRepository.create(Poliza(**data))

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
    def update(id_poliza: int, data: dict) -> Poliza | None:
        fecha_inicio = data.get("fecha_inicio")
        fecha_vencimiento = data.get("fecha_vencimiento")
        if fecha_inicio and fecha_vencimiento:
            validar_rango_fechas(fecha_inicio, fecha_vencimiento)
        if "prima_mensual" in data:
            validar_monto_positivo(float(data["prima_mensual"]), "prima_mensual")
        return PolizaRepository.update(id_poliza, data)

    @staticmethod
    def delete(id_poliza: int) -> bool:
        return PolizaRepository.delete(id_poliza)
