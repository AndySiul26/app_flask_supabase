from flask import Flask, request, jsonify
from supabase import create_client, Client
from config import Config
from datetime import datetime

app = Flask(__name__)

# Configuración de Supabase
supabase: Client = create_client(Config.SUPABASE_URL, Config.SUPABASE_KEY)

@app.route('/ventas', methods=['POST'])
def create_venta():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    
    try:
        # Verificar si el cliente existe
        cliente = supabase.table('clientes').select('*').eq('id_cliente', data['id_cliente']).execute()

        # Si el cliente no existe, devolver un error
        if not cliente.data:
            return jsonify({'error': 'Cliente no encontrado'}), 400

        nombre_cliente = cliente.data[0]['nombre_cliente']

        # Verificar si el comprobante existe
        comprobante = supabase.table('comprobantes').select('*').eq('id_comprobante', data['id_comprobante']).execute()
        
        # Si el comprobante no existe, insertarlo
        if not comprobante.data:
            now = datetime.now()
            supabase.table('comprobantes').insert({
                'id_comprobante': data['id_comprobante'],
                'id_cliente': data['id_cliente'],
                'nombre_cliente': nombre_cliente,
                'fecha': now.date().isoformat(),
                'hora': now.time().isoformat()
            }).execute()

        # Insertar la venta
        venta = supabase.table('ventas').insert({
            'precio_id': data['precio_id'],
            'id_cliente': data['id_cliente'],
            'cantidad': data['cantidad'],
            'nombre_cliente': nombre_cliente,
            'vendedor': data['vendedor'],
            'periodo_inicial': data['periodo_inicial'],
            'periodo_final': data['periodo_final'],
            'medio_pago': data['medio_pago'],
            'id_comprobante': data['id_comprobante'],
            'created_at': datetime.now().isoformat()
        }).execute()

        # Actualizar el contador de compras del cliente
        supabase.table('clientes').update({'compras': cliente.data[0]['compras'] + 1}).eq('id_cliente', data['id_cliente']).execute()

        return jsonify({'venta_id': venta.data[0]['id']}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/clientes', methods=['POST'])
def create_cliente():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    
    try:
        data['fecha_registro'] = datetime.now().date().isoformat()
        data['compras'] = 0
        print(data)
        cliente = supabase.table('clientes').insert(data).execute()
        return jsonify({'id_cliente': cliente.data[0]['id_cliente']}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500
    
@app.route('/comprobantes', methods=['POST'])
def create_comprobante():
    data = request.json
    if not data:
        return jsonify({'error': 'Invalid input'}), 400
    
    try:
        now = datetime.now()
        data['fecha'] = now.date().isoformat()
        data['hora'] = now.time().isoformat()
        comprobante = supabase.table('comprobantes').insert(data).execute()
        return jsonify({'id_comprobante': comprobante.data[0]['id_comprobante']}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)