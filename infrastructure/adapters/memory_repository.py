from application.ports.repository import RewardRepository
from domain.entities import RewardAccount

class InMemoryRewardRepository(RewardRepository):
    def __init__(self):
        self._accounts = {}

    def save(self, account: RewardAccount) -> None:
        if not account or not isinstance(account, RewardAccount):
            raise TypeError("Se esperaba una instancia de RewardAccount")
        self._accounts[account.tarjeta_cliente] = account

    def find_by_card(self, card_number: str) -> RewardAccount:
        return self._accounts.get(card_number, None)
