import pika
import json

RABBITMQ_HOST = 'amqps://odedhptn:e7o5mMHHzurIT8f2v_17Umn2tXOMXadN@jackal.rmq.cloudamqp.com/odedhptn'
NOTIFICATION_QUEUE = 'notification_queue'


def send_fake_email(notification):
    print(f"Enviando notificação para {notification['customer']}")
    print(f"Conteúdo: Seu pedido foi {notification['status']}!")


def callback(ch, method, properties, body):
    notification = json.loads(body)
    send_fake_email(notification)
    ch.basic_ack(delivery_tag=method.delivery_tag)


def start_consumer():
    params = pika.URLParameters(RABBITMQ_HOST)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()

    channel.queue_declare(queue=NOTIFICATION_QUEUE, durable=True)
    channel.basic_consume(
        queue=NOTIFICATION_QUEUE,
        on_message_callback=callback
    )

    print('Aguardando notificações...')
    channel.start_consuming()


if __name__ == '__main__':
    start_consumer()
