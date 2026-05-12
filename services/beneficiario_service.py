from models.beneficiario import Beneficiario
from models.asegurado import Asegurado
from repositories.asegurado_repository import AseguradoRepository
from repositories.beneficiario_repository import BeneficiarioRepository
from repositories.poliza_repository import PolizaRepository
from services.validators import validar_porcentaje, validar_requerido, validar_telefono


class BeneficiarioService:
    @staticmethod
    def _normalize_id(value) -> int | None:
        if value in (None, ""):
            return None
        return int(value)

    @staticmethod
    def _validar_vinculo_asegurado_poliza(id_asegurado: int, id_poliza: int) -> None:
        """Valida que el asegurado (titular o dependiente) esté vinculado a la póliza."""
        poliza = PolizaRepository.get_by_id(id_poliza)
        if not poliza:
            raise ValueError("La póliza seleccionada no existe o ya no está disponible.")
        
        asegurado = AseguradoRepository.get_by_id(id_asegurado)
        if not asegurado:
            raise ValueError("El asegurado no existe.")
        
        # Es titular de la póliza
        if poliza.id_asegurado == id_asegurado:
            return
        
        # Es dependiente de esta póliza
        if asegurado.id_poliza == id_poliza:
            return
        
        raise ValueError("El asegurado no está vinculado a esta póliza.")

    @staticmethod
    def _validar_total_porcentaje(
        id_poliza: int,
        id_asegurado: int,
        porcentaje: float,
        *,
        exclude_id: int | None = None,
    ) -> None:
        """Valida que el porcentaje acumulado del asegurado no exceda 100%."""
        total_actual = BeneficiarioRepository.get_total_porcentaje_by_asegurado(
            id_poliza,
            id_asegurado,
            exclude_id=exclude_id,
        )
        if round(total_actual + porcentaje, 4) > 100.0:
            raise ValueError("La suma de porcentajes de beneficiarios no puede exceder 100.")

    @staticmethod
    def create(data: dict) -> Beneficiario:
        payload = data.copy()

        id_asegurado = BeneficiarioService._normalize_id(payload.get("id_asegurado"))
        id_poliza = BeneficiarioService._normalize_id(payload.get("id_poliza"))

        if id_poliza is None:
            raise ValueError("El campo 'id_poliza' es obligatorio.")
        if id_asegurado is None:
            raise ValueError("El campo 'id_asegurado' es obligatorio.")

        validar_requerido(payload.get("nombre_completo", ""), "nombre_completo")
        validar_requerido(payload.get("parentesco", ""), "parentesco")
        validar_telefono(payload.get("telefono"), "telefono")

        # Validar que el asegurado está vinculado a la póliza
        BeneficiarioService._validar_vinculo_asegurado_poliza(id_asegurado, id_poliza)

        payload["id_poliza"] = id_poliza
        payload["id_asegurado"] = id_asegurado

        porcentaje = float(payload.get("porcentaje_participacion", 0))
        validar_porcentaje(porcentaje)
        BeneficiarioService._validar_total_porcentaje(id_poliza, id_asegurado, porcentaje)

        return BeneficiarioRepository.create(Beneficiario(**payload))

    @staticmethod
    def get_by_id(id_beneficiario: int) -> Beneficiario | None:
        return BeneficiarioRepository.get_by_id(id_beneficiario)

    @staticmethod
    def get_all() -> list[Beneficiario]:
        return BeneficiarioRepository.get_all()

    @staticmethod
    def get_by_asegurado(id_asegurado: int) -> list[Beneficiario]:
        """Retorna beneficiarios de un asegurado (titular o dependiente)."""
        return BeneficiarioRepository.get_by_asegurado(id_asegurado)

    @staticmethod
    def get_by_poliza(id_poliza: int) -> list[Beneficiario]:
        """Retorna todos los beneficiarios de una póliza."""
        return BeneficiarioRepository.get_by_poliza(id_poliza)

    @staticmethod
    def update(id_beneficiario: int, data: dict) -> Beneficiario | None:
        entity = BeneficiarioRepository.get_by_id(id_beneficiario)
        if not entity:
            return None

        payload = data.copy()
        if "id_poliza" in payload:
            payload["id_poliza"] = BeneficiarioService._normalize_id(payload.get("id_poliza"))
        if "nombre_completo" in payload:
            validar_requerido(payload.get("nombre_completo", ""), "nombre_completo")
        if "parentesco" in payload:
            validar_requerido(payload.get("parentesco", ""), "parentesco")
        if "telefono" in payload:
            validar_telefono(payload.get("telefono"), "telefono")

        id_poliza = payload.get("id_poliza", entity.id_poliza)
        id_asegurado = payload.get("id_asegurado", entity.id_asegurado)
        
        # Validar cambio de asegurado/póliza si se está actualizando
        if "id_asegurado" in payload or "id_poliza" in payload:
            BeneficiarioService._validar_vinculo_asegurado_poliza(id_asegurado, id_poliza)

        if "porcentaje_participacion" in payload:
            porcentaje = float(payload["porcentaje_participacion"])
            validar_porcentaje(porcentaje)
            BeneficiarioService._validar_total_porcentaje(
                id_poliza,
                id_asegurado,
                porcentaje,
                exclude_id=id_beneficiario,
            )

        return BeneficiarioRepository.update(id_beneficiario, payload)

    @staticmethod
    def delete(id_beneficiario: int) -> bool:
        return BeneficiarioRepository.delete(id_beneficiario)
