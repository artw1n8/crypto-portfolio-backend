import os
import aiohttp
from dotenv import load_dotenv

load_dotenv()

api_key = os.environ["COINGECKO_API_KEY"]

timeout = aiohttp.ClientTimeout(total=10)

headers = {
    "x-cg-demo-api-key": api_key,
}

async def get_coin_list():
    async with aiohttp.ClientSession(
        headers=headers,
        timeout=timeout
    ) as session:
        async with session.get(
            "https://api.coingecko.com/api/v3/coins/markets",
                params={
                    "vs_currency": "usd",
                    "order": "market_cap_desc",
                    "per_page": 20,
                    "page": 1,
                },
        ) as response:
            response.raise_for_status()
            return await response.json()


async def get_coin(coin_name: str):
    async with aiohttp.ClientSession(
        headers=headers,
        timeout=timeout
    ) as session:
        async with session.get(
            "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": f"{coin_name}",
                    "vs_currencies": "usd",
                    "include_last_updated_at": "true",
                },
        ) as response:
            response.raise_for_status()
            return await response.json()


async def get_coins(coin_names: list[str]):
    async with aiohttp.ClientSession(
        headers=headers,
        timeout=timeout
    ) as session:
        async with session.get(
            "https://api.coingecko.com/api/v3/simple/price",
                params={
                    "ids": f",".join(coin_names),
                    "vs_currencies": "usd",
                    "include_last_updated_at": "true",
                },
        ) as response:
            response.raise_for_status()
            return await response.json()