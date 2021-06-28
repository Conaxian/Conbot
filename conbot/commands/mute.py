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
    "name": "mute",
    "category": "mod",
    "index": 3,
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
        raise CmdError("cmd/mute/no_perms")
    if not mute_role:
        raise CmdError("cmd/mute/no_mute_role", ctx.prefix)
    if mute_role >= ctx.guild.me.top_role:
        raise BotPermsError
    if read_data(f"mutes/{ctx.guild.id}/{target.id}"):
        raise CmdError("cmd/mute/muted", target.mention)

    reason = Loc("cmd/mute/reason").format(ctx.author)
    target_roles = list(filter(utils.is_role_normal, target.roles))
    await target.remove_roles(*target_roles,
        reason=reason.cstring(ctx.guild))
    await target.add_roles(mute_role,
        reason=reason.cstring(ctx.guild))
    role_ids = [role.id for role in target_roles]
    mute = {"roles": role_ids}
    write_data(f"mutes/{ctx.guild.id}/{target.id}", mute)

    text = Loc("cmd/mute/success").format(target.mention)
    embed = cembed(ctx, text)
    await ctx.reply(embed=embed)
