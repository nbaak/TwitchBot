import importlib
import inspect

from pathlib import Path

loaded_cog_objects = {}  # Singletons


class Cog:

    def __init__(self):
        print(f"registering cog class: {self.__class__}")
        loaded_cog_objects[str(self.__class__)] = self

    @staticmethod
    def get_class(classname):
        if classname in loaded_cog_objects:
            return loaded_cog_objects[classname]

        return None


def load_extension(path):
    path = Path(path)

    module = importlib.import_module(path.stem)

    for name_local in dir(module):
        if inspect.isclass(getattr(module, name_local)):
            print(f'{name_local} is a class')
            _class = getattr(module, name_local)
            _object = _class()

            if not _object.__class__ in loaded_cog_objects:
                loaded_cog_objects[str(_object.__class__)] = _object


def debug_show_cogs():
    for k, v in loaded_cog_objects.items():
        print(k, v)
