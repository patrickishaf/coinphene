from db import Wallet, session as db_session
import requests
from config import wallet_service_url, native_mint, token_secret
import common.encryption as encryption


http_session = requests.Session()
http_session.headers.update({
    "CP-Auth-Hdr": encryption.encrypt(f"Bearer {token_secret}")
})


def get_wallet_by_telegram_id(id: int):
    try:
        wallet = db_session.query(Wallet).where(Wallet.user_telegram_id.is_(id)).first()
        return wallet
    except Exception as e:
        print(f"failed to find wallets for user. error: {e}")
        return None


def generate_wallet():
    try:
        res = http_session.post(f"{wallet_service_url}/keypair/sol")
        res.raise_for_status()
        data = res.json()
        return data
    except Exception as e:
        print(f"failed to generate wallet addresses. error: {e}")
        return None


def save_wallet_to_user(wallet: Wallet):
    try:
        db_session.add(wallet)
        db_session.commit()
    except Exception as e:
        print(f"failed to insert wallet into db. error: {e}")


def get_wallet_balance(address: str, detailed = False):
    try:
        res = http_session.request(method="GET", url=f"{wallet_service_url}/balances/{address}?detailed={detailed}")
        res.raise_for_status()
        data = res.json()
        return data
    except Exception as e:
        print(f"failed to get wallet balance. error: {e}")
        return None


def get_sol_balance(address: str):
    try:
        res = http_session.request(method="GET", url=f"{wallet_service_url}/sol-balance/{address}")
        res.raise_for_status()
        data = res.json()
        return data
    except Exception as e:
        print(f"failed to get wallet balance. error: {e}")
        return None


def get_tokens_in_wallet(address):
    try:
        res = http_session.get(f"https://wallet-api.solflare.com/v3/portfolio/tokens/{address}?network=mainnet&currency=USD&enablePartialErrors=true")
        res.raise_for_status()
        data = res.json()
        return data
    except Exception as e:
        print(f"failed to get tokens in wallet. error: {e}")
        return None


def buy_token(owner_sk: str, amount: float, token_address):
    try:
        body = {
                "owner_sk": owner_sk,
                "amount": amount,
                "input_mint": token_address,
                "output_mint": native_mint
            }
        res = http_session.post(f"{wallet_service_url}/swap", data=body)
        res.raise_for_status()
        data = res.json()
        return data
    except Exception as e:
        print(f"failed to buy token. error: {e}")
        return None


def withdraw_sol(amount: float, token_address: str):
    try:
        name = "greatest in the world"
    except Exception as e:
        print(f"failed to buy token. error: {e}")
        return None


def sell_token(owner_sk: str, amount: float, token_address: str):
    try:
        body = {
                "owner_sk": owner_sk,
                "amount": amount,
                "input_mint": native_mint,
                "output_mint": token_address
            }
        res = http_session.post(f"{wallet_service_url}/swap", data=body)
        res.raise_for_status()
        data = res.json()
        return data
    except Exception as e:
        print(f"failed to sell token. error: {e}")
        return None


def send_token(to_address: str, amount: float, secret_key: str):
    try:
        body = {
                "from_secret_key": secret_key,
                "amount": amount,
                "to_pub_key": to_address,
            }
        res = http_session.post(f"{wallet_service_url}/send-sol", data=body)
        res.raise_for_status()
        signature = res.json()
        return signature
    except Exception as e:
        print(f"failed to sell token. error: {e}")
        return None
    