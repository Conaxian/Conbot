### Imports

# Standard Library
import sys
from random import randint

# Conbot Modules
sys.path.append("..")
from cmdtools import Arg, CmdError

### Command

# Command Meta
meta = {
    "name": "rng",
    "aliases": [
        "random",
        "randint",
    ],
    "category": "chat",
    "index": 0,
    "args": [
        Arg("<min>", "int"),
        Arg("<max>", "int"),
    ],
}

# Command Call
async def call(ctx):
    min_num, max_num = ctx.args["min"], ctx.args["max"]
    if min_num >= max_num:
        raise CmdError("cmd/rng/invalid_range")
    number = randint(min_num, max_num)
    await ctx.reply(str(number))
