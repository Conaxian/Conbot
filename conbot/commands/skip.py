### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import utils
from cmdtools import CmdError
from cembed import embed, cembed, tfooter
from loclib import Loc
from musiclib import queues, player_check

### Command

# Command Meta
meta = {
    "name": "skip",
    "category": "music",
    "index": 3,
}

# Command Call
async def call(ctx):
    voice = utils.get(ctx.bot.voice_clients, guild=ctx.guild)
    queue = queues.get(ctx.guild.id, [])
    if not voice or not queue:
        raise CmdError("cmd/queue/empty")

    voice.stop()
    name = utils.escape_md(queue[0].info["title"])
    text = Loc("cmd/skip/text").format(name)
    embed_ = cembed(ctx, text)
    await ctx.reply(embed=embed_)

    await player_check(ctx.bot.voice_clients)
    if not queue:
        text = Loc("cmd/queue/empty")
        embed_ = tfooter(embed(text.cstring(ctx.guild)))
        await ctx.send(embed=embed_)
