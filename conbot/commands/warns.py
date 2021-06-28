### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import const
from conyaml import read_data
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "warns",
    "category": "mod",
    "aliases": [
        "warnings",
        "warn-list",
    ],
    "index": 6,
}

# Command Call
async def call(ctx):
    warns = list(read_data(f"warns/{ctx.guild.id}").values()) \
        [-const.max_warns_shown:]
    fields = []
    title = Loc("cmd/warns/title").format(ctx.guild.name)

    if warns:
        text = Loc("cmd/warns/last").format(const.max_warns_shown)
        for warn in warns:
            member = ctx.guild.get_member(int(warn["member"]))
            entry = Loc("cmd/warns/entry") \
                .format(warn["reason"], *warn["time"].split("-"))
            fields.append((str(member), entry))
    else:
        text = Loc("cmd/warns/none")

    embed = cembed(ctx, text, title=title, author={
        "name": ctx.guild.name,
        "icon": ctx.guild.icon_url,
    }, fields=fields)
    await ctx.reply(embed=embed)
