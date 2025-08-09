from flask import Flask, request, jsonify
import mysql.connector

app = Flask(__name__)

# Configuración de la base de datos
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Guate2024!',
    'database': 'datos_ambientales'
}

@app.route('/api/datos', methods=['POST'])
def recibir_datos():
    if request.is_json:
        datos = request.get_json()
        temperatura = datos.get("temperatura")
        humedad = datos.get("humedad")

        try:
            # Conectar a la base de datos
            conn = mysql.connector.connect(**db_config)
            cursor = conn.cursor()

            # Insertar los datos
            sql = "INSERT INTO lecturas (temperatura, humedad) VALUES (%s, %s)"
            val = (temperatura, humedad)
            cursor.execute(sql, val)

            # Guardar los cambios
            conn.commit()

            print(f"Datos guardados: Temp={temperatura}°C, Humedad={humedad}%")
            return jsonify({"mensaje": "Datos recibidos y guardados"}), 200

        except mysql.connector.Error as err:
            print(f"Error al guardar en la base de datos: {err}")
            return jsonify({"mensaje": f"Error en la base de datos: {err}"}), 500

        finally:
            if 'conn' in locals() and conn.is_connected():
                cursor.close()
                conn.close()

    else:
        return jsonify({"mensaje": "La peticion no es un JSON valido"}), 400

if __name__ == '__main__':
    app.run(host='::', port=5000, debug=True, ssl_context='adhoc')