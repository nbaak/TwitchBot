
import inspect
import importlib
import sys

from pathlib import Path

cogs = []


def load_extension(path):
    print(path)
    path = Path(path)
    
    module = importlib.import_module(path.stem)
    
    for name_local in dir(module):
        if inspect.isclass(getattr(module, name_local)):
            print(f'{name_local} is a class')
            MysteriousClass = getattr(module, name_local)
            mysterious_object = MysteriousClass()
            
            print(mysterious_object.__class__)
            cogs.append(mysterious_object)
