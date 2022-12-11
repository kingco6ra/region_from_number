#!/usr/bin/python3
import asyncio
import re
import sys
from datetime import datetime
from typing import AsyncIterable, TypedDict

from aiohttp import ClientSession
from colorama import Fore


class ResponseJson(TypedDict):
    phone: str
    country: str  # unused
    region: str
    subRegion: str  # unused
    locality: str  # unused
    operator: str
    timeZone: str  # unused


async def parse_numbers(numbers_array: list[str]) -> AsyncIterable[str]:
    for number in numbers_array:
        number = re.search(r'[7|8][0-9]+', number)
        if number is None:
            continue
        yield number.group()


async def get_region(number: str) -> ResponseJson:
    async with ClientSession() as session:
        async with session.get(f'https://fincalculator.ru/api/tel/{number}') as response:
            return await response.json()


async def main():
    if len(sys.argv) == 1:
        print(
            f'~> {Fore.BLUE}get_region {Fore.RESET + Fore.YELLOW}$NUMBERS $TARGET_REGION\n{Fore.RESET}'
            f'{Fore.YELLOW}$NUMBERS{Fore.RESET} - номер или список из номеров, где каждый начинается с новой строки.\n'
            f'{Fore.YELLOW}$TARGET_REGION{Fore.RESET} - опциональный аргумент, указывается в том случае, если нужно найти номер с определенным регионом.'
        )
        sys.exit(0)

    start_time = datetime.now()
    numbers_array = sys.argv[1].split('\n')
    target_region = '' if len(sys.argv) != 3 else re.escape(sys.argv[2])
    print(f'{Fore.GREEN}Получение регионов.')

    async for number in parse_numbers(numbers_array):
        data = await get_region(number)
        region = data["region"]
        match = bool(re.match(target_region, region, re.IGNORECASE))

        print(
            f'{Fore.GREEN if match else Fore.CYAN}{data["phone"]} - {region or "Неизвестно"} - {data["operator"] or "Неизвестно"}'
        )
    end_time = datetime.now() - start_time
    print(f'{Fore.GREEN}Сканирование заняло {end_time.total_seconds()} сек.')


def run():
    asyncio.run(main())
