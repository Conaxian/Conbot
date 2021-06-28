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
    "name": "status",
    "aliases": [
        "online",
        "test",
    ],
    "category": "info",
    "index": 2,
}

# Command Call
async def call(ctx):
    text = Loc("cmd/status/online")
    embed = cembed(ctx, text)
    await ctx.reply(embed=embed)
