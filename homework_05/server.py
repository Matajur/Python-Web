import asyncio
import logging

import names
import websockets

from utility import MAX_DAYS, MIN_DAYS, parser

from datetime import datetime

from aiofile import async_open
from websockets import WebSocketServerProtocol, WebSocketProtocolError
from websockets.exceptions import ConnectionClosedOK


class Server:
    clients = set()

    async def register(self, ws: WebSocketServerProtocol):
        ws.name = names.get_full_name()
        self.clients.add(ws)
        logging.info(f"{ws.remote_address} connects")

    async def unregister(self, ws: WebSocketServerProtocol):
        self.clients.remove(ws)
        logging.info(f"{ws.remote_address} disconnects")

    async def send_to_clients(self, message: str):
        if self.clients:
            [await client.send(message) for client in self.clients]

    async def ws_handler(self, ws: WebSocketServerProtocol):
        await self.register(ws)
        try:
            await self.distrubute(ws)
        except ConnectionClosedOK:
            pass
        finally:
            await self.unregister(ws)

    async def distrubute(self, ws: WebSocketServerProtocol):
        async for message in ws:
            if message.startswith("exchange"):
                await self.make_log()
                r = await self.exchanger(message)
                await self.send_to_clients(r)
            else:
                await self.send_to_clients(f"{ws.name}: {message}")

    async def exchanger(self, message):
        """
        Input example:
        exchange 5 PLN
        """
        args = message.strip().split(" ", 2)
        try:
            days = int(args[1])
            if days > MAX_DAYS:
                days = MAX_DAYS
            if days < MIN_DAYS:
                days = 1
        except:
            days = MIN_DAYS
        try:
            new_currency = args[2].strip().upper()
        except:
            new_currency = None
        r = await parser(days, new_currency)
        return r

    async def make_log(self):
        now = datetime.now()
        async with async_open("log.dat", "a+") as file:
            await file.write(f"{now}\n")


async def main():
    server = Server()
    async with websockets.serve(server.ws_handler, "localhost", 8080):
        await asyncio.Future()  # run forever


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    try:
        asyncio.run(main())
    except KeyboardInterrupt as err:
        print("Server stopped")
