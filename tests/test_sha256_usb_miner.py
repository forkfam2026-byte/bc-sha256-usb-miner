import sha256_usb_miner
from sha256_usb_miner import SHA256Miner, MinerConfig


def test_mine_finds_nonce_with_monkeypatch(monkeypatch):
    class DummyHash:
        def __init__(self, _):
            pass
        def hexdigest(self):
            return "0" + "f" * 63

    monkeypatch.setattr("sha256_usb_miner.hashlib.sha256", lambda x: DummyHash(x))

    config = MinerConfig(difficulty=1, max_nonce=100)
    miner = SHA256Miner(config)
    result = miner.mine("data")
    assert result.hash_value.startswith("0")
    assert result.nonce == 0
