from datetime import datetime

class Transaction:
    def __init__(self, monto: float, tarjeta_cliente: str, restaurante_id: str, fecha_hora: str = None):
        if monto <= 0:
            raise ValueError("El monto consumido debe ser mayor a cero.")
        if not tarjeta_cliente or not isinstance(tarjeta_cliente, str):
            raise ValueError("El número de tarjeta del cliente es inválido.")
        if not restaurante_id or not isinstance(restaurante_id, str):
            raise ValueError("El código del restaurante es inválido.")
        
        self.monto = float(monto)
        self.tarjeta_cliente = tarjeta_cliente.strip()
        self.restaurante_id = restaurante_id.strip()
        self.fecha_hora = fecha_hora.strip() if fecha_hora else datetime.now().isoformat()

    def to_dict(self) -> dict:
        return {
            "monto": self.monto,
            "tarjeta_cliente": self.tarjeta_cliente,
            "restaurante_id": self.restaurante_id,
            "fecha_hora": self.fecha_hora
        }


class RewardAccount:
    def __init__(self, tarjeta_cliente: str, puntos_acumulados: float = 0.0):
        if not tarjeta_cliente or not isinstance(tarjeta_cliente, str):
            raise ValueError("El número de tarjeta del cliente es inválido.")
        
        self.tarjeta_cliente = tarjeta_cliente.strip()
        self.puntos_acumulados = float(puntos_acumulados)

    def acumular_puntos(self, monto: float) -> float:
        if monto <= 0:
            raise ValueError("El monto para acumular puntos debe ser mayor a cero.")
        
        # Lógica de negocio: 10% del consumo se acumula en puntos
        nuevos_puntos = round(monto * 0.10, 2)
        self.puntos_acumulados = round(self.puntos_acumulados + nuevos_puntos, 2)
        return nuevos_puntos
