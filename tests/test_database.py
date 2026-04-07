
from controllers.agente_controller import AgenteController

def test_crear_agente():
    print("\n--- TEST: Crear agente ---")
    resultado = AgenteController.create_agente({
    "clave_agente": "AG001",
    "nombre": "Juan",
    "apellido_paterno": "Pérez",
    "apellido_materno": "López",
    "correo": "juan@mail.com",
    "rol": "ADMIN",
    "password": "1234"
})
    print(resultado)
    assert resultado["ok"] == True, "Falló al crear agente"
    print("Agente creado:", resultado["data"])
    return resultado["data"].id_agente  # retorna el id para los demás tests

def test_get_agente(id_agente: int):
    print("\n--- TEST: Obtener agente por ID ---")
    resultado = AgenteController.get_agente_by_id(id_agente)
    print(resultado)
    assert resultado["ok"] == True, "Falló al obtener agente"
    print("Agente encontrado:", resultado["data"])

def test_get_all_agentes():
    print("\n--- TEST: Obtener todos los agentes ---")
    resultado = AgenteController.get_all_agentes()
    print(resultado)
    assert resultado["ok"] == True, "❌ Falló al obtener agentes"
    print(f"✅ Total agentes: {len(resultado['data'])}")

def test_update_agente(id_agente: int):
    print("\n--- TEST: Actualizar agente ---")
    resultado = AgenteController.update_agente(id_agente, {
        "nombre": "Juan Actualizado"
    })
    print(resultado)
    assert resultado["ok"] == True, "❌ Falló al actualizar agente"
    print("✅ Agente actualizado:", resultado["data"])

def test_delete_agente(id_agente: int):
    print("\n--- TEST: Eliminar agente ---")
    resultado = AgenteController.delete_agente(id_agente)
    print(resultado)
    assert resultado["ok"] == True, "❌ Falló al eliminar agente"
    print("✅", resultado["mensaje"])

def test_agente_no_existe():
    print("\n--- TEST: Agente que no existe ---")
    resultado = AgenteController.get_agente_by_id(9999)
    assert resultado["ok"] == False, "❌ Debería haber fallado"
    print("✅ Manejo correcto de error:", resultado["error"])


if __name__ == "__main__":
    print("======= INICIANDO TESTS =======")
    id_agente = test_crear_agente()
    test_get_agente(id_agente)
    test_get_all_agentes()
    test_update_agente(id_agente)
    test_agente_no_existe()
    test_delete_agente(id_agente)    
    print("\n======= TESTS COMPLETADOS =======")