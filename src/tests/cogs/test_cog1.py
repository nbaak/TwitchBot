
import bot

class ClassA(bot.Cog): # bot.Cog
    
    def __init__(self):
        super().__init__()
        self.name = 'C'
    
    @bot.command('!c')
    async def test_123(self):
        print('Test 1 2 3')
        print(self.name)