import sys
from infrastructure.adapters.rabbitmq_adapter import RabbitMQPublisher
from application.use_cases import PublishTransactionUseCase

def parse_arguments(monto, tarjeta, restaurante):
    try:
        monto = float(sys.argv[1])
        if len(sys.argv) > 2:
            tarjeta = sys.argv[2]
        if len(sys.argv) > 3:
            restaurante = sys.argv[3]
    except ValueError:
        print(" [!] Argumentos inválidos. Usando valores por defecto.")
    return monto, tarjeta, restaurante


def prompt_user_inputs(monto, tarjeta, restaurante):
    print("Presiona ENTER para usar los valores por defecto o introduce nuevos:")
    try:
        monto_in = input(f"Monto consumido [{monto}]: ").strip()
        if monto_in:
            monto = float(monto_in)
        
        tarjeta_in = input(f"Tarjeta del cliente [{tarjeta}]: ").strip()
        if tarjeta_in:
            tarjeta = tarjeta_in
            
        restaurante_in = input(f"Código del restaurante [{restaurante}]: ").strip()
        if restaurante_in:
            restaurante = restaurante_in
    except (KeyboardInterrupt, EOFError):
        print("\n [!] Cancelado por el usuario.")
        return None
    return monto, tarjeta, restaurante


def main():
    print("=== PRODUCTOR - SISTEMA DE RESTAURANTE ===")
    
    monto = 150.0
    tarjeta = "1234-5678-9012-3456"
    restaurante = "REST-UTEC-001"
    
    # Permitir argumentos por línea de comandos para facilitar las pruebas automatizadas
    if len(sys.argv) > 1:
        monto, tarjeta, restaurante = parse_arguments(monto, tarjeta, restaurante)
    else:
        inputs = prompt_user_inputs(monto, tarjeta, restaurante)
        if inputs is None:
            return
        monto, tarjeta, restaurante = inputs

    # Inicializar el adaptador y el caso de uso
    publisher = RabbitMQPublisher()
    use_case = PublishTransactionUseCase(publisher)
    
    try:
        tx_data = use_case.execute(monto, tarjeta, restaurante)
        print(f" [x] Mensaje enviado a RabbitMQ: {tx_data}")
    except Exception as e:
        print(f" [!] Error en el productor: {e}")
    finally:
        publisher.close()

if __name__ == "__main__":
    main()
