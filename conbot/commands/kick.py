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
    "name": "kick",
    "category": "mod",
    "index": 0,
    "args": [
        Arg("<target>", "member"),
    ],
    "perms": [
        "kick_members",
    ],
}

# Command Call
async def call(ctx):
    target = ctx.args["target"]
    if target.top_role >= ctx.author.top_role:
        raise CmdError("cmd/kick/no_perms")
    reason = Loc("cmd/kick/reason").format(ctx.author)
    await target.kick(reason=reason.cstring(ctx.guild))

    text = Loc("cmd/kick/success").format(target.mention)
    embed = cembed(ctx, text)
    await ctx.reply(embed=embed)
