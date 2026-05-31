import sys
import os
from infrastructure.adapters.rabbitmq_adapter import RabbitMQConsumer
from infrastructure.adapters.memory_repository import InMemoryRewardRepository
from application.use_cases import ProcessTransactionUseCase

def main():
    print("=== CONSUMIDOR - SISTEMA DE RECOMPENSAS ===")
    
    # Inicializar adaptadores y caso de uso
    repository = InMemoryRewardRepository()
    use_case = ProcessTransactionUseCase(repository)
    consumer = RabbitMQConsumer()
    
    # Cola de la que se consumirá
    nombre_cola = "laboratorio_1"
    
    def procesar_evento(data):
        print(f"\n [>] Evento recibido de la cola: {data}")
        try:
            # Ejecutar el caso de uso
            resultado = use_case.execute(data)
            print(f" [✓] Recompensa Procesada:")
            print(f"     - Tarjeta Cliente: {resultado['tarjeta_cliente']}")
            print(f"     - Puntos Ganados: {resultado['puntos_ganados']}")
            print(f"     - Total Acumulado: {resultado['puntos_acumulados']}")
        except Exception as e:
            print(f" [!] Error al procesar la recompensa: {e}")

    try:
        consumer.consume(nombre_cola, procesar_evento)
    except KeyboardInterrupt:
        print("\n [*] Deteniendo el consumidor de recompensas...")
    except Exception as e:
        print(f" [!] Error en la ejecución del consumidor: {e}")
    finally:
        try:
            consumer.close()
        except Exception:
            pass

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n [*] Saliendo...")
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
