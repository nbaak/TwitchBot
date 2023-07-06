
import bot

class TestBotAnswer(bot.Cog): # bot.Cog
    
    def __init__(self):
        super().__init__()
    
    @bot.command('!test')
    async def test_command(self, ctx):
        if ctx.message:
            await ctx.reply(f"you said: {ctx.message}")
        else:
            await ctx.reply("yes?")
            
    @bot.command('!hello')
    async def hello(self, ctx):
        await ctx.reply(f"hello, {ctx.user}")