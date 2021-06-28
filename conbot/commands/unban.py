### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
from cmdtools import Arg, CmdError
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "unban",
    "aliases": [
        "pardon",
    ],
    "category": "mod",
    "index": 2,
    "args": [
        Arg("<target>", "banned_user"),
    ],
    "perms": [
        "ban_members",
    ],
}

# Command Call
async def call(ctx):
    target = ctx.args["target"]
    reason = Loc("cmd/unban/reason").format(ctx.author)
    await ctx.guild.unban(target,
        reason=reason.cstring(ctx.guild))

    text = Loc("cmd/unban/success").format(target.mention)
    embed = cembed(ctx, text)
    await ctx.reply(embed=embed)
