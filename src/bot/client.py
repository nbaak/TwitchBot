import asyncio

class Client:
    def __init__(self, bot_username, channel, oauth_token):
        self.server = "irc.chat.twitch.tv"
        self.port = 6667
        self.bot_username = bot_username
        self.channel = channel
        self.oauth_token = oauth_token
        self.connected = False
        
        self.opcode_handlers = {}

    async def connect(self):
        self.reader, self.writer = await asyncio.open_connection(self.server, self.port)
        self.writer.write(f"PASS {self.oauth_token}\n".encode("utf-8"))
        self.writer.write(f"NICK {self.bot_username}\n".encode("utf-8"))
        self.writer.write(f"JOIN #{self.channel}\n".encode("utf-8"))
        await self.writer.drain()
        self.connected = True

    async def send_message(self, message):
        self.writer.write(f"PRIVMSG #{self.channel} :{message}\n".encode("utf-8"))
        await self.writer.drain()

    async def check_connection(self):
        self.writer.write("PING :tmi.twitch.tv\n".encode("utf-8"))
        await self.writer.drain()

        resp = await self.reader.read(2048).decode("utf-8")

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
                resp = await self.reader.read(2048).decode("utf-8")

                if resp.startswith("PING"):
                    self.writer.write("PONG\n".encode("utf-8"))
                    await self.writer.drain()
                elif "PRIVMSG" in resp:
                    username = resp.split("!", 1)[0].lstrip(":")
                    message = resp.split("PRIVMSG", 1)[1].split(":", 1)[1].rstrip("\r\n")

                    for opcode in self.opcode_handlers:
                        if message.startswith(opcode):
                            await self.handle_opcode(opcode, message)

                # Add more message processing logic as needed

            except ConnectionResetError:
                self.connected = False
                self.writer.close()
                await asyncio.sleep(2)  # Wait for 2 seconds before attempting to reconnect
                continue

            await self.check_connection()
            await asyncio.sleep(0.1)  # Adjust the sleep time as needed
