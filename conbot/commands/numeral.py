### Imports

# Standard Library
import sys
from num2words import num2words

# Conbot Modules
sys.path.append("..")
import const
from cmdtools import Arg, CmdError
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "numeral",
    "aliases": [
        "num2word",
        "num2words",
    ],
    "category": "chat",
    "index": 2,
    "args": [
        Arg("<number>", "num"),
    ],
}

# Command Call
async def call(ctx):
    number = ctx.args["number"]
    try:
        num_str = num2words(number)
        if len(num_str) > const.embed_desc_limit:
            raise OverflowError
    except OverflowError:
        raise CmdError("cmd/numeral/too_large")

    num_str = num_str.title().replace("And", "and")
    title = Loc("cmd/numeral/title")
    embed = cembed(ctx, num_str, title=title)
    await ctx.reply(embed=embed)
