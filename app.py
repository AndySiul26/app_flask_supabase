from flask import Flask, request, jsonify
from supabase import create_client, Client
from config import Config
from datetime import datetime

app = Flask(__name__)

# Configuración de Supabase
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

@app.route('/insert_servicio', methods=['POST'])
def insert_servicio():
    try:
        data = request.json
        response = supabase.table("servicios").insert(data).execute()
        if response.data:
            return jsonify(response.data[0]), 201
        else:
            return jsonify({"error": response.error}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insert_cliente', methods=['POST'])
def insert_cliente():
    try:
        data = request.json
        response = supabase.table("clientes").insert(data).execute()
        if response.data:
            return jsonify(response.data[0]), 201
        else:
            return jsonify({"error": response.error_message}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insert_contacto_cliente', methods=['POST'])
def insert_contacto_cliente():
    try:
        data = request.json
        response = supabase.table("contactos_clientes").insert(data).execute()
        if response.data:
            return jsonify(response.data[0]), 201
        else:
            return jsonify({"error": response.error_message}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insert_negocio', methods=['POST'])
def insert_negocio():
    try:
        data = request.json
        response = supabase.table("negocios").insert(data).execute()
        if response.data:
            return jsonify(response.data[0]), 201
        else:
            return jsonify({"error": response.error_message}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insert_sitio_web_negocio', methods=['POST'])
def insert_sitio_web_negocio():
    try:
        data = request.json
        response = supabase.table("sitios_web_negocios").insert(data).execute()
        if response.data:
            return jsonify(response.data[0]), 201
        else:
            return jsonify({"error": response.error_message}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insert_venta', methods=['POST'])
def insert_venta():
    try:
        data = request.json
        
        # Obtener los detalles del servicio
        servicio = supabase.table("servicios").select("*").eq("id", data['id_servicio']).execute()
        if not servicio.data:
            return jsonify({"error": "Servicio no encontrado"}), 404
        
        servicio = servicio.data[0]
        
        # Calcular el precio total del servicio
        precio_total_servicio = (servicio['precio_normal'] - servicio['descuento']) * data['cantidad']
        
        # Añadir el precio_total_servicio a los datos
        data['precio_total_servicio'] = precio_total_servicio
        
        response = supabase.table("ventas").insert(data).execute()
        if response.data:
            return jsonify(response.data[0]), 201
        else:
            return jsonify({"error": response.error}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insert_comprobante', methods=['POST'])
def insert_comprobante():
    try:
        data = request.json
        # Comprobar que sea un texto concatenado por comas ids_ventas o directamente un entero
        ids_ventas_list = [0]
        
        if (type(data.get("ids_ventas")) != str and type(data.get("ids_ventas")) == int):
            ids_ventas_list[0] = data.get("ids_ventas")
        else:
            ids_ventas_list = data.get("ids_ventas").split(",") # Convertir la cadena en una lista de enteros
        
        del data["ids_ventas"]  # Eliminar la propiedad "ids_ventas" del diccionario "data"
        
        response = supabase.table("comprobantes").insert(data).execute()
        
        if response.data:
            comprobante_id = response.data[0]["id"]
            
            # Insertar en ventas_comprobantes
            
            for id_venta in ids_ventas_list:
                insert_data = {
                    "id_comprobante": comprobante_id,
                    "id_venta": int(id_venta)
                }
                supabase.table("ventas_comprobantes").insert(insert_data).execute()

            # Actualizar las ventas con el ID del comprobante
            supabase.table("ventas").update({"id_comprobante": comprobante_id}).in_("id", ids_ventas_list).execute()
            return jsonify({"id": comprobante_id}), 201
        else:
            return jsonify({"error": response.error_message}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)