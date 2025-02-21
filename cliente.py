import requests

def obtener_usuarios():
    """Realiza una petición GET al servidor y muestra los usuarios"""
    response = requests.get('http://localhost:5000/usuarios')
    
    if response.status_code == 200:
        usuarios = response.json()
        print("\nUsuarios encontrados:")
        for usuario in usuarios:
            print(f"ID: {usuario['id']}, Nombre: {usuario['nombre']}")
    else:
        print("No se encontraron usuarios.")

def agregar_usuario():
    """Solicita un nombre y lo envía al servidor mediante una petición POST"""
    nombre = input("\nIngrese el nombre del nuevo usuario: ").strip()
    if nombre:
        nuevo_usuario = {"nombre": nombre}
        response = requests.post('http://localhost:5000/usuarios', json=nuevo_usuario)
        
        if response.status_code == 201:
            print("✅ Usuario agregado con éxito.")
        else:
            print("❌ Error al agregar usuario:", response.json().get("error", "Error desconocido"))
    else:
        print("⚠️ El nombre no puede estar vacío.")

if __name__ == "__main__":
    while True:
        print("\n--- Menú ---")
        print("1. Ver usuarios")
        print("2. Agregar usuario")
        print("3. Salir")
        
        opcion = input("Seleccione una opción: ").strip()
        
        if opcion == "1":
            obtener_usuarios()
        elif opcion == "2":
            agregar_usuario()
        elif opcion == "3":
            print("Saliendo del programa...")
            break
        else:
            print("❌ Opción no válida. Intente de nuevo.")
