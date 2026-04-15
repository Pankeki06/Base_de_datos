"""Controlador de autenticación."""

from services.auth_service import login_agente


class AuthController:
    @staticmethod
    def login(clave_agente: str, password: str) -> dict:
        """Valida clave + contraseña de agente y devuelve resultado."""
        if not clave_agente or not clave_agente.strip():
            return {"ok": False, "error": "Debe ingresar la clave de agente."}
        if not password or not password.strip():
            return {"ok": False, "error": "Debe ingresar la contraseña."}
        try:
            agente = login_agente(clave_agente.strip(), password)
            if not agente:
                return {"ok": False, "error": "Clave o contraseña incorrecta."}
            return {"ok": True, "data": agente}
        except Exception as e:
            return {"ok": False, "error": str(e)}