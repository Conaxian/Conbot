### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import utils
from cmdtools import CmdError
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "join",
    "aliases": [
        "connect",
    ],
    "category": "music",
    "index": 0,
}

# Command Call
async def call(ctx):
    voice = ctx.author.voice
    if not voice:
        raise CmdError("cmd/join/no_voice")
    if utils.get(ctx.bot.voice_clients, guild=ctx.guild):
        raise CmdError("cmd/join/connected")

    await voice.channel.connect()
    channel_name = utils.escape_md(str(voice.channel))
    text = Loc("cmd/join/success").format(channel_name)
    embed = cembed(ctx, text)
    await ctx.reply(embed=embed)
