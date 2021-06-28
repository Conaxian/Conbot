### Imports

# Standard Library
import sys
from time import gmtime, strftime

# Conbot Modules
sys.path.append("..")
import const
import utils
from cembed import cembed
from loclib import Loc
from musiclib import queues

### Command

# Command Meta
meta = {
    "name": "queue",
    "aliases": [
        "songs",
        "song-list",
        "music-list",
    ],
    "category": "music",
    "index": 4,
}

# Command Call
async def call(ctx):
    queue = queues.get(ctx.guild.id, [])
    title = Loc("cmd/queue/title")

    if not queue:
        text = Loc("cmd/queue/empty")
        embed = cembed(ctx, text, title=title, author={
            "name": ctx.guild.name,
            "icon": ctx.guild.icon_url,
        })

    else:
        fields = []
        for audio in queue:
            name = utils.escape_md(audio.info["title"])
            entry = Loc("cmd/queue/entry")
            requestor = audio.ctx.author.mention
            duration = strftime(const.time_format_sec,
                gmtime(audio.info["duration"]))
            entry.format(requestor, duration)
            fields.append((name, entry))
        embed = cembed(ctx, title=title, author={
            "name": ctx.guild.name,
            "icon": ctx.guild.icon_url,
        }, fields=fields)

    await ctx.reply(embed=embed)
