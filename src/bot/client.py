import asyncio

# import bot.handler

import bot
import opcode
from .context import Context


class Client:
    def __init__(self, bot_username, oauth_token, channels):
        self.server = "irc.chat.twitch.tv"
        self.port = 6667
        self.bot_username = bot_username
        self.channel = channels[0] # just the first channel for now
        self.oauth_token = oauth_token
        self.connected = False

        self.opcode_handlers = {}

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.server, self.port)
        self.send(f"PASS {self.oauth_token}")
        self.send(f"NICK {self.bot_username}")
        self.send(f"JOIN {self.channel}")
        await self.writer.drain()
        self.connected = True

    async def send_message(self, message):
        self.writer.write(f"PRIVMSG #{self.channel} :{message}\n".encode("utf-8"))
        await self.writer.drain()

    def send(self, message):
        self.writer.write(f"{message}\n".encode("utf-8"))

    async def check_connection(self):
        self.writer.write("PING :tmi.twitch.tv\n".encode("utf-8"))
        await self.writer.drain()
        
        resp = await self.reader.read(2048)
        resp = resp.decode("utf-8")

        if resp.startswith("PING"):
            self.writer.write("PONG\n".encode("utf-8"))
            await self.writer.drain()
        else:
            self.connected = False
            self.writer.close()

    async def handle_opcode(self, opcode, *args):
        handler = self.opcode_handlers.get(opcode)
        if handler:
            if asyncio.iscoroutinefunction(handler):
                await handler(*args)
            else:
                handler(*args)

    def opcode_handler(self, opcode):
        def decorator(func):
            self.opcode_handlers[opcode] = func
            return func

        return decorator

    async def start(self):
        await self.connect()

        while True:
            if not self.connected:
                await self.connect()

            try:
                resp = await self.reader.read(2048)
                resp = resp.decode("utf-8")
                print(f"raw: {resp}")
                # Build Context Object
                # :k3nny0r!k3nny0r@k3nny0r.tmi.twitch.tv PRIVMSG #k3nny0r :test
                # :k3nny0r!k3nny0r@k3nny0r.tmi.twitch.tv PRIVMSG #sadschlong :asdasd
                message_data = resp.split(':', maxsplit=2)
                message_data.pop(0)
                # print(message_data)
                com_data = message_data[0].strip().split(' ')                
                message = message_data[-1]
                print(com_data)
                print(message)
                
                if resp.startswith("PING"):
                    self.writer.write("PONG\n".encode("utf-8"))
                    await self.writer.drain()
                elif "PRIVMSG" in resp:
                    username = resp.split("!", 1)[0].lstrip(":")
                    message = (
                        resp.split("PRIVMSG", 1)[1].split(":", 1)[1].rstrip("\r\n")
                    )

                    for opcode in self.opcode_handlers:
                        if message.startswith(opcode):
                            await self.handle_opcode(opcode, message)

                # Add more message processing logic as needed

            except ConnectionResetError:
                self.connected = False
                self.writer.close()
                await asyncio.sleep(
                    2
                )  # Wait for 2 seconds before attempting to reconnect
                continue

            # await self.check_connection()
            await asyncio.sleep(0.1)  # Adjust the sleep time as needed
