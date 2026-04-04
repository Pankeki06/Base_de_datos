from config.database import create_session


def test_create_session_returns_session():
    """Llama a create_session() y verifica que retorna una sesión válida."""
    session = create_session()
    assert session is not None
    session.close()
