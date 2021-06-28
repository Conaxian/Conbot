### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import const
from cmdtools import Arg
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "perms",
    "aliases": [
        "perm",
        "permissions",
        "permission",
    ],
    "category": "info",
    "index": 4,
    "args": [
        Arg("[member]", "member"),
    ],
}

# Command Call
async def call(ctx):
    member = ctx.args["member"] or ctx.author
    perms = member.guild_permissions
    yes = Loc("misc/yes").cstring(ctx)
    no = Loc("misc/no").cstring(ctx)
    fields = {}

    for permissions in const.permissions.values():
        for perm in permissions:
            name = Loc(f"perm/{perm}")
            enabled = f"**[{yes}]" if getattr(perms, perm) \
                else f"**[{no}]"
            enabled += ("(https://discord.com/developers/"
            "docs/topics/permissions)**")
            fields[name] = enabled

    text = Loc("cmd/perms/text").format(member.mention)
    title = Loc("cmd/perms/title").format(ctx.guild.name)
    embed = cembed(ctx, text, title=title, author={
        "name": member.name,
        "icon": member.avatar_url,
    }, fields=fields, inline=True)
    await ctx.reply(embed=embed)
