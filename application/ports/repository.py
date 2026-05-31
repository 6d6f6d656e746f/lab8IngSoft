from abc import ABC, abstractmethod
from domain.entities import RewardAccount

class RewardRepository(ABC):
    @abstractmethod
    def save(self, account: RewardAccount) -> None:
        """
        Guarda o actualiza una cuenta de recompensas.
        """
        pass

    @abstractmethod
    def find_by_card(self, card_number: str) -> RewardAccount:
        """
        Busca una cuenta de recompensas asociada a un número de tarjeta.
        Retorna la cuenta de recompensas encontrada o None si no existe.
        """
        pass
