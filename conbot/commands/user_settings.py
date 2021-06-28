### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
from cmdtools import Arg
from conyaml import read_data
from cfglib import user_config
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "user-settings",
    "aliases": [
        "user-config",
        "user-options",
        "settings",
        "config",
        "options",
    ],
    "category": "config",
    "index": 0,
    "args": [
        Arg("[member]", "member"),
    ],
}

# Command Call
async def call(ctx):
    target = ctx.args["member"] or ctx.author
    fields = {}
    for config in user_config:
        name = Loc(f"config/name/{config.name}")
        value = read_data(f"user_config/{ctx.author.id}/{config.name}")
        value = config.display(value) or Loc("misc/none")
        fields[name] = value

    title = Loc("cmd/user_settings/title")
    embed = cembed(ctx, title=title, author={
        "name": target.name,
        "icon": target.avatar_url,
    }, fields=fields)
    await ctx.reply(embed=embed)
