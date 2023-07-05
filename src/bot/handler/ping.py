import bot


@bot.command("PING")
async def ping(ctx):
    ctx.send("PONG")
