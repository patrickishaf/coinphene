import requests
from sqlalchemy import select
from db import SplToken, session as db_session

http_session = requests.Session()
base_url = "https://api.geckoterminal.com/api/v2"


def get_token_info(token_address):
    try:
        res = http_session.get(f"{base_url}/networks/solana/tokens/{token_address}")
        res.raise_for_status()
        data = res.json()
        return data
    except Exception as e:
        print(f"failed to get token info. error: {e}")
        return None

# def get_ohlc():
#     try:
#         res = http_session.get("https://wallet-api.solflare.com/v2/trade/chart/ohlcv?baseAddress=4k3Dyjzvzp8eMZWUXbBCjEvwSkkk59S5iCNLY3QrkX6R&currency=usd&interval=1H&timeFrom=1725954970&timeTo=1727034970")
#         res.raise_for_status()
#         data = res.json()
#         return data
#     except Exception as e:
#         print(f"failed to get additional data. error: {e}")
#         return None
    

def get_token_from_symbol_cached(symbol: str):
    try:
        query = select(SplToken).where(SplToken.symbol.is_(symbol))
        token = db_session.scalar(query)
        return token
    except Exception as e:
        print(f"failed to get cached token from symbol. error: {e}")
        return None
    

def get_token_from_address_cached(address: str):
    try:
        query = select(SplToken).where(SplToken.address.is_(address))
        token = db_session.scalar(query)
        return token
    except Exception as e:
        print(f"failed to get cached token from address. error: {e}")
        return None
    

def create_spl_token(token: SplToken):
    # if token exists, return
    # if token does not exist, create it
    try:
        existing = db_session.query(SplToken).where(SplToken.address.is_(token.address)).first()
        if existing is None:
            db_session.add(token)
            db_session.commit()
    except Exception as e:
        print(f"failed to save spl token info. error: {e}")


def create_roman_reigns():
    pass