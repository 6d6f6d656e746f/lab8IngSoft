from abc import ABC, abstractmethod

class MessagePublisher(ABC):
    @abstractmethod
    def publish(self, topic: str, message: dict) -> None:
        """
        Publica un mensaje (diccionario serializable a JSON) en un tema/cola específico.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Cierra la conexión del publicador limpiamente.
        """
        pass


class MessageConsumer(ABC):
    @abstractmethod
    def consume(self, topic: str, callback_fn) -> None:
        """
        Inicia la escucha de mensajes en un tema/cola específico.
        El callback_fn debe recibir (ch, method, properties, body) o similar deserializado.
        """
        pass

    @abstractmethod
    def close(self) -> None:
        """
        Cierra la conexión del consumidor limpiamente.
        """
        pass
