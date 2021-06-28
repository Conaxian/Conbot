### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
from cmdtools import Arg

### Command

# Command Meta
meta = {
    "name": "emoji",
    "aliases": [
        "emote",
    ],
    "category": "tools",
    "index": 0,
    "args": [
        Arg("<name>", "custom_emoji_any"),
    ],
}

# Command Call
async def call(ctx):
    emoji = ctx.args["name"]
    await ctx.reply(str(emoji))
