from flask import Flask, request, jsonify
import pika
import json

app = Flask(__name__)

# Configurações do RabbitMQ
RABBITMQ_HOST = 'amqps://odedhptn:e7o5mMHHzurIT8f2v_17Umn2tXOMXadN@jackal.rmq.cloudamqp.com/odedhptn'
QUEUE_NAME = 'order_queue'  # Fila principal


def send_to_queue(order_data):
    """Publica o pedido na fila de processamento"""
    params = pika.URLParameters(RABBITMQ_HOST)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Cria fila durável se não existir
    channel.queue_declare(queue=QUEUE_NAME, durable=True)

    # Publica mensagem persistente
    channel.basic_publish(
        exchange='',
        routing_key=QUEUE_NAME,
        body=json.dumps(order_data),
        properties=pika.BasicProperties(
            delivery_mode=2  # Garante persistência
        )
    )
    connection.close()


@app.route('/order', methods=['POST'])
def create_order():
    """Endpoint para recebimento de pedidos"""
    data = request.json

    # Validação básica
    required_fields = ['customer', 'items', 'total']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Dados incompletos'}), 400

    try:
        send_to_queue(data)
        return jsonify({'message': 'Pedido recebido e enviado para processamento'}), 202
    except Exception as e:
        return jsonify({'error': str(e)}), 500  # Erro interno


if __name__ == '__main__':
    app.run(port=5000, debug=True)  # Executa o servidor Flask
