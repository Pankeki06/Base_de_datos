from datetime import datetime
from types import SimpleNamespace

import flet as ft
import services.session_manager as session_manager
from views import dashboard_view as dashboard_module
from views import ui_controls as ui_controls_module
from views.asegurado import asignaciones_view as asignaciones_module
from views.asegurado import detalle_view as detalle_module
from views.asegurado import formulario_view as formulario_module
from views.asegurado import lista_view as asegurados_lista_module
from views.polizas import lista_view as polizas_module


class DummyPage:
    def __init__(self):
        self.controls = []
        self.dialogs = []
        self.pop_dialog_calls = 0
        self.run_task_calls = []

    def update(self):
        pass

    def add(self, control):
        self.controls.append(control)

    def show_dialog(self, dialog):
        self.dialogs.append(dialog)

    def pop_dialog(self):
        self.pop_dialog_calls += 1

    def run_task(self, handler, *args, **kwargs):
        self.run_task_calls.append((handler, args, kwargs))


def _walk_controls(control):
    if control is None:
        return
    if getattr(control, "visible", True) is False:
        return
    yield control

    for attr in ("content", "title", "subtitle", "leading", "trailing"):
        child = getattr(control, attr, None)
        if child is not None:
            yield from _walk_controls(child)

    for attr in ("controls", "actions"):
        children = getattr(control, attr, None)
        if children:
            for child in children:
                yield from _walk_controls(child)


def _find_first(control, control_type, predicate=lambda _control: True):
    return next(
        item
        for item in _walk_controls(control)
        if isinstance(item, control_type) and predicate(item)
    )


def _find_text_values(control) -> list[str]:
    return [item.value for item in _walk_controls(control) if isinstance(item, ft.Text) and item.value]


def _button_label(control) -> str | None:
    text = getattr(control, "text", None)
    if text:
        return text

    content = getattr(control, "content", None)
    if isinstance(content, str):
        return content
    if isinstance(content, ft.Text):
        return content.value

    return getattr(content, "value", None)


def test_dashboard_view_build_smoke(monkeypatch):
    page = DummyPage()

    monkeypatch.setattr(
        dashboard_module,
        "obtener_agente",
        lambda: SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz"),
    )
    monkeypatch.setattr(dashboard_module.DashboardView, "_build_recientes", lambda self: ft.Text("Recientes"))
    monkeypatch.setattr(dashboard_module.DashboardView, "_build_kpis", lambda self: ft.Text("KPIs"))

    view = dashboard_module.DashboardView(page, lambda *_args, **_kwargs: None)
    control = view.build()

    assert isinstance(control, ft.Container)


def test_sidebar_muestra_boton_agentes_solo_para_admin(monkeypatch):
    monkeypatch.setattr(
        session_manager,
        "obtener_agente",
        lambda: SimpleNamespace(id_agente=1, rol="admin"),
    )

    sidebar = ui_controls_module.app_sidebar(lambda *_args, **_kwargs: None, "/dashboard")
    tooltips = [
        getattr(item, "tooltip", None)
        for item in _walk_controls(sidebar)
        if getattr(item, "tooltip", None)
    ]

    assert "Agentes" in tooltips


def test_sidebar_oculta_boton_agentes_para_agente_normal(monkeypatch):
    monkeypatch.setattr(
        session_manager,
        "obtener_agente",
        lambda: SimpleNamespace(id_agente=2, rol="agente"),
    )

    sidebar = ui_controls_module.app_sidebar(lambda *_args, **_kwargs: None, "/dashboard")
    tooltips = [
        getattr(item, "tooltip", None)
        for item in _walk_controls(sidebar)
        if getattr(item, "tooltip", None)
    ]

    assert "Agentes" not in tooltips


def test_lista_polizas_view_build_carga_productos_y_beneficios(monkeypatch):
    page = DummyPage()
    producto = SimpleNamespace(
        id_producto=1,
        nombre="Vida Integral",
        tipo_seguro="Vida",
        activo=True,
        prima_base=650.0,
        descripcion="Plan de prueba",
    )
    beneficio = SimpleNamespace(
        id_producto_beneficio=10,
        nombre_beneficio="Cobertura base",
        monto_cobertura=150000.0,
        incluido_base=True,
    )

    monkeypatch.setattr(
        polizas_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto]},
    )
    monkeypatch.setattr(
        polizas_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda id_producto: {"ok": True, "data": [beneficio] if id_producto == 1 else []},
    )

    view = polizas_module.ListaPolizasView(page, lambda *_args, **_kwargs: None)
    control = view.build()

    assert isinstance(control, ft.Container)
    assert len(view._productos) == 1
    assert view._beneficios_map[1][0].nombre_beneficio == "Cobertura base"


def test_lista_polizas_crea_beneficio_opcional_con_costo_extra(monkeypatch):
    page = DummyPage()
    captured_payload = {}
    producto = SimpleNamespace(
        id_producto=1,
        nombre="Vida Integral",
        tipo_seguro="Vida",
        activo=True,
        prima_base=650.0,
        descripcion="Plan de prueba",
    )

    monkeypatch.setattr(
        polizas_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto]},
    )
    monkeypatch.setattr(
        polizas_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda _id_producto: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        polizas_module.ProductoBeneficioController,
        "create_producto_beneficio",
        lambda payload: captured_payload.update(payload) or {"ok": True, "data": SimpleNamespace(id_producto_beneficio=7, **payload)},
    )

    view = polizas_module.ListaPolizasView(page, lambda *_args, **_kwargs: None)
    control = view.build()

    add_button = _find_first(
        control,
        ft.TextButton,
        lambda item: "Agregar" in _find_text_values(item),
    )
    add_button.on_click(None)

    dialog = page.dialogs[-1]
    labels = {
        field.label: field
        for field in _walk_controls(dialog)
        if isinstance(field, ft.TextField)
    }
    base_sw = _find_first(dialog, ft.Switch, lambda item: item.label == "Incluido en base (sin costo extra)")

    labels["Nombre del beneficio"].value = "Dental premium"
    labels["Monto de cobertura"].value = "18000"
    labels["Descripcion"].value = "Cobertura dental opcional"
    base_sw.value = False
    base_sw.on_change(SimpleNamespace(control=base_sw))
    labels["Costo extra mensual"].value = "135"

    save_button = _find_first(dialog, ft.FilledButton, lambda item: _button_label(item) == "Guardar")
    save_button.on_click(None)

    assert captured_payload["incluido_base"] is False
    assert captured_payload["costo_extra"] == 135.0
    assert captured_payload["descripcion"] == "Cobertura dental opcional"


def test_lista_polizas_edita_beneficio_base_y_limpia_costo_extra(monkeypatch):
    page = DummyPage()
    captured_payload = {}
    producto = SimpleNamespace(
        id_producto=1,
        nombre="Vida Integral",
        tipo_seguro="Vida",
        activo=True,
        prima_base=650.0,
        descripcion="Plan de prueba",
    )
    beneficio = SimpleNamespace(
        id_producto_beneficio=10,
        nombre_beneficio="Dental premium",
        descripcion="Cobertura dental opcional",
        monto_cobertura=18000.0,
        incluido_base=False,
        costo_extra=135.0,
    )

    monkeypatch.setattr(
        polizas_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto]},
    )
    monkeypatch.setattr(
        polizas_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda _id_producto: {"ok": True, "data": [beneficio]},
    )
    monkeypatch.setattr(
        polizas_module.ProductoBeneficioController,
        "update_producto_beneficio",
        lambda id_beneficio, payload: captured_payload.update({"id": id_beneficio, **payload}) or {"ok": True, "data": SimpleNamespace(id_producto_beneficio=id_beneficio, **payload)},
    )

    view = polizas_module.ListaPolizasView(page, lambda *_args, **_kwargs: None)
    control = view.build()

    edit_button = _find_first(control, ft.IconButton, lambda item: getattr(item, "tooltip", None) == "Editar beneficio")
    edit_button.on_click(None)

    dialog = page.dialogs[-1]
    labels = {
        field.label: field
        for field in _walk_controls(dialog)
        if isinstance(field, ft.TextField)
    }
    base_sw = _find_first(dialog, ft.Switch, lambda item: item.label == "Incluido en base")
    base_sw.value = True
    base_sw.on_change(SimpleNamespace(control=base_sw))

    save_button = _find_first(dialog, ft.FilledButton, lambda item: _button_label(item) == "Guardar")
    save_button.on_click(None)

    assert labels["Costo extra mensual"].disabled is True
    assert captured_payload["incluido_base"] is True
    assert captured_payload["costo_extra"] is None


def test_formulario_asegurado_build_smoke(monkeypatch):
    page = DummyPage()

    monkeypatch.setattr(
        session_manager,
        "obtener_agente",
        lambda: SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz"),
    )

    view = formulario_module.FormularioAseguradoView(page, lambda *_args, **_kwargs: None)
    control = view.build()

    assert isinstance(control, ft.Container)


def test_formulario_asegurado_modal_vinculo_muestra_polizas_disponibles(monkeypatch):
    page = DummyPage()
    poliza = SimpleNamespace(id_poliza=7, numero_poliza="POL-UI-07")

    monkeypatch.setattr(
        formulario_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda id_asegurado: {"ok": True, "data": [poliza]},
    )

    view = formulario_module.FormularioAseguradoView(page, lambda *_args, **_kwargs: None)
    view._open_link_to_existing_poliza_modal(10)

    assert len(page.dialogs) == 1
    dialog = page.dialogs[0]
    assert isinstance(dialog, ft.AlertDialog)
    poliza_dd = dialog.content.controls[0]
    assert isinstance(poliza_dd, ft.Dropdown)
    assert poliza_dd.options[0].key == "7"
    assert poliza_dd.options[0].text == "POL-UI-07"


def test_formulario_asegurado_post_save_redirige_a_asignaciones():
    page = DummyPage()
    nav_calls = []

    def navigate(route, **kwargs):
        nav_calls.append((route, kwargs))

    view = formulario_module.FormularioAseguradoView(page, navigate)
    view._show_post_save_options(44)

    assert len(page.dialogs) == 1
    dialog = page.dialogs[0]
    action = next(button for button in dialog.actions if isinstance(button, ft.FilledButton))

    action.on_click(None)

    assert nav_calls == [("/asegurado/asignaciones", {"id_asegurado": 44})]


def test_lista_asegurados_row_polizas_muestra_resumen_y_afiliados_sin_avatar(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=10,
        id_agente_responsable=1,
        nombre="Roberto",
        apellido_paterno="Martinez",
        apellido_materno="Soto",
        rfc="ROMS900101AA1",
        celular="5511111111",
    )
    polizas = [
        SimpleNamespace(
            id_poliza=21,
            numero_poliza="POL-VIDA-01",
            estatus="activa",
            prima_mensual=1200.0,
            fecha_inicio="2026-01-01",
            fecha_vencimiento="2027-01-01",
        ),
        SimpleNamespace(
            id_poliza=22,
            numero_poliza="POL-GMM-02",
            estatus="activa",
            prima_mensual=2100.0,
            fecha_inicio="2026-02-01",
            fecha_vencimiento="2027-02-01",
        ),
    ]

    monkeypatch.setattr(
        asegurados_lista_module,
        "obtener_agente",
        lambda: SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz"),
    )

    view = asegurados_lista_module.ListaAseguradoView(page, lambda *_args, **_kwargs: None)
    view._search_scope = "portfolio"
    view._asegurados_ids = {10, 11, 12, 13}
    view._participantes_poliza_map = {
        21: [
            {"id_asegurado": 10, "nombre_completo": "Roberto Martinez", "tipo_participante": "titular"},
            {"id_asegurado": 11, "nombre_completo": "Patricia Velazquez", "tipo_participante": "conyuge"},
            {"id_asegurado": 12, "nombre_completo": "Emilio Martinez", "tipo_participante": "hijo"},
            {"id_asegurado": 13, "nombre_completo": "Camila Martinez", "tipo_participante": "hijo"},
        ],
        22: [
            {"id_asegurado": 10, "nombre_completo": "Roberto Martinez", "tipo_participante": "titular"},
        ],
    }

    control = view._build_row(asegurado, polizas, participaciones=[])

    texts = _find_text_values(control)
    icons = {
        getattr(item, "name", None) or getattr(item, "icon", None)
        for item in _walk_controls(control)
        if isinstance(item, ft.Icon)
    }

    assert isinstance(control.content, ft.Column)
    assert "Total mensual" in texts
    assert "$3,300" in texts
    assert "2 póliza(s) · 4 persona(s)" in texts
    assert "POL-VIDA-01" in texts
    assert "POL-GMM-02" in texts
    assert "Roberto Martinez" in texts
    assert "Patricia V." in texts
    assert "Emilio M." in texts
    assert ft.Icons.PERSON_ROUNDED not in icons
    assert ft.Icons.GROUP_OUTLINED not in icons


def test_detalle_asegurado_build_conserva_mapa_historico_y_catalogo_activo(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=5,
        id_agente_responsable=1,
        nombre="Laura",
        apellido_paterno="Historica",
        apellido_materno="Test",
        rfc="LAHI900101AA1",
        correo="laura@test.com",
        celular="5512345678",
        calle="Calle Uno",
        numero_exterior="10",
        numero_interior="2",
        colonia="Centro",
        municipio="Monterrey",
        estado="Nuevo Leon",
        codigo_postal="64000",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto_activo = SimpleNamespace(id_producto=1, nombre="Activo", tipo_seguro="Vida")
    producto_inactivo = SimpleNamespace(id_producto=2, nombre="Historico", tipo_seguro="Vida")
    poliza_historica = SimpleNamespace(
        id_poliza=11,
        id_producto=2,
        numero_poliza="POL-HIST-01",
        estatus="activa",
        prima_mensual=800.0,
        fecha_inicio="2026-01-01",
        fecha_vencimiento="2027-01-01",
    )

    monkeypatch.setattr(
        detalle_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        detalle_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        detalle_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": [poliza_historica]},
    )
    monkeypatch.setattr(
        detalle_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        detalle_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto_activo, producto_inactivo]},
    )
    monkeypatch.setattr(
        detalle_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        detalle_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda _id_producto: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        detalle_module.BeneficioController,
        "get_beneficios_by_poliza",
        lambda _id_poliza: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        detalle_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        detalle_module.SeguimientoController,
        "get_seguimientos_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )

    view = detalle_module.DetalleAseguradoView(page, lambda *_args, **_kwargs: None, id_asegurado=5)
    control = view.build()

    assert isinstance(control, ft.Container)
    assert set(view._producto_map) == {1, 2}
    assert [producto.id_producto for producto in view._productos_activos] == [1]
    assert view._polizas[0].numero_poliza == "POL-HIST-01"


def test_detalle_asegurado_beneficiarios_se_muestran_separados_por_poliza(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=5,
        id_agente_responsable=1,
        nombre="Laura",
        apellido_paterno="Beneficiaria",
        apellido_materno="Detalle",
        rfc="LABD900101AA1",
        correo="laura@test.com",
        celular="5512345678",
        calle="Calle Uno",
        numero_exterior="10",
        numero_interior="2",
        colonia="Centro",
        municipio="Monterrey",
        estado="Nuevo Leon",
        codigo_postal="64000",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto_a = SimpleNamespace(id_producto=1, nombre="Vida Integral", tipo_seguro="Vida")
    producto_b = SimpleNamespace(id_producto=2, nombre="GMM Familiar", tipo_seguro="Gastos")
    poliza_a = SimpleNamespace(
        id_poliza=11,
        id_producto=1,
        numero_poliza="POL-DET-01",
        estatus="activa",
        prima_mensual=800.0,
        fecha_inicio="2026-01-01",
        fecha_vencimiento="2027-01-01",
    )
    poliza_b = SimpleNamespace(
        id_poliza=12,
        id_producto=2,
        numero_poliza="POL-DET-02",
        estatus="activa",
        prima_mensual=950.0,
        fecha_inicio="2026-02-01",
        fecha_vencimiento="2027-02-01",
    )
    beneficiario_a = SimpleNamespace(
        id_beneficiario=1,
        id_poliza=11,
        nombre_completo="Mario Test",
        parentesco="Conyuge",
        porcentaje_participacion=60.0,
        telefono="5511111111",
    )
    beneficiario_b = SimpleNamespace(
        id_beneficiario=2,
        id_poliza=12,
        nombre_completo="Daniel Test",
        parentesco="Hijo",
        porcentaje_participacion=40.0,
        telefono="5522222222",
    )

    monkeypatch.setattr(
        detalle_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        detalle_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        detalle_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": [poliza_a, poliza_b]},
    )
    monkeypatch.setattr(
        detalle_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        detalle_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto_a, producto_b]},
    )
    monkeypatch.setattr(
        detalle_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto_a, producto_b]},
    )
    monkeypatch.setattr(
        detalle_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda _id_producto: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        detalle_module.BeneficioController,
        "get_beneficios_by_poliza",
        lambda _id_poliza: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        detalle_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": [beneficiario_a, beneficiario_b]},
    )
    monkeypatch.setattr(
        detalle_module.SeguimientoController,
        "get_seguimientos_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )

    view = detalle_module.DetalleAseguradoView(page, lambda *_args, **_kwargs: None, id_asegurado=5)
    view.build()
    beneficiarios_tab = view._tab_beneficiarios()
    texts = _find_text_values(beneficiarios_tab)

    assert "Beneficiarios cargados: 2 · Polizas con beneficiarios: 2" in texts
    assert "Poliza en trabajo" in texts
    assert (
        "Poliza POL-DET-01" in texts
        or "Poliza POL-DET-02" in texts
    )
    assert (
        "Mario Test" in texts
        or "Daniel Test" in texts
    )
    assert (
        "Total asignado en esta poliza: 60%" in texts
        or "Total asignado en esta poliza: 40%" in texts
    )


def test_asignaciones_asegurado_build_carga_polizas_beneficiarios_y_beneficios(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=8,
        id_agente_responsable=1,
        nombre="Rocio",
        apellido_paterno="Asignacion",
        apellido_materno="Test",
        rfc="ROAT900101AA1",
        correo="rocio@test.com",
        celular="5512345609",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto_activo = SimpleNamespace(id_producto=1, nombre="Producto Activo", tipo_seguro="Vida")
    poliza = SimpleNamespace(
        id_poliza=21,
        id_producto=1,
        numero_poliza="POL-ASIG-01",
        estatus="activa",
        prima_mensual=900.0,
        fecha_inicio="2026-01-01",
        fecha_vencimiento="2027-01-01",
    )
    poliza_externa = SimpleNamespace(id_poliza=99, numero_poliza="POL-DISP-99")
    beneficiario = SimpleNamespace(
        id_beneficiario=1,
        id_poliza=21,
        nombre_completo="Mario Test",
        parentesco="Conyuge",
        porcentaje_participacion=50.0,
        telefono="5511111111",
    )
    beneficio = SimpleNamespace(
        id_beneficio=1,
        id_asegurado_poliza=None,
        nombre_beneficio="Hospitalizacion",
        descripcion="Cobertura general",
        monto_cobertura=120000.0,
    )
    participante = {
        "id_asegurado_poliza": 15,
        "id_asegurado": 8,
        "tipo_participante": "titular",
        "nombre_completo": "Rocio Asignacion Test",
    }

    monkeypatch.setattr(
        asignaciones_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        asignaciones_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": [poliza]},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda _id: {"ok": True, "data": [poliza_externa]},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participantes_by_poliza",
        lambda _id: {"ok": True, "data": [participante]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda _id_producto: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": [beneficiario]},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficioController,
        "get_beneficios_by_poliza",
        lambda _id: {"ok": True, "data": [beneficio]},
    )

    view = asignaciones_module.AsignacionesAseguradoView(
        page,
        lambda *_args, **_kwargs: None,
        id_asegurado=8,
    )
    control = view.build()
    tab_bar = _find_first(
        control,
        ft.TabBar,
        lambda item: [tab.label for tab in item.tabs] == ["Polizas", "Beneficiarios", "Beneficios"],
    )

    assert isinstance(control, ft.Container)
    assert len(view._polizas) == 1
    assert len(view._beneficiarios) == 1
    assert view._available_polizas[0].numero_poliza == "POL-DISP-99"
    assert view._beneficios_map[21][0].nombre_beneficio == "Hospitalizacion"
    assert [tab.label for tab in tab_bar.tabs] == ["Polizas", "Beneficiarios", "Beneficios"]
    assert not any(isinstance(item, ft.TabBarView) for item in _walk_controls(control))


def test_asignaciones_asegurado_abre_beneficios_cuando_recibe_focus_poliza(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=8,
        id_agente_responsable=1,
        nombre="Rocio",
        apellido_paterno="Focus",
        apellido_materno="Test",
        rfc="ROFO900101AA1",
        correo="rocio@test.com",
        celular="5512345609",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto_activo = SimpleNamespace(id_producto=1, nombre="Producto Activo", tipo_seguro="Vida")
    poliza = SimpleNamespace(
        id_poliza=21,
        id_producto=1,
        numero_poliza="POL-ASIG-01",
        estatus="activa",
        prima_mensual=900.0,
        fecha_inicio="2026-01-01",
        fecha_vencimiento="2027-01-01",
    )

    monkeypatch.setattr(
        asignaciones_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        asignaciones_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": [poliza]},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participantes_by_poliza",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda _id_producto: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficioController,
        "get_beneficios_by_poliza",
        lambda _id: {"ok": True, "data": []},
    )

    view = asignaciones_module.AsignacionesAseguradoView(
        page,
        lambda *_args, **_kwargs: None,
        id_asegurado=8,
        focus_poliza_id=21,
    )
    control = view.build()
    tabs = _find_first(control, ft.Tabs, lambda item: item.length == 3)
    texts = _find_text_values(control)

    assert tabs.selected_index == 2
    assert "Vinculo completado. Continua con los beneficios de la poliza POL-ASIG-01." in texts


def test_asignaciones_asegurado_selecciona_poliza_en_beneficios(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=8,
        id_agente_responsable=1,
        nombre="Rocio",
        apellido_paterno="Selector",
        apellido_materno="Poliza",
        rfc="ROSP900101AA1",
        correo="rocio@test.com",
        celular="5512345609",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto = SimpleNamespace(id_producto=1, nombre="Vida Plus", tipo_seguro="Vida")
    poliza_a = SimpleNamespace(
        id_poliza=21,
        id_producto=1,
        numero_poliza="POL-ASIG-01",
        estatus="activa",
        prima_mensual=900.0,
        fecha_inicio="2026-01-01",
        fecha_vencimiento="2027-01-01",
    )
    poliza_b = SimpleNamespace(
        id_poliza=22,
        id_producto=1,
        numero_poliza="POL-ASIG-02",
        estatus="activa",
        prima_mensual=950.0,
        fecha_inicio="2026-02-01",
        fecha_vencimiento="2027-02-01",
    )
    beneficio_a = SimpleNamespace(
        id_beneficio=1,
        id_asegurado_poliza=None,
        nombre_beneficio="Hospitalizacion",
        descripcion="Cobertura general",
        monto_cobertura=120000.0,
    )
    beneficio_b = SimpleNamespace(
        id_beneficio=2,
        id_asegurado_poliza=None,
        nombre_beneficio="Dental",
        descripcion="Cobertura dental",
        monto_cobertura=35000.0,
    )

    monkeypatch.setattr(
        asignaciones_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        asignaciones_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": [poliza_a, poliza_b]},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participantes_by_poliza",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda _id_producto: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficioController,
        "get_beneficios_by_poliza",
        lambda id_poliza: {"ok": True, "data": [beneficio_a] if id_poliza == 21 else [beneficio_b]},
    )

    view = asignaciones_module.AsignacionesAseguradoView(
        page,
        lambda *_args, **_kwargs: None,
        id_asegurado=8,
        focus_poliza_id=21,
    )
    control = view.build()

    texts = _find_text_values(control)
    poliza_b_btn = _find_first(
        control,
        ft.FilledButton,
        lambda item: _button_label(item) == "POL-ASIG-02",
    )

    assert "Hospitalizacion" in texts
    assert "Dental" not in texts

    poliza_b_btn.on_click(None)
    texts = _find_text_values(control)

    assert "Dental" in texts
    assert "Hospitalizacion" not in texts


def test_asignaciones_asegurado_selecciona_poliza_en_beneficiarios(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=8,
        id_agente_responsable=1,
        nombre="Rocio",
        apellido_paterno="Selector",
        apellido_materno="Beneficiario",
        rfc="ROSB900101AA1",
        correo="rocio@test.com",
        celular="5512345609",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto = SimpleNamespace(id_producto=1, nombre="Vida Plus", tipo_seguro="Vida")
    poliza_a = SimpleNamespace(
        id_poliza=21,
        id_producto=1,
        numero_poliza="POL-ASIG-01",
        estatus="activa",
        prima_mensual=900.0,
        fecha_inicio="2026-01-01",
        fecha_vencimiento="2027-01-01",
    )
    poliza_b = SimpleNamespace(
        id_poliza=22,
        id_producto=1,
        numero_poliza="POL-ASIG-02",
        estatus="activa",
        prima_mensual=950.0,
        fecha_inicio="2026-02-01",
        fecha_vencimiento="2027-02-01",
    )
    beneficiario_a = SimpleNamespace(
        id_beneficiario=1,
        id_poliza=21,
        nombre_completo="Mario Test",
        parentesco="Conyuge",
        porcentaje_participacion=60.0,
        telefono="5511111111",
    )
    beneficiario_b = SimpleNamespace(
        id_beneficiario=2,
        id_poliza=22,
        nombre_completo="Daniel Test",
        parentesco="Hijo",
        porcentaje_participacion=40.0,
        telefono="5522222222",
    )

    monkeypatch.setattr(
        asignaciones_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        asignaciones_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": [poliza_a, poliza_b]},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participantes_by_poliza",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda _id_producto: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": [beneficiario_a, beneficiario_b]},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficioController,
        "get_beneficios_by_poliza",
        lambda _id: {"ok": True, "data": []},
    )

    view = asignaciones_module.AsignacionesAseguradoView(
        page,
        lambda *_args, **_kwargs: None,
        id_asegurado=8,
        focus_poliza_id=21,
        focus_tab="beneficiarios",
    )
    control = view.build()
    tabs = _find_first(control, ft.Tabs, lambda item: item.length == 3)

    texts = _find_text_values(control)
    poliza_b_btn = _find_first(
        control,
        ft.FilledButton,
        lambda item: _button_label(item) == "POL-ASIG-02",
    )

    assert tabs.selected_index == 1
    assert "Mario Test" in texts
    assert "Daniel Test" not in texts
    assert "Total asignado en esta poliza: 60%" in texts

    poliza_b_btn.on_click(None)
    texts = _find_text_values(control)

    assert "Daniel Test" in texts
    assert "Mario Test" not in texts
    assert "Total asignado en esta poliza: 40%" in texts


def test_asignaciones_asegurado_aplica_defaults_del_catalogo(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=8,
        id_agente_responsable=1,
        nombre="Rocio",
        apellido_paterno="Catalogo",
        apellido_materno="Test",
        rfc="ROCT900101AA1",
        correo="rocio@test.com",
        celular="5512345609",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto_activo = SimpleNamespace(
        id_producto=1,
        nombre="Vida Integral",
        tipo_seguro="Vida",
        prima_base=650.0,
    )
    producto_beneficio = SimpleNamespace(
        id_producto_beneficio=71,
        id_producto=1,
        nombre_beneficio="Cobertura base",
        descripcion="Proteccion principal",
        monto_cobertura=150000.0,
        incluido_base=True,
    )

    monkeypatch.setattr(
        asignaciones_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        asignaciones_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda id_producto: {"ok": True, "data": [producto_beneficio] if id_producto == 1 else []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )

    view = asignaciones_module.AsignacionesAseguradoView(
        page,
        lambda *_args, **_kwargs: None,
        id_asegurado=8,
    )
    control = view.build()

    producto_dd = _find_first(control, ft.Dropdown, lambda item: item.label == "Producto activo")
    prima_f = _find_first(control, ft.TextField, lambda item: item.label == "Prima mensual")
    texts = _find_text_values(control)

    assert producto_dd.value == "1"
    assert prima_f.value == "650.00"
    assert any(
        "Despues de crearla podras ajustar sus beneficios en la pestaña Beneficios." in value
        for value in texts
    )
    assert not any(isinstance(item, ft.Checkbox) for item in _walk_controls(control))


def test_asignaciones_asegurado_abre_datepicker_desde_formulario(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=8,
        id_agente_responsable=1,
        nombre="Rocio",
        apellido_paterno="Calendario",
        apellido_materno="Test",
        rfc="ROCL900101AA1",
        correo="rocio@test.com",
        celular="5512345609",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto_activo = SimpleNamespace(
        id_producto=1,
        nombre="Vida Integral",
        tipo_seguro="Vida",
        prima_base=650.0,
    )

    monkeypatch.setattr(
        asignaciones_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        asignaciones_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda _id_producto: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )

    view = asignaciones_module.AsignacionesAseguradoView(
        page,
        lambda *_args, **_kwargs: None,
        id_asegurado=8,
    )
    control = view.build()

    calendar_btn = _find_first(
        control,
        ft.IconButton,
        lambda item: item.tooltip == "Abrir calendario de inicio",
    )
    inicio_f = _find_first(control, ft.TextField, lambda item: item.label == "Fecha inicio (AAAA-MM-DD)")

    calendar_btn.on_click(None)
    page.dialogs[-1].on_change(SimpleNamespace(control=SimpleNamespace(value=datetime(2026, 4, 27, 6, 0))))

    assert isinstance(page.dialogs[-1], ft.DatePicker)
    assert inicio_f.value == "2026-04-27"


def test_asignaciones_asegurado_aplica_defaults_al_cambiar_producto(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=8,
        id_agente_responsable=1,
        nombre="Rocio",
        apellido_paterno="Cambio",
        apellido_materno="Producto",
        rfc="ROCP900101AA1",
        correo="rocio@test.com",
        celular="5512345609",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto_a = SimpleNamespace(id_producto=1, nombre="Vida Base", tipo_seguro="Vida", prima_base=450.0)
    producto_b = SimpleNamespace(id_producto=2, nombre="Accidentes Plus", tipo_seguro="Accidentes", prima_base=725.0)
    beneficio_a = SimpleNamespace(
        id_producto_beneficio=87,
        id_producto=1,
        nombre_beneficio="Vida base",
        descripcion="Cobertura inicial",
        monto_cobertura=3000.0,
        incluido_base=True,
    )
    beneficio_b = SimpleNamespace(
        id_producto_beneficio=88,
        id_producto=2,
        nombre_beneficio="Renta diaria",
        descripcion="Pago diario por hospitalizacion",
        monto_cobertura=5000.0,
        incluido_base=True,
    )

    monkeypatch.setattr(
        asignaciones_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        asignaciones_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto_a, producto_b]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto_a, producto_b]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda id_producto: {
            "ok": True,
            "data": [beneficio_a] if id_producto == 1 else [beneficio_b],
        },
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )

    view = asignaciones_module.AsignacionesAseguradoView(
        page,
        lambda *_args, **_kwargs: None,
        id_asegurado=8,
    )
    control = view.build()

    producto_dd = _find_first(control, ft.Dropdown, lambda item: item.label == "Producto activo")
    prima_f = _find_first(control, ft.TextField, lambda item: item.label == "Prima mensual")

    assert producto_dd.value == "1"
    assert prima_f.value == "450.00"
    assert not any(isinstance(item, ft.Checkbox) for item in _walk_controls(control))

    producto_dd.on_change(SimpleNamespace(control=SimpleNamespace(value="2")))

    assert producto_dd.value == "2"
    assert prima_f.value == "725.00"
    assert not any(isinstance(item, ft.Checkbox) for item in _walk_controls(control))


def test_asignaciones_asegurado_separa_crear_y_vincular_poliza(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=8,
        id_agente_responsable=1,
        nombre="Rocio",
        apellido_paterno="Modo",
        apellido_materno="Poliza",
        rfc="ROMP900101AA1",
        correo="rocio@test.com",
        celular="5512345609",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto = SimpleNamespace(id_producto=1, nombre="Vida Plus", tipo_seguro="Vida", prima_base=820.0)
    poliza_disponible = SimpleNamespace(id_poliza=14, numero_poliza="POL-VINC-14")
    beneficio = SimpleNamespace(
        id_producto_beneficio=90,
        id_producto=1,
        nombre_beneficio="Muerte accidental",
        descripcion="Cobertura inicial",
        monto_cobertura=45000.0,
        incluido_base=True,
    )

    monkeypatch.setattr(
        asignaciones_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        asignaciones_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda _id: {"ok": True, "data": [poliza_disponible]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda _id_producto: {"ok": True, "data": [beneficio]},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficioController,
        "get_beneficios_by_poliza",
        lambda _id_poliza: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )

    view = asignaciones_module.AsignacionesAseguradoView(
        page,
        lambda *_args, **_kwargs: None,
        id_asegurado=8,
    )
    control = view.build()

    crear_mode_btn = _find_first(
        control,
        ft.FilledButton,
        lambda item: _button_label(item) == "Crear nueva poliza",
    )
    vincular_mode_btn = _find_first(
        control,
        ft.FilledButton,
        lambda item: _button_label(item) == "Vincular poliza existente",
    )

    assert crear_mode_btn is not None
    assert vincular_mode_btn is not None
    assert any(
        isinstance(item, ft.TextField) and item.label == "Numero de poliza"
        for item in _walk_controls(control)
    )
    assert not any(
        isinstance(item, ft.Dropdown) and item.label == "Poliza activa existente"
        for item in _walk_controls(control)
    )

    vincular_mode_btn.on_click(None)

    assert any(
        isinstance(item, ft.Dropdown) and item.label == "Poliza activa existente"
        for item in _walk_controls(control)
    )
    assert not any(
        isinstance(item, ft.Text) and item.value == "Beneficios de la poliza seleccionada"
        for item in _walk_controls(control)
    )
    assert not any(
        isinstance(item, ft.TextField) and item.label == "Numero de poliza"
        for item in _walk_controls(control)
    )


def test_asignaciones_asegurado_actualiza_beneficios_al_cambiar_poliza_vinculada(monkeypatch):
    page = DummyPage()
    asegurado = SimpleNamespace(
        id_asegurado=8,
        id_agente_responsable=1,
        nombre="Rocio",
        apellido_paterno="Cambio",
        apellido_materno="Vinculo",
        rfc="ROCV900101AA1",
        correo="rocio@test.com",
        celular="5512345609",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto = SimpleNamespace(id_producto=1, nombre="Vida Plus", tipo_seguro="Vida", prima_base=820.0)
    poliza_a = SimpleNamespace(id_poliza=14, id_producto=1, numero_poliza="POL-VINC-14")
    poliza_b = SimpleNamespace(id_poliza=15, id_producto=1, numero_poliza="POL-VINC-15")
    beneficio_catalogo = SimpleNamespace(
        id_producto_beneficio=90,
        id_producto=1,
        nombre_beneficio="Muerte accidental",
        descripcion="Cobertura inicial",
        monto_cobertura=45000.0,
        incluido_base=True,
    )
    beneficio_a = SimpleNamespace(
        id_beneficio=1,
        id_poliza=14,
        id_producto_beneficio=90,
        id_asegurado_poliza=None,
        nombre_beneficio="Beneficio poliza A",
        descripcion="Descripcion A",
        monto_cobertura=10000.0,
        vigente=True,
    )
    beneficio_b = SimpleNamespace(
        id_beneficio=2,
        id_poliza=15,
        id_producto_beneficio=90,
        id_asegurado_poliza=None,
        nombre_beneficio="Beneficio poliza B",
        descripcion="Descripcion B",
        monto_cobertura=25000.0,
        vigente=True,
    )

    monkeypatch.setattr(
        asignaciones_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        asignaciones_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda _id: {"ok": True, "data": [poliza_a, poliza_b]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda _id_producto: {"ok": True, "data": [beneficio_catalogo]},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficioController,
        "get_beneficios_by_poliza",
        lambda id_poliza: {"ok": True, "data": [beneficio_a] if id_poliza == 14 else [beneficio_b]},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )

    view = asignaciones_module.AsignacionesAseguradoView(
        page,
        lambda *_args, **_kwargs: None,
        id_asegurado=8,
    )
    control = view.build()

    vincular_mode_btn = _find_first(
        control,
        ft.FilledButton,
        lambda item: _button_label(item) == "Vincular poliza existente",
    )
    vincular_mode_btn.on_click(None)

    poliza_vinculo_dd = _find_first(control, ft.Dropdown, lambda item: item.label == "Poliza activa existente")
    texts = _find_text_values(control)

    assert poliza_vinculo_dd.value == "14"
    assert "Beneficio poliza A" not in texts
    assert "Beneficios de la poliza seleccionada" not in texts

    poliza_vinculo_dd.on_change(SimpleNamespace(control=SimpleNamespace(value="15")))
    texts = _find_text_values(control)

    assert poliza_vinculo_dd.value == "15"
    assert "Beneficio poliza B" not in texts
    assert "POL-VINC-15 · Vida Plus" not in texts


def test_asignaciones_asegurado_crea_poliza_y_navega_a_beneficios(monkeypatch):
    page = DummyPage()
    captured_payload = {}
    nav_calls = []
    asegurado = SimpleNamespace(
        id_asegurado=8,
        id_agente_responsable=1,
        nombre="Rocio",
        apellido_paterno="Crear",
        apellido_materno="Poliza",
        rfc="ROCP900102AA2",
        correo="rocio@test.com",
        celular="5512345609",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto_activo = SimpleNamespace(
        id_producto=1,
        nombre="Vida Integral",
        tipo_seguro="Vida",
        prima_base=650.0,
    )
    beneficio_base = SimpleNamespace(
        id_producto_beneficio=71,
        id_producto=1,
        nombre_beneficio="Cobertura base",
        descripcion="Proteccion principal",
        monto_cobertura=150000.0,
        incluido_base=True,
    )
    beneficio_opcional = SimpleNamespace(
        id_producto_beneficio=72,
        id_producto=1,
        nombre_beneficio="Dental opcional",
        descripcion="Cobertura dental adicional",
        monto_cobertura=12000.0,
        incluido_base=False,
    )

    monkeypatch.setattr(
        asignaciones_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        asignaciones_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "create_poliza",
        lambda payload: captured_payload.update(payload) or {"ok": True, "data": SimpleNamespace(id_poliza=50)},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda id_producto: {"ok": True, "data": [beneficio_base, beneficio_opcional] if id_producto == 1 else []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )

    view = asignaciones_module.AsignacionesAseguradoView(
        page,
        lambda route, **kwargs: nav_calls.append((route, kwargs)),
        id_asegurado=8,
    )
    control = view.build()

    numero_f = _find_first(control, ft.TextField, lambda item: item.label == "Numero de poliza")
    inicio_f = _find_first(control, ft.TextField, lambda item: item.label == "Fecha inicio (AAAA-MM-DD)")
    vencimiento_f = _find_first(control, ft.TextField, lambda item: item.label == "Fecha vencimiento (AAAA-MM-DD)")
    create_button = _find_first(
        control,
        ft.FilledButton,
        lambda item: _button_label(item) == "Crear poliza",
    )

    numero_f.value = "POL-SEL-UI-01"
    inicio_f.value = "2026-05-01"
    vencimiento_f.value = "2027-05-01"

    create_button.on_click(None)

    assert "beneficios_seleccionados" not in captured_payload
    assert captured_payload["numero_poliza"] == "POL-SEL-UI-01"
    assert nav_calls == [
        (
            "/asegurado/asignaciones",
            {"id_asegurado": 8, "focus_poliza_id": 50},
        )
    ]


def test_asignaciones_asegurado_edita_monto_beneficio_desde_modal(monkeypatch):
    page = DummyPage()
    captured_payload = {}
    nav_calls = []
    asegurado = SimpleNamespace(
        id_asegurado=8,
        id_agente_responsable=1,
        nombre="Rocio",
        apellido_paterno="Template",
        apellido_materno="Benefit",
        rfc="ROTB900101AA1",
        correo="rocio@test.com",
        celular="5512345609",
    )
    agente = SimpleNamespace(id_agente=1, nombre="Ana", apellido_paterno="Diaz")
    producto_activo = SimpleNamespace(id_producto=1, nombre="Vida Integral", tipo_seguro="Vida", prima_base=650.0)
    poliza = SimpleNamespace(
        id_poliza=21,
        id_producto=1,
        numero_poliza="POL-ASIG-01",
        estatus="activa",
        prima_mensual=900.0,
        fecha_inicio="2026-01-01",
        fecha_vencimiento="2027-01-01",
    )
    producto_beneficio = SimpleNamespace(
        id_producto_beneficio=71,
        id_producto=1,
        nombre_beneficio="Cobertura extra",
        descripcion="Descripcion desde catalogo",
        monto_cobertura=25000.0,
        incluido_base=False,
    )
    beneficio_emitido = SimpleNamespace(
        id_beneficio=501,
        id_poliza=21,
        id_producto_beneficio=71,
        id_asegurado_poliza=None,
        nombre_beneficio="Cobertura extra",
        descripcion="Descripcion desde catalogo",
        monto_cobertura=25000.0,
        costo_aplicado=120.0,
        monto_override=None,
        vigente=True,
    )

    monkeypatch.setattr(
        asignaciones_module.AseguradoController,
        "get_asegurado_by_id",
        lambda _id: {"ok": True, "data": asegurado},
    )
    monkeypatch.setattr(
        asignaciones_module.AgenteController,
        "get_agente_by_id",
        lambda _id: {"ok": True, "data": agente},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_polizas_by_asegurado",
        lambda _id: {"ok": True, "data": [poliza]},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participaciones_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_available_polizas_for_participante",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "get_participantes_by_poliza",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_all_productos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoPolizaController,
        "get_productos_activos",
        lambda: {"ok": True, "data": [producto_activo]},
    )
    monkeypatch.setattr(
        asignaciones_module.ProductoBeneficioController,
        "get_beneficios_by_producto",
        lambda id_producto: {"ok": True, "data": [producto_beneficio] if id_producto == 1 else []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficiarioController,
        "get_beneficiarios_by_asegurado",
        lambda _id: {"ok": True, "data": []},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficioController,
        "get_beneficios_by_poliza",
        lambda _id: {"ok": True, "data": [beneficio_emitido]},
    )
    monkeypatch.setattr(
        asignaciones_module.BeneficioController,
        "update_beneficio",
        lambda id_beneficio, payload: captured_payload.update({"id_beneficio": id_beneficio, **payload}) or {"ok": True, "data": payload},
    )
    monkeypatch.setattr(
        asignaciones_module.PolizaController,
        "update_poliza",
        lambda _id_poliza, _payload: {"ok": True, "data": poliza},
    )

    view = asignaciones_module.AsignacionesAseguradoView(
        page,
        lambda route, **kwargs: nav_calls.append((route, kwargs)),
        id_asegurado=8,
        focus_poliza_id=21,
    )
    control = view.build()
    text_values = _find_text_values(control)
    assert "Aplica a" not in text_values
    assert "Origen" not in text_values
    assert any("Costo beneficios: $120.00" in text for text in text_values)
    assert any("Prima final: $770.00" in text for text in text_values)
    back_icon = _find_first(
        control,
        ft.Icon,
        lambda item: getattr(item, "icon", None) == ft.Icons.ARROW_BACK_ROUNDED,
    )
    assert (back_icon.size or 0) >= 18

    all_buttons = [item for item in _walk_controls(control) if isinstance(item, (ft.OutlinedButton, ft.FilledButton, ft.TextButton))]
    assert not any(_button_label(item) == "Agregar beneficio" for item in all_buttons)

    edit_button = _find_first(
        control,
        ft.TextButton,
        lambda item: _button_label(item) == "Editar monto",
    )
    edit_button.on_click(None)

    dialog = page.dialogs[-1]
    dialog_text_values = _find_text_values(dialog)
    assert "Aplica a" not in dialog_text_values
    override_f = _find_first(dialog, ft.TextField, lambda item: item.label == "Override de monto (opcional)")
    save_button = _find_first(
        dialog,
        ft.FilledButton,
        lambda item: _button_label(item) == "Guardar",
    )

    override_f.value = "33333"
    save_button.on_click(None)

    assert captured_payload["id_asegurado_poliza"] is None
    assert captured_payload["monto_override"] == 33333.0
    assert captured_payload["vigente"] is True
    assert captured_payload["id_beneficio"] == 501
    assert nav_calls == [
        (
            "/asegurado/asignaciones",
            {"id_asegurado": 8, "focus_poliza_id": 21, "focus_tab": "beneficios"},
        )
    ]