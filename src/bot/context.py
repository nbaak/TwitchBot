

class Context:

    def __init__(self, client, opcode, user, channel, message, raw=None):
        self.client = client
        self.opcode = opcode
        self.user = user
        self.channel = channel
        self.message = message
        self.raw = raw

    def send(self, opcode, channel, message):
        self.client.send(opcode, channel, message)
