### Imports

# Standard Library
import sys
from random import randint

# Conbot Modules
sys.path.append("..")
from cmdtools import Arg
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "gay",
    "aliases": [
        "how-gay",
        "gay-level",
        "gay-meter",
    ],
    "category": "chat",
    "index": 4,
    "args": [
        Arg("[target]", "inf_str"),
    ],
}

# Command Call
async def call(ctx):
    target = ctx.args["target"] or ctx.author.mention
    gayness = randint(0, 100)
    text = Loc("cmd/gay/text").format(target, gayness)
    title = Loc("cmd/gay/title")
    embed = cembed(ctx, text, title=title)
    await ctx.reply(embed=embed)
