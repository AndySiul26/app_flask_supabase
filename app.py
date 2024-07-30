from flask import Flask, request, jsonify
from supabase import create_client, Client
from config import Config
from datetime import datetime

app = Flask(__name__)

# Configuración de Supabase
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

@app.route('/clientes', methods=['POST'])
def add_cliente():
    data = request.json
    try:
        response = supabase.table('clientes').insert(data).execute()
        print(response)  # Añadir impresión de depuración
        if response.data:
            return jsonify(response.data), 201
        else:
            return jsonify({"error": "No data returned"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ventas', methods=['POST'])
def add_venta():
    data = request.json
    try:
        # Obtener ID del comprobante
        comprobante_response = supabase.table('comprobantes').select('id_comprobante').order('id_comprobante', desc=True).limit(1).execute()
        id_comprobante = comprobante_response.data[0]['id_comprobante'] + 1 if comprobante_response.data else 1

        # Insertar nuevo comprobante
        supabase.table('comprobantes').insert({
            'id_comprobante': id_comprobante,
            'id_cliente': data['id_cliente'],
            'nombre_cliente': data['nombre_cliente'],
            'fecha': data['fecha'],
            'hora': data['hora']
        }).execute()

        # Insertar venta
        data['id_comprobante'] = id_comprobante
        response = supabase.table('ventas').insert(data).execute()
        return jsonify(response.data), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/ventas', methods=['GET'])
def get_ventas():
    try:
        response = supabase.table('ventas').select('*').execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/clientes/<id_cliente>', methods=['PUT'])
def update_cliente(id_cliente):
    data = request.json
    try:
        response = supabase.table('clientes').update(data).eq('id_cliente', id_cliente).execute()
        return jsonify(response.data), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)