import flet as ft
from views.login_view import LoginView, create_login_view


class DummyPage:
    """Página mínima para pruebas de UI."""

    def __init__(self):
        self.controls = []

    def update(self):
        pass

    def add(self, control):
        self.controls.append(control)


class FocusPage(DummyPage):
    def __init__(self):
        super().__init__()
        self.run_task_calls = []

    def run_task(self, handler, *args, **kwargs):
        self.run_task_calls.append((handler, args, kwargs))


def test_login_view_shows_login_fields_and_button():
    """Verifica que la vista de login contiene los controles esperados."""
    page = DummyPage()
    clicked = {"called": False}

    def login_callback(clave, pwd, validation_text, page_obj):
        clicked["called"] = True
        assert clave == "user123"
        assert pwd == "pass123"
        assert isinstance(validation_text, ft.Text)
        assert page_obj is page

    login_view = create_login_view(page, login_callback)

    assert isinstance(login_view, ft.Column)
    assert any(isinstance(control, ft.TextField) and control.label == "Clave de agente" for control in login_view.controls)
    assert any(isinstance(control, ft.TextField) and control.label == "Contraseña" for control in login_view.controls)
    assert any(isinstance(control, ft.Button) for control in login_view.controls)

    # Llenar los campos de texto como lo haría el usuario
    username_field = next(control for control in login_view.controls if isinstance(control, ft.TextField) and control.label == "Clave de agente")
    password_field = next(control for control in login_view.controls if isinstance(control, ft.TextField) and control.label == "Contraseña")
    username_field.value = "user123"
    password_field.value = "pass123"

    login_button = next(control for control in login_view.controls if isinstance(control, ft.Button))
    login_button.on_click(None)
    assert clicked["called"] is True


def test_login_view_programa_focus_con_run_task():
    page = FocusPage()
    view = LoginView(page, lambda *_args, **_kwargs: None)
    control = ft.TextField(label="Contraseña")

    view._focus_control(control)

    assert len(page.run_task_calls) == 1
    scheduled, args, kwargs = page.run_task_calls[0]
    assert scheduled == control.focus
    assert args == ()
    assert kwargs == {}
