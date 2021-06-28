### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import utils
from cmdtools import CmdError
from cembed import cembed
from loclib import Loc
from musiclib import queues

### Command

# Command Meta
meta = {
    "name": "leave",
    "aliases": [
        "disconnect",
        "dc",
        "quit",
    ],
    "category": "music",
    "index": 1,
}

# Command Call
async def call(ctx):
    voice = utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    if not voice:
        raise CmdError("cmd/leave/no_voice")

    await voice.disconnect()
    queues.get(voice.guild.id, []).clear()
    channel_name = utils.escape_md(str(voice.channel))
    text = Loc("cmd/leave/success").format(channel_name)
    embed = cembed(ctx, text)
    await ctx.reply(embed=embed)
