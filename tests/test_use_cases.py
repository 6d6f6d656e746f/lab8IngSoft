import pytest
from unittest.mock import MagicMock
from application.use_cases import PublishTransactionUseCase, ProcessTransactionUseCase
from application.ports.message_broker import MessagePublisher
from application.ports.repository import RewardRepository
from infrastructure.adapters.memory_repository import InMemoryRewardRepository
from domain.entities import RewardAccount

def test_publish_transaction_use_case():
    mock_publisher = MagicMock(spec=MessagePublisher)
    use_case = PublishTransactionUseCase(mock_publisher)
    
    result = use_case.execute(150.0, "1234-5678", "REST-999")
    
    assert result["monto"] == 150.0
    assert result["tarjeta_cliente"] == "1234-5678"
    assert result["restaurante_id"] == "REST-999"
    
    mock_publisher.publish.assert_called_once_with("laboratorio_1", result)


def test_process_transaction_use_case_new_account():
    mock_repo = MagicMock(spec=RewardRepository)
    mock_repo.find_by_card.return_value = None  # Simula que la cuenta no existe
    
    mock_notifier = MagicMock(spec=MessagePublisher)
    
    use_case = ProcessTransactionUseCase(mock_repo, mock_notifier)
    
    tx_data = {
        "monto": 200.0,
        "tarjeta_cliente": "4321-8765",
        "restaurante_id": "REST-111",
        "fecha_hora": "2026-05-30T12:00:00"
    }
    
    result = use_case.execute(tx_data)
    
    assert result["tarjeta_cliente"] == "4321-8765"
    assert result["puntos_ganados"] == 20.0
    assert result["puntos_acumulados"] == 20.0
    assert result["status"] == "PROCESSED"
    
    # Verificar que find_by_card y save fueron llamados
    mock_repo.find_by_card.assert_called_once_with("4321-8765")
    mock_repo.save.assert_called_once()
    
    # Verificar que se publicó notificación
    mock_notifier.publish.assert_called_once()


def test_process_transaction_use_case_existing_account():
    mock_repo = MagicMock(spec=RewardRepository)
    existing_account = RewardAccount("4321-8765", 15.5)
    mock_repo.find_by_card.return_value = existing_account
    
    use_case = ProcessTransactionUseCase(mock_repo) # Sin notificador
    
    tx_data = {
        "monto": 100.0,
        "tarjeta_cliente": "4321-8765",
        "restaurante_id": "REST-111",
        "fecha_hora": "2026-05-30T12:00:00"
    }
    
    result = use_case.execute(tx_data)
    
    assert result["tarjeta_cliente"] == "4321-8765"
    assert result["puntos_ganados"] == 10.0
    assert result["puntos_acumulados"] == 25.5
    
    mock_repo.save.assert_called_once_with(existing_account)


def test_process_transaction_notification_exception_handling():
    mock_repo = MagicMock(spec=RewardRepository)
    mock_repo.find_by_card.return_value = None
    
    mock_notifier = MagicMock(spec=MessagePublisher)
    mock_notifier.publish.side_effect = Exception("Connection error to notify queue")
    
    use_case = ProcessTransactionUseCase(mock_repo, mock_notifier)
    
    tx_data = {
        "monto": 50.0,
        "tarjeta_cliente": "1111-2222",
        "restaurante_id": "REST-999"
    }
    
    # No debería fallar el caso de uso principal si falla la notificación
    result = use_case.execute(tx_data)
    assert result["puntos_acumulados"] == 5.0
    mock_repo.save.assert_called_once()
    mock_notifier.publish.assert_called_once()


def test_in_memory_reward_repository():
    repo = InMemoryRewardRepository()
    
    # Verificar búsqueda de tarjeta inexistente
    assert repo.find_by_card("non-existent") is None
    
    # Guardar
    account = RewardAccount("9999-8888", 100.0)
    repo.save(account)
    
    # Buscar
    found = repo.find_by_card("9999-8888")
    assert found is not None
    assert found.tarjeta_cliente == "9999-8888"
    assert found.puntos_acumulados == 100.0
    
    # Test de error de tipo en save
    with pytest.raises(TypeError):
        repo.save("invalid type")
