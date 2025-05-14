# order-system# Sistema de Processamento de Pedidos

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

**Instalação:**
```bash
git clone https://github.com/seu-usuario/order-system.git
cd order-system
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt