# Sistema de Processamento de Pedidos

Sistema distribuído para e-commerce com comunicação assíncrona via RabbitMQ/CloudAMQP

## 📦 Componentes
- **order_service.py**: API REST para receber pedidos
- **order_processor.py**: Processamento assíncrono de pedidos
- **notification_consumer.py**: Serviço de notificação (opcional)

## 🚀 Execução
**Pré-requisitos:**
- Python 3.9+
- RabbitMQ local ou conta CloudAMQP
- Portas 5000 (API) e 5672 (AMQP) liberadas

**Instalação e Funcionamento:**
```powershell

git clone https://github.com/seu-usuario/order-system.git
cd order-system

inicie o script:
.\run.bat

depois envie pedidos através do metodo post http no próprio terminal powershell nesse formato:

Invoke-WebRequest -Uri http://localhost:5000/order `
-Method POST `
-Headers @{ "Content-Type" = "application/json" } `
-Body '{"customer": "NOME_CLIENTE", "items": ["PRODUTO"], "total": 999.99}'

OBS: No terminal de processamento de pedido (order_processor) será impresso qual o pedido está sendo processado e após processar vai imprimir a notificação do pedido no terminal de notificações (notication_consumer).

Você pode visualizar os pedidos e as filas através da interface de gerenciamento do rabiit na url gerada do cloudamqp:

https://jackal.rmq.cloudamqp.com

username: odedhptn
password: e7o5mMHHzurIT8f2v_17Umn2tXOMXadN