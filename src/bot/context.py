class Context:
    def __init__(self, client, opcode, command, user, channel, message, raw=None):
        self.client = client
        self.opcode = opcode
        self.command = command
        self.user = user
        self.channel = channel
        
        
        if self.command in message:
            message = message.removeprefix(self.command)
        self.message = message.strip()
        self.raw = raw

    def send(self, opcode, channel, message):
        self.client.send(opcode, channel, message)
    
    async def reply(self, message, user=None):
        if user:
            pass
        else:
            await self.reply_channel(message)
        
    async def reply_channel(self, message):
        self.client.send(f"PRIVMSG {self.channel} :{message}")
        await self.client.writer.drain()
        
    def __repr__(self):
        return f"{self.user} {self.channel}: {self.message}"