### Imports

# Standard Library
from typing import Generator

### Class Definitions

# Flags
class Flags:
    """
    Stores flags as attributes with boolean values.
    """

    def __init__(self, *flags):
        for flag in flags:
            setattr(self, flag, True)

    def __repr__(self):
        return str(tuple(vars(self).keys()))

    def __getattr__(self, attr: str) -> bool:
        return False

# Attribute Dict
class AttrDict:
    """
    Stores key-value pairs as attributes.
    """

    def __init__(self, **attrs):
        for key, value in attrs.items():
            setattr(self, key, value)

    def __repr__(self):
        return str(vars(self))

    def __getattr__(self, attr: str):
        pass

    def __getitem__(self, key):
        return getattr(self, str(key))

    def __bool__(self) -> bool:
        return bool(vars(self))

    def __iter__(self) -> Generator:
        for key, value in vars(self).items():
            yield key, value

    def keys(self) -> tuple[str]:
        return tuple(vars(self).keys())

    def values(self) -> tuple:
        return tuple(vars(self).values())
