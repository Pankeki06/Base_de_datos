from models.beneficiario import Beneficiario
from repositories.beneficiario_repository import BeneficiarioRepository
from repositories.poliza_repository import PolizaRepository
from services.validators import validar_porcentaje, validar_requerido, validar_telefono


class BeneficiarioService:
    @staticmethod
    def _normalize_id_poliza(value) -> int | None:
        if value in (None, ""):
            return None
        return int(value)

    @staticmethod
    def _validar_poliza_de_asegurado(id_asegurado: int, id_poliza: int | None) -> None:
        if id_poliza is None:
            return

        poliza = PolizaRepository.get_by_id(id_poliza)
        if not poliza:
            raise ValueError("La póliza seleccionada no existe o ya no está disponible.")

        participaciones = PolizaRepository.get_participaciones_by_asegurado(id_asegurado)
        if not any(int(item.get("id_poliza", 0)) == int(id_poliza) for item in participaciones):
            raise ValueError("La póliza seleccionada no está vinculada a este asegurado.")

    @staticmethod
    def _validar_total_porcentaje(
        id_asegurado: int,
        porcentaje: float,
        *,
        id_poliza: int | None,
        exclude_id: int | None = None,
    ) -> None:
        total_actual = BeneficiarioRepository.get_total_porcentaje_by_asegurado(
            id_asegurado,
            id_poliza=id_poliza,
            exclude_id=exclude_id,
        )
        if round(total_actual + porcentaje, 4) > 100.0:
            raise ValueError("La suma de porcentajes de beneficiarios no puede exceder 100.")

    @staticmethod
    def create(data: dict) -> Beneficiario:
        payload = data.copy()

        validar_requerido(payload.get("id_asegurado"), "id_asegurado")
        validar_requerido(payload.get("nombre_completo", ""), "nombre_completo")
        validar_requerido(payload.get("parentesco", ""), "parentesco")
        validar_telefono(payload.get("telefono"), "telefono")

        payload["id_poliza"] = BeneficiarioService._normalize_id_poliza(payload.get("id_poliza"))

        id_asegurado = int(payload["id_asegurado"])
        id_poliza = payload.get("id_poliza")
        BeneficiarioService._validar_poliza_de_asegurado(id_asegurado, id_poliza)

        porcentaje = float(payload.get("porcentaje_participacion", 0))
        validar_porcentaje(porcentaje)
        BeneficiarioService._validar_total_porcentaje(
            id_asegurado,
            porcentaje,
            id_poliza=id_poliza,
        )
        return BeneficiarioRepository.create(Beneficiario(**payload))

    @staticmethod
    def get_by_id(id_beneficiario: int) -> Beneficiario | None:
        return BeneficiarioRepository.get_by_id(id_beneficiario)

    @staticmethod
    def get_all() -> list[Beneficiario]:
        return BeneficiarioRepository.get_all()

    @staticmethod
    def get_by_asegurado(id_asegurado: int) -> list[Beneficiario]:
        return BeneficiarioRepository.get_by_asegurado(id_asegurado)

    @staticmethod
    def update(id_beneficiario: int, data: dict) -> Beneficiario | None:
        entity = BeneficiarioRepository.get_by_id(id_beneficiario)
        if not entity:
            return None

        payload = data.copy()
        if "id_poliza" in payload:
            payload["id_poliza"] = BeneficiarioService._normalize_id_poliza(payload.get("id_poliza"))
        if "nombre_completo" in payload:
            validar_requerido(payload.get("nombre_completo", ""), "nombre_completo")
        if "parentesco" in payload:
            validar_requerido(payload.get("parentesco", ""), "parentesco")
        if "telefono" in payload:
            validar_telefono(payload.get("telefono"), "telefono")

        id_asegurado = int(payload.get("id_asegurado", entity.id_asegurado))
        id_poliza = payload.get("id_poliza", entity.id_poliza)
        BeneficiarioService._validar_poliza_de_asegurado(id_asegurado, id_poliza)
        porcentaje = float(payload.get("porcentaje_participacion", entity.porcentaje_participacion))
        if "id_asegurado" in payload or "id_poliza" in payload or "porcentaje_participacion" in payload:
            validar_porcentaje(porcentaje)
            BeneficiarioService._validar_total_porcentaje(
                id_asegurado,
                porcentaje,
                id_poliza=id_poliza,
                exclude_id=id_beneficiario,
            )

        return BeneficiarioRepository.update(id_beneficiario, payload)

    @staticmethod
    def delete(id_beneficiario: int) -> bool:
        return BeneficiarioRepository.delete(id_beneficiario)
