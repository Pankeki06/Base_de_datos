from services.auth_service import authenticate


class DummySession:
    """Sesión falsificada para simular la base de datos."""

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def exec(self, statement):
        class DummyResult:
            def first(self):
                return object()

        return DummyResult()


def test_authenticate_calls_service_with_valid_user(monkeypatch):
    """Prueba la función authenticate sin conectar a la base de datos real."""
    monkeypatch.setattr("services.auth_service.create_session", lambda: DummySession())

    result = authenticate("admin001", "Seguros123!")
    assert result is True


def test_authenticate_returns_false_when_user_not_found(monkeypatch):
    """Prueba la función authenticate cuando no existe el usuario."""

    class EmptySession(DummySession):
        def exec(self, statement):
            class EmptyResult:
                def first(self):
                    return None

            return EmptyResult()

    monkeypatch.setattr("services.auth_service.create_session", lambda: EmptySession())

    result = authenticate("no_existe", "123")
    assert result is False
