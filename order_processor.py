import pika
import json
import time

RABBITMQ_HOST = 'amqps://odedhptn:e7o5mMHHzurIT8f2v_17Umn2tXOMXadN@jackal.rmq.cloudamqp.com/odedhptn'
QUEUE_NAME = 'order_queue'  # Fila principal de pedidos
NOTIFICATION_QUEUE = 'notification_queue'  # Fila de notificações


def process_order(order):
    """Processa um pedido recebido"""
    print(f"Processando pedido para: {order['customer']}")
    time.sleep(2)  # Simula processamento demorado

    # Valida campos obrigatórios
    if not all(key in order for key in ['customer', 'items', 'total']):
        raise ValueError("Pedido inválido")

    # Simula ações de negócio
    print(
        f"Nota fiscal gerada para {order['customer']} | Total: {order['total']}")
    send_notification(order)  # Dispara notificação


def send_notification(order):
    """Publica notificação na fila"""
    params = pika.URLParameters(RABBITMQ_HOST)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Garante a fila de notificações
    channel.queue_declare(queue=NOTIFICATION_QUEUE, durable=True)

    # Publica mensagem persistente
    channel.basic_publish(
        exchange='',
        routing_key=NOTIFICATION_QUEUE,
        body=json.dumps(
            {'customer': order['customer'], 'status': 'processed'}),
        properties=pika.BasicProperties(
            delivery_mode=2  # Mensagem persistente
        )
    )
    connection.close()


def callback(ch, method, properties, body):
    """Callback para mensagens recebidas"""
    try:
        order = json.loads(body)
        process_order(order)
        ch.basic_ack(delivery_tag=method.delivery_tag)  # ACK explícito
    except Exception as e:
        print(f"Erro no processamento: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag,
                      requeue=False)  # Rejeita mensagem


def start_consumer():
    """Configura e inicia o consumidor principal"""
    params = pika.URLParameters(RABBITMQ_HOST)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    # Configurações de qualidade de serviço
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)  # Processa 1 mensagem por vez

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    print('Aguardando pedidos...')
    channel.start_consuming()


if __name__ == '__main__':
    start_consumer()
