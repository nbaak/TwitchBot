import importlib
import inspect

from pathlib import Path

cogs = {}

class Cog:

    def __init__(self):
        print(f"registering cog class: {self.__class__}")
        cogs[str(self.__class__)] = self
        
    @staticmethod
    def get_class(classname):
        if classname in cogs:
            return cogs[classname]
            
        return None
        

def load_extension(path):
    path = Path(path)
    
    module = importlib.import_module(path.stem)
    
    for name_local in dir(module):
        if inspect.isclass(getattr(module, name_local)):
            print(f'{name_local} is a class')
            _class = getattr(module, name_local)
            _object = _class()
            
            if not _object.__class__ in cogs:
                cogs[str(_object.__class__)] = _object
                
                
def debug_show_cogs():
    for k,v in cogs.items():
        print(k, v)