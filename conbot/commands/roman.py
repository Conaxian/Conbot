### Imports

# Standard Library
import sys

# Dependencies
from roman import toRoman as to_roman
from roman import OutOfRangeError

# Conbot Modules
sys.path.append("..")
from cmdtools import Arg, CmdError
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "roman",
    "category": "chat",
    "index": 3,
    "args": [
        Arg("<number>", "int"),
    ],
}

# Command Call
async def call(ctx):
    number = ctx.args["number"]
    try:
        num_str = to_roman(number)
    except OutOfRangeError:
        raise CmdError("cmd/roman/too_large")

    title = Loc("cmd/roman/title")
    embed = cembed(ctx, num_str, title=title)
    await ctx.reply(embed=embed)
