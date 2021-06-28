### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "shutdown",
    "category": "dev",
    "aliases": [
        "exit",
        "off",
    ],
    "flags": [
        "dev",
    ],
}

# Command Call
async def call(ctx):
    text = Loc("cmd/shutdown/exit")
    embed = cembed(ctx, text)
    await ctx.reply(embed=embed)
    await ctx.bot.close()
