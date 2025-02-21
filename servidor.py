from flask import Flask, jsonify, request, render_template, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'secreto123'  # Clave para manejar sesiones en Flask

# Usuario y clave válidos
CREDENCIALES = {"usuario": "diegos", "clave": "admin123"}

# Base de datos simulada
base_datos = {
    "usuarios": [
        {"id": 1, "nombre": "jose"},
        {"id": 2, "nombre": "maria"}
    ]
}

# Ruta de login
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        clave = request.form['clave']

        if usuario == CREDENCIALES["usuario"] and clave == CREDENCIALES["clave"]:
            session['usuario'] = usuario  # Guardar sesión
            return redirect(url_for('menu'))
        else:
            return render_template('login.html', error="❌ Usuario o clave incorrectos")

    return render_template('login.html')

# Ruta del menú principal (protegido)
@app.route('/menu')
def menu():
    if 'usuario' not in session:  # Si no hay sesión, redirigir al login
        return redirect(url_for('login'))
    return render_template('index.html')

# Ruta para cerrar sesión
@app.route('/logout')
def logout():
    session.pop('usuario', None)  # Eliminar sesión
    return redirect(url_for('login'))

# Rutas para manejar usuarios (ya existentes)
@app.route('/usuarios', methods=['GET'])
def obtener_usuarios():
    return jsonify(base_datos['usuarios'])

@app.route('/usuarios', methods=['POST'])
def agregar_usuario():
    nuevo_usuario = request.json
    if "nombre" in nuevo_usuario:
        nuevo_id = len(base_datos["usuarios"]) + 1
        nuevo_usuario["id"] = nuevo_id
        base_datos["usuarios"].append(nuevo_usuario)
        return jsonify({"mensaje": "Usuario agregado exitosamente", "usuario": nuevo_usuario}), 201
    else:
        return jsonify({"error": "El campo 'nombre' es requerido"}), 400

@app.route('/usuarios/<int:usuario_id>', methods=['DELETE'])
def eliminar_usuario(usuario_id):
    global base_datos
    usuarios_filtrados = [u for u in base_datos["usuarios"] if u["id"] != usuario_id]

    if len(usuarios_filtrados) == len(base_datos["usuarios"]):
        return jsonify({"error": "Usuario no encontrado"}), 404

    base_datos["usuarios"] = usuarios_filtrados
    return jsonify({"mensaje": f"Usuario con ID {usuario_id} eliminado exitosamente"}), 200

if __name__ == '__main__':
    app.run(port=5000, debug=True)

