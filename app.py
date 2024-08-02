from flask import Flask, request, jsonify
from supabase import create_client, Client
from config import Config
from datetime import datetime

app = Flask(__name__)

# Configuración de Supabase
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)
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
        response = supabase.table("ventas").insert(data).execute()
        if response.data == 201:
            return jsonify(response.data[0]), 201
        else:
            return jsonify({"error": response.error_message}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/insert_comprobante', methods=['POST'])
def insert_comprobante():
    try:
        data = request.json
        response = supabase.table("comprobantes").insert(data).execute()
        if response.data:
            comprobante_id = response.data[0]["id"]

            # Insertar en ventas_comprobantes
            ids_ventas_list = data.get("ids_ventas").split(",")
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