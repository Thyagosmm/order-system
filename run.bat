@echo off
REM Script completo com venv e dependências

REM 1. Cria ambiente virtual se não existir
if not exist "venv\" (
    python -m venv venv
    call venv\Scripts\activate
    pip install --upgrade pip
    pip install -r requirements.txt
)

REM 2. Inicia serviços em janelas separadas
start "Serviço Pedidos" cmd /k "call venv\Scripts\activate && python order_service.py"
timeout /t 5 /nobreak >nul

start "Processamento" cmd /k "call venv\Scripts\activate && python order_processor.py"
timeout /t 2 /nobreak >nul

start "Notificações" cmd /k "call venv\Scripts\activate && python notification_consumer.py"

echo [✓] Sistema iniciado!
echo Teste com:
echo Invoke-WebRequest -Uri http://localhost:5000/order `
echo -Method POST `
echo -Headers @{ "Content-Type" = "application/json" } `
echo -Body '{"customer": "Compra de Thyago", "items": ["Camisa da Boss"], "total": 50.00}'