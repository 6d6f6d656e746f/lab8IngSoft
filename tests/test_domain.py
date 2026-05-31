import pytest
from domain.entities import Transaction, RewardAccount

def test_transaction_creation_success():
    tx = Transaction(150.0, "1234-5678", "REST-999", "2026-05-30T20:00:00")
    assert tx.monto == 150.0
    assert tx.tarjeta_cliente == "1234-5678"
    assert tx.restaurante_id == "REST-999"
    assert tx.fecha_hora == "2026-05-30T20:00:00"

def test_transaction_creation_invalid_monto():
    with pytest.raises(ValueError, match="monto consumido debe ser mayor a cero"):
        Transaction(0, "1234-5678", "REST-999")
    with pytest.raises(ValueError, match="monto consumido debe ser mayor a cero"):
        Transaction(-10.5, "1234-5678", "REST-999")

def test_transaction_creation_invalid_tarjeta():
    with pytest.raises(ValueError, match="tarjeta del cliente es inválido"):
        Transaction(100.0, "", "REST-999")
    with pytest.raises(ValueError, match="tarjeta del cliente es inválido"):
        Transaction(100.0, None, "REST-999")

def test_transaction_creation_invalid_restaurante():
    with pytest.raises(ValueError, match="código del restaurante es inválido"):
        Transaction(100.0, "1234-5678", "")
    with pytest.raises(ValueError, match="código del restaurante es inválido"):
        Transaction(100.0, "1234-5678", None)

def test_transaction_to_dict():
    tx = Transaction(200.0, " 9876-5432 ", " REST-888 ", "2026-05-30")
    d = tx.to_dict()
    assert d["monto"] == 200.0
    assert d["tarjeta_cliente"] == "9876-5432"  # Stripped
    assert d["restaurante_id"] == "REST-888"    # Stripped
    assert d["fecha_hora"] == "2026-05-30"

def test_reward_account_creation_success():
    account = RewardAccount("1234-5678", 50.0)
    assert account.tarjeta_cliente == "1234-5678"
    assert account.puntos_acumulados == 50.0

def test_reward_account_creation_invalid_tarjeta():
    with pytest.raises(ValueError, match="tarjeta del cliente es inválido"):
        RewardAccount("")
    with pytest.raises(ValueError, match="tarjeta del cliente es inválido"):
        RewardAccount(None)

def test_reward_account_accumulation_success():
    account = RewardAccount("1234-5678", 10.0)
    nuevos_puntos = account.acumular_puntos(150.0)
    assert nuevos_puntos == 15.0  # 10% of 150
    assert account.puntos_acumulados == 25.0  # 10 + 15

def test_reward_account_accumulation_invalid_monto():
    account = RewardAccount("1234-5678")
    with pytest.raises(ValueError, match="monto para acumular puntos debe ser mayor a cero"):
        account.acumular_puntos(0)
    with pytest.raises(ValueError, match="monto para acumular puntos debe ser mayor a cero"):
        account.acumular_puntos(-50)
