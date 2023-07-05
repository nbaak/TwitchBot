import asyncio
import sys

sys.path.append("..")

import bot
import os


@bot.command("!a")
async def test_a():
    print("Test A")


@bot.command("!a")
async def test_ab():
    print("Test AB")


def test(loop):
    # client = bot.Client()

    for f in os.listdir("./cogs"):
        if f.endswith(".py"):
            bot.load_extension(f"cogs.{f}")

    bot.debug_show_cogs()

    loop.run_until_complete(bot.run("!a"))

    loop.run_until_complete(bot.run("!c"))

    loop.run_until_complete(bot.run("!d"))

    # cd = test2.ClassD()
    loop.run_until_complete(bot.run("!e", "EE"))
    loop.run_until_complete(bot.run("!f"))

    loop.run_until_complete(bot.run("!ZZZZ"))
    print("#################")

    loop.run_until_complete(bot.run("PRIVMSG", "test123"))

    print("TEST DONE")


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    test(loop)
    loop.close()
