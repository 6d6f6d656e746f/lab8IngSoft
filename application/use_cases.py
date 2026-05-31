import json
from domain.entities import Transaction, RewardAccount
from application.ports.message_broker import MessagePublisher
from application.ports.repository import RewardRepository

class PublishTransactionUseCase:
    def __init__(self, publisher: MessagePublisher):
        self.publisher = publisher

    def execute(self, monto: float, tarjeta_cliente: str, restaurante_id: str) -> dict:
        # Crea la entidad de dominio (realiza validaciones de negocio)
        transaction = Transaction(monto, tarjeta_cliente, restaurante_id)
        data = transaction.to_dict()
        
        # Publica la transacción a través de la interfaz abstracta (puerto)
        self.publisher.publish("laboratorio_1", data)
        return data


class ProcessTransactionUseCase:
    def __init__(self, repository: RewardRepository, notification_publisher: MessagePublisher = None):
        self.repository = repository
        self.notification_publisher = notification_publisher

    def execute(self, transaction_data: dict) -> dict:
        # Reconstruir transacción y validar
        monto = transaction_data.get("monto")
        tarjeta_cliente = transaction_data.get("tarjeta_cliente")
        restaurante_id = transaction_data.get("restaurante_id")
        fecha_hora = transaction_data.get("fecha_hora")
        
        transaction = Transaction(monto, tarjeta_cliente, restaurante_id, fecha_hora)
        
        # Buscar cuenta de recompensas existente o crear una nueva
        account = self.repository.find_by_card(transaction.tarjeta_cliente)
        if not account:
            account = RewardAccount(transaction.tarjeta_cliente)
            
        # Ejecutar lógica de negocio para acumular puntos
        puntos_ganados = account.acumular_puntos(transaction.monto)
        
        # Guardar en repositorio
        self.repository.save(account)
        
        result = {
            "tarjeta_cliente": account.tarjeta_cliente,
            "puntos_ganados": puntos_ganados,
            "puntos_acumulados": account.puntos_acumulados,
            "status": "PROCESSED"
        }
        
        # Publicar opcionalmente una notificación (si está configurada)
        if self.notification_publisher:
            notification_event = {
                "tarjeta_cliente": account.tarjeta_cliente,
                "mensaje": f"Se acumularon {puntos_ganados} puntos. Saldo actual: {account.puntos_acumulados}",
                "timestamp": transaction.fecha_hora
            }
            try:
                self.notification_publisher.publish("notificaciones_recompensa", notification_event)
            except Exception as e:
                # Loggear el error pero no detener el flujo principal de recompensas
                print(f" [!] No se pudo enviar la notificación: {e}")
                
        return result
