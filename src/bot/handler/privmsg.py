import bot


@bot.command('PRIVMSG')
async def privmsg(ctx):
    print(f"CTX: {ctx}")
