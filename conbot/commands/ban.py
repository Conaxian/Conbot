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
    "name": "ban",
    "category": "mod",
    "index": 1,
    "args": [
        Arg("<target>", "member"),
    ],
    "perms": [
        "ban_members",
    ],
}

# Command Call
async def call(ctx):
    target = ctx.args["target"]
    if target.top_role >= ctx.author.top_role:
        raise CmdError("cmd/ban/no_perms")
    reason = Loc("cmd/ban/reason").format(ctx.author)
    await target.ban(reason=reason.cstring(ctx.guild))

    text = Loc("cmd/ban/success").format(target.mention)
    embed = cembed(ctx, text)
    await ctx.reply(embed=embed)
