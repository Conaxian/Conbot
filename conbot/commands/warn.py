### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
from utils import date, time, escape_md
from cmdtools import Arg, CmdError
from conyaml import read_data, write_data
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "warn",
    "category": "mod",
    "index": 5,
    "args": [
        Arg("<target>", "member"),
        Arg("[reason]", "inf_str")
    ],
    "perms": [
        "manage_messages",
    ],
}

# Command Call
async def call(ctx):
    target = ctx.args["target"]
    reason = escape_md(ctx.args["reason"]) or "Unspecified"
    if target.top_role >= ctx.author.top_role:
        raise CmdError("cmd/warn/no_perms")

    data = read_data(f"warns/{ctx.guild.id}")
    warn_indices = [int(index) for index in data.keys()]
    warn_index = max(warn_indices or (-1,)) + 1
    warn = {
        "member": str(target.id),
        "reason": reason,
        "time": f"{date()}-{time()}",
    }
    write_data(f"warns/{ctx.guild.id}/{warn_index}", warn)

    text = Loc("cmd/warn/success").format(target.mention, reason)
    embed = cembed(ctx, text)
    await ctx.reply(embed=embed)
