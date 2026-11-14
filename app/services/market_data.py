from sqlalchemy.orm import Session
from app.clients import coingecko
from app.repositories import users as users_repository

class InvalidCoinSymbolError(Exception):
    pass

async def get_coin_list():
    coins = await coingecko.get_coin_list()

    return [
            {
                "id": coin["id"],
                "symbol": coin["symbol"],
                "name": coin["name"],
                "image": coin["image"],
                "current_price": coin["current_price"],
            }
            for coin in coins
        ]

async def get_coin(coin_symbol: str):
    try:
        coin = await coingecko.get_coin(coin_symbol)
    except Exception:
        raise InvalidCoinSymbolError

    if not coin or coin_symbol not in coin:
        raise InvalidCoinSymbolError

    return coin


async def get_coins(coin_symbols: list[str]):
    try:
        coins = await coingecko.get_coins(coin_symbols)
    except Exception:
        raise InvalidCoinSymbolError

    if not coins or coin_symbols[0] not in coins:
        raise InvalidCoinSymbolError

    return coins