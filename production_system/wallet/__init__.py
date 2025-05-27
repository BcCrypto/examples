import json
import os
import time
from typing import Tuple

import httpx
from cryptography.fernet import Fernet

WALLET_FILE = "ian_stubbs_wallet.json"
WALLET_KEY = "ian_wallet.key"


def _get_fernet() -> Fernet:
    if not os.path.exists(WALLET_KEY):
        with open(WALLET_KEY, "wb") as f:
            f.write(Fernet.generate_key())
    return Fernet(open(WALLET_KEY, "rb").read())


def _load_wallet() -> dict:
    fernet = _get_fernet()
    if not os.path.exists(WALLET_FILE):
        data = {"balance": 0, "history": []}
        with open(WALLET_FILE, "wb") as f:
            f.write(fernet.encrypt(json.dumps(data).encode()))
        return data

    encrypted = open(WALLET_FILE, "rb").read()
    return json.loads(fernet.decrypt(encrypted).decode())


def _save_wallet(data: dict) -> None:
    fernet = _get_fernet()
    with open(WALLET_FILE, "wb") as f:
        f.write(fernet.encrypt(json.dumps(data).encode()))


def update_wallet(amount: int, reason: str) -> None:
    """Update wallet balance with a reason."""
    data = _load_wallet()
    data["balance"] += amount
    data.setdefault("history", []).append({
        "amount": amount,
        "reason": reason,
        "ts": time.time(),
    })
    _save_wallet(data)


def get_balance() -> int:
    return _load_wallet().get("balance", 0)


def transfer_tokens(target: str, amount: int) -> Tuple[bool, str]:
    """Transfer tokens from this wallet to another encrypted wallet."""
    wallet_path = f"{target}_wallet.json"
    if not os.path.exists(wallet_path):
        return False, f"Target wallet '{target}' does not exist."

    data = _load_wallet()
    if data["balance"] < amount:
        return False, "Insufficient balance."

    data["balance"] -= amount
    data.setdefault("history", []).append({
        "amount": -amount,
        "reason": f"Transfer to {target}",
        "ts": time.time(),
    })
    _save_wallet(data)

    target_fernet = _get_fernet()
    with open(wallet_path, "rb") as f:
        target_data = json.loads(target_fernet.decrypt(f.read()).decode())
    target_data["balance"] += amount
    target_data.setdefault("history", []).append({
        "amount": amount,
        "reason": f"Received from Ian Stubbs",
        "ts": time.time(),
    })
    with open(wallet_path, "wb") as f:
        f.write(target_fernet.encrypt(json.dumps(target_data).encode()))

    receipt = {
        "from": "Ian Stubbs",
        "to": target,
        "amount": amount,
        "timestamp": time.time(),
    }
    with open("transfer_receipts.log", "a") as f:
        f.write(json.dumps(receipt) + "\n")

    return True, f"Transferred {amount} tokens to {target}."


async def redeem_proof(proof: str) -> None:
    """Redeem a QR code proof via remote endpoints and reward the wallet."""
    async with httpx.AsyncClient() as client:
        await client.post("https://rfdelta.com/eth/redeem", json={"proof": proof})
        await client.post("https://rfdelta.com/api/unlock", json={"token": proof})
    update_wallet(10, f"Reward from proof: {proof}")

