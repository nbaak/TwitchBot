import asyncio

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
                
                if resp.startswith("PING"):
                    self.writer.write("PONG\n".encode("utf-8"))
                    await self.writer.drain()
                    
                elif "PRIVMSG" in resp:
                    # get sender informations
                    username = resp.split("!", 1)[0].lstrip(":")
                    channel = resp.split(':', maxsplit=2)[1].split(' ')[2]
                    message = (
                        resp.split("PRIVMSG", 1)[1].split(":", 1)[1].rstrip("\r\n")
                    )
                    
                    # handle commands here
                    if message.startswith("!"):
                        cmd = message.split(' ')[0].strip()
                        ctx = Context(self, 'PRIVMSG', cmd, username, channel, message, resp)
                        print(ctx)
                        await bot.run(cmd, ctx)

                # Add more message processing logic as needed

            except ConnectionResetError:
                self.connected = False
                self.writer.close()
                await asyncio.sleep(
                    2
                )  # Wait for 2 seconds before attempting to reconnect
                continue

            # await self.check_connection() # todo: fix it?
            await asyncio.sleep(0.1)  # Adjust the sleep time as needed
