### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
from cmdtools import Arg
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "announce",
    "category": "dev",
    "args": [
        Arg("channel", "text_channel_any"),
        Arg("text", "inf_str"),
    ],
    "flags": [
        "dev",
    ],
}

# Command Call
async def call(ctx):
    channel, text = ctx.args["channel"], ctx.args["text"]
    await channel.send(text)
