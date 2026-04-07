"""Controlador de autenticación."""

from services.auth_service import login_agente


class AuthController:
    @staticmethod
    def login(clave_agente: str, password: str) -> dict:
        """Valida credenciales y devuelve resultado. No toca la UI."""
        if not clave_agente or not password:
            return {"ok": False, "error": "Debe ingresar clave y contraseña."}
        try:
            agente = login_agente(clave_agente, password)
            if not agente:
                return {"ok": False, "error": "Clave o contraseña incorrecta."}
            return {"ok": True, "data": agente}
        except Exception as e:
            return {"ok": False, "error": str(e)}