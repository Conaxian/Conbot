### Imports

# Standard Library
import os
import sys
import importlib
from typing import Callable

# Conbot Modules
sys.path.append("..")
import const
from cbcollections import Flags

### Class definitions

# Command
class Command:
    """
    Holds all information about a single command.
    """

    def __init__(self,
        name: str,
        aliases: list[str],
        category: str,
        index: int,
        args: list,
        perms: list,
        flags: list,
        call: Callable,
    ):
        self.name = name
        self.aliases = aliases
        self.category = category
        self.index = index
        self.args = args
        self.perms = perms
        self.flags = flags
        self.call = call

    def calls(self) -> list:
        """
        Returns all calls of the command.
        """
        return [self.name] + self.aliases

### Initialization

# Define an empty list of commands
commands = []

# Import all commands and add them to the list
for cmd_file in os.listdir(const.cmd_dir):
    if not cmd_file.endswith(".py") or cmd_file == "__init__.py": continue
    module_name = "." + cmd_file.removesuffix(".py")
    cmd_module = importlib.import_module(module_name, const.cmd_dir)

    meta = cmd_module.meta
    flags = meta.get("flags", [])
    command = Command(
        meta["name"],
        meta.get("aliases", []),
        meta["category"],
        meta.get("index", 0),
        meta.get("args", []),
        meta.get("perms", []),
        Flags(*flags),
        cmd_module.call,
    )
    commands.append(command)
