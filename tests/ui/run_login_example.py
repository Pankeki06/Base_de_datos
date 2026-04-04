import flet as ft
from views.login_view import create_login_view


def main(page: ft.Page):
    """Ejecuta solamente la vista de login para revisión manual."""
    
    def login(clave: str, pwd: str, validation_text: ft.Text, page_obj: ft.Page):
        validation_text.value = f"Ingresaste: {clave} / {pwd}"
        page_obj.update()

    page.add(create_login_view(page, login))


if __name__ == "__main__":
    ft.run(main)
