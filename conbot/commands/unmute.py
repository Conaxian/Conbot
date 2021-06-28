### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import utils
from cmdtools import Arg, CmdError, BotPermsError
from conyaml import read_data, write_data
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "unmute",
    "category": "mod",
    "index": 4,
    "args": [
        Arg("<target>", "member"),
    ],
    "perms": [
        "manage_messages",
    ],
}

# Command Call
async def call(ctx):
    target = ctx.args["target"]
    mute_role_id = read_data("guild_config/" + \
        str(ctx.guild.id)).mute_role
    mute_role = ctx.guild.get_role(mute_role_id)

    if target.top_role >= ctx.author.top_role:
        raise CmdError("cmd/unmute/no_perms")
    if not mute_role:
        raise CmdError("cmd/mute/no_mute_role", ctx.prefix)
    if mute_role >= ctx.guild.me.top_role:
        raise BotPermsError
    mute = read_data(f"mutes/{ctx.guild.id}/{target.id}")
    if not mute:
        raise CmdError("cmd/unmute/not_muted", target.mention)

    reason = Loc("cmd/unmute/reason").format(ctx.author)
    original_roles = [ctx.guild.get_role(role_id)
        for role_id in mute.roles]
    await target.add_roles(*original_roles,
        reason=reason.cstring(ctx.guild))
    await target.remove_roles(mute_role,
        reason=reason.cstring(ctx.guild))
    mutes = read_data("mutes")
    mutes[ctx.guild.id].pop(str(target.id))
    write_data("mutes", mutes)

    text = Loc("cmd/unmute/success").format(target.mention)
    embed = cembed(ctx, text)
    await ctx.reply(embed=embed)
