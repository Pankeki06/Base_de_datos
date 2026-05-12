from .agente_repository import AgenteRepository
from .asegurado_repository import AseguradoRepository
from .beneficiario_repository import BeneficiarioRepository
from .beneficio_repository import BeneficioRepository
from .poliza_repository import PolizaRepository
from .producto_poliza_repository import ProductoPolizaRepository
from .producto_beneficio_repository import ProductoBeneficioRepository
from .seguimiento_repository import SeguimientoRepository
from .seguimiento_contacto_repository import SeguimientoContactoRepository

__all__ = [
    "AgenteRepository",
    "AseguradoRepository",
    "BeneficiarioRepository",
    "BeneficioRepository",
    "PolizaRepository",
    "ProductoPolizaRepository",
    "ProductoBeneficioRepository",
    "SeguimientoRepository",
    "SeguimientoContactoRepository",
]
