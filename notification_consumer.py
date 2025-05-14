import pika
import json

# Configuração de conexão com RabbitMQ/CloudAMQP usando URL AMQPS
RABBITMQ_HOST = 'amqps://odedhptn:e7o5mMHHzurIT8f2v_17Umn2tXOMXadN@jackal.rmq.cloudamqp.com/odedhptn'
NOTIFICATION_QUEUE = 'notification_queue'  # Nome da fila para notificações


def send_fake_email(notification):
    """Simula o envio de e-mail através de logs"""
    print(f"Enviando notificação para {notification['customer']}")
    print(f"Conteúdo: Seu pedido foi {notification['status']}!")


def callback(ch, method, properties, body):
    """Função chamada quando uma mensagem é recebida"""
    notification = json.loads(body)  # Desserializa o JSON
    send_fake_email(notification)
    ch.basic_ack(delivery_tag=method.delivery_tag)  # Confirma o processamento


def start_consumer():
    """Inicia o consumidor de notificações"""
    params = pika.URLParameters(RABBITMQ_HOST)  # Parâmetros de conexão
    connection = pika.BlockingConnection(params)  # Conexão persistente
    channel = connection.channel()

    # Garante que a fila existe e é durável
    channel.queue_declare(queue=NOTIFICATION_QUEUE, durable=True)

    # Configura o consumidor
    channel.basic_consume(
        queue=NOTIFICATION_QUEUE,
        on_message_callback=callback  # Registra o callback
    )

    print('Aguardando notificações...')
    channel.start_consuming()  # Inicia o loop infinito de consumo


if __name__ == '__main__':
    start_consumer()
