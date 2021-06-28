### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
from cmdtools import Arg
from cembed import cembed

### Command

# Command Meta
meta = {
    "name": "avatar",
    "aliases": [
        "profile-pic",
        "pfp",
    ],
    "category": "info",
    "index": 5,
    "args": [
        Arg("[member]", "member"),
    ],
}

# Command Call
async def call(ctx):
    member = ctx.args["member"] or ctx.author
    embed = cembed(ctx, image=member.avatar_url, author={
        "name": member.name,
        "icon": member.avatar_url,
    })
    await ctx.reply(embed=embed)
