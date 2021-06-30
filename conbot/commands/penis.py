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
    "name": "penis",
    "aliases": [
        "penis-length",
        "penis-size",
    ],
    "category": "chat",
    "index": 5,
    "args": [
        Arg("[target]", "inf_str"),
    ],
}

# Command Call
async def call(ctx):
    target = ctx.args["target"] or ctx.author.mention
    penis = "**8" + ("=" * randint(0, 10)) + ">**"
    text = Loc("cmd/penis/text").format(target, penis)
    title = Loc("cmd/penis/title")
    embed = cembed(ctx, text, title=title)
    await ctx.reply(embed=embed)
