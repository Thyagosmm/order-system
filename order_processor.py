import pika
import json
import time

RABBITMQ_HOST = 'amqps://odedhptn:e7o5mMHHzurIT8f2v_17Umn2tXOMXadN@jackal.rmq.cloudamqp.com/odedhptn'
QUEUE_NAME = 'order_queue'
NOTIFICATION_QUEUE = 'notification_queue'


def process_order(order):
    # Simulação de processamento
    print(f"Processando pedido para: {order['customer']}")
    time.sleep(2)  # Simula trabalho demorado

    # Validação básica
    if not all(key in order for key in ['customer', 'items', 'total']):
        raise ValueError("Pedido inválido")

    # Simula geração de NF e atualização de estoque
    print(
        f"Nota fiscal gerada para {order['customer']} | Total: {order['total']}")

    # Envia notificação (opcional)
    send_notification(order)


def send_notification(order):
    params = pika.URLParameters(RABBITMQ_HOST)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=NOTIFICATION_QUEUE, durable=True)

    channel.basic_publish(
        exchange='',
        routing_key=NOTIFICATION_QUEUE,
        body=json.dumps(
            {'customer': order['customer'], 'status': 'processed'}),
        properties=pika.BasicProperties(
            delivery_mode=2  # Correção aqui: parêntese faltando
        )  # Fecha corretamente o BasicProperties
    )  # Fecha corretamente o basic_publish
    connection.close()


def callback(ch, method, properties, body):
    try:
        order = json.loads(body)
        process_order(order)
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Erro no processamento: {str(e)}")
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=False)


def start_consumer():
    params = pika.URLParameters(RABBITMQ_HOST)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    channel.basic_qos(prefetch_count=1)

    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    print('Aguardando pedidos...')
    channel.start_consuming()


if __name__ == '__main__':
    start_consumer()
