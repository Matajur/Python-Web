import asyncio
import logging
import sys

import requests

from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta
from time import time

URL = "https://api.privatbank.ua/p24api/exchange_rates?json&date=01.12.2014"
BASE_C = ("USD", "EUR")
MAX_DAYS = 10
MIN_DAYS = 1
TODAY = datetime.now()
if TODAY.hour < 8:
    TODAY = TODAY - timedelta(hours=8)


def preview_fetch(day):
    logging.debug(f"Starting day: {day}")
    start = time()
    that_day = TODAY - timedelta(days=day)
    url = f"{URL[:-10]}{that_day.strftime('%d.%m.%Y')}"
    try:
        r = requests.get(url)
        if r.status_code == 200:
            logging.debug(f"Finishing day: {day} in {round(time() - start, 2)} sec")
            return r.json()
        else:
            logging.error(f"Error status: {r.status_code} for {url}")
    except:
        logging.error(f"Server connection error occured for {url}")


async def preview_fetch_async(days):
    loop = asyncio.get_running_loop()

    with ThreadPoolExecutor(days) as pool:
        futures = [
            loop.run_in_executor(pool, preview_fetch, day) for day in range(days)
        ]
        result = await asyncio.gather(*futures, return_exceptions=True)
        return result


async def parser(days, new_currency):
    database = await preview_fetch_async(days)
    result = f"Printing exchange rates for last {days} days:"
    for record in database:
        if record is not None:
            result += f"\n{record['date']}"
            for el in record["exchangeRate"]:
                if el["currency"] in BASE_C or el["currency"] == new_currency:
                    result += f"\n{el['currency']} -> buy: {el['purchaseRate']} / sale: {el['saleRate']}"
    return result


if __name__ == "__main__":
    """
    Input example:
    python utility.py 5 PLN
    """
    start = time()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(message)s")
    try:
        days = int(sys.argv[1])
        if days > MAX_DAYS:
            days = MAX_DAYS
        if days < MIN_DAYS:
            days = 1
    except:
        days = MIN_DAYS
    try:
        new_currency = sys.argv[2].strip().upper()
    except:
        new_currency = None
    print(asyncio.run(parser(days, new_currency)))
    logging.debug(f"Total execution time: {round(time() - start, 2)} sec")
