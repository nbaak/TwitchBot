import asyncio

from .cog import Cog, get_cog_instance

function_command_register = {}


class Command:
    def __init__(self, cmd, func):
        self.cmd = cmd
        self.func = func

        self.is_async = is_async(func)
        self.is_method = is_method(func)

        if self.is_method:
            self.classname = (
                f"<class '{func.__module__}.{func.__qualname__.split('.')[0]}'>"
            )
        else:
            self.classname = None

    async def run(self, *args):
        if self.is_method:
            _instance = get_cog_instance(self.classname)
            if _instance:
                await self.func(_instance, *args)
            else:
                print(f"No Instance found for {self.classname}")
        else:
            await self.func(*args)

    def info(self):
        print(f"cmd: {self.cmd}, async: {self.is_async}, method: {self.is_method}")

    def __repr__(self):
        return f"cmd: {self.cmd}, async: {self.is_async}, method: {self.is_method}"

    def test(self):
        print(f"TEST: {self.cmd}")
        print(Cog.get_class(self.classname))


def is_async(func):
    return asyncio.iscoroutinefunction(func)


def is_method(func):
    return "self" in func.__code__.co_varnames


async def run(cmd, *args):
    if cmd in function_command_register:
        for command in function_command_register[cmd]:
            await command.run(*args)


def command(cmd):
    def decorator(func):
        command = Command(cmd, func)

        if cmd in function_command_register:
            function_command_register[cmd].append(command)
        else:
            function_command_register[cmd] = [command]
        return func

    return decorator
