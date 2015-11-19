import sys
import inspect

from . import props

class Terrain:
    props_available = None
    
    def __str__(self):
        return self.__class__.__name__.lower()

class Meadow(Terrain):
    symbol = "  " # boring ol' meadow
    props_available = [
        (props.Bush, 0.8),
        (props.Brook, 0.1),
        (props.Stream, 0.1)]


class Lake(Terrain):
    symbol = "~~" # waves?
    props_available = [
        (props.Water, 1)]


class Forest(Terrain):
    symbol = '||' # trees?
    props_available = [(props.Tree, 0.9)] * 35 + [
        (props.Stream, 0.2)]


terrains = [cls
    for name, cls
    in inspect.getmembers(sys.modules[__name__])
    if inspect.isclass(cls) and issubclass(cls, Terrain) and cls != Terrain]
