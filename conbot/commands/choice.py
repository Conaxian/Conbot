### Imports

# Standard Library
import sys
from random import choice

# Conbot Modules
sys.path.append("..")
from cmdtools import Arg
from cembed import cembed

### Command

# Command Meta
meta = {
    "name": "choice",
    "aliases": [
        "choose",
    ],
    "category": "chat",
    "index": 1,
    "args": [
        Arg("<choice1>", "word_comma"),
        Arg("<choice2>", "word_comma"),
        Arg("[choice3, ..., choiceN]", "inf_words_comma"),
    ],
}

# Command Call
async def call(ctx):
    choices = [ctx.args["choice1"], ctx.args["choice2"]]
    choices += ctx.args["choice3, ..., choiceN"] or []
    embed = cembed(ctx, choice(choices))
    await ctx.reply(embed=embed)
