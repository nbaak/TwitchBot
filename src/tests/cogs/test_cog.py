
import bot


class ClassB(bot.Cog):
    
    def __init__(self, bot=None):
        super().__init__()
        self.name = "GURKE D"
        self.bot = bot

    @bot.command('!d')
    async def test_D(self):
        print('Test D')
        print(self.name)


class ClassD(bot.Cog):
    
    @bot.command('!e')
    async def wusel(self, a):
        self.a = a
        
    @bot.command('!f')
    async def pusel(self):
        print(f'Test F-{self.a}')
        