################################################################

import sys

sys.path.append("..")

import utils
import cembed
import conyaml
import cmdlib
import loclib

################################################################

async def unmute(ctx):

    target_id = utils.mention_id(ctx.args["target"])
    target = ctx.guild.get_member(target_id)
    target_mention = f"<@!{target_id}>"
    mute_role_id = conyaml.read_server_config(ctx.guild.id, "mute_role")
    mute_role = ctx.guild.get_role(mute_role_id)

    if not target:
        raise cmdlib.CmdError("err_unknown_member", ctx.client.user.mention)
    if target.top_role >= ctx.author.top_role:
        raise cmdlib.CmdError("err_mute_perms_author")
    if not mute_role:
        raise cmdlib.CmdError("err_no_mute_role", ctx.prefix)
    if mute_role >= ctx.guild.me.top_role:
        raise cmdlib.BotPermsError()
    mute_data = conyaml.get_mute(ctx.guild.id, target.id)
    if not mute_data:
        raise cmdlib.CmdError("err_unmute_member_not_muted", target_mention)

    reason = loclib.Loc.server("text_unmute_reason", ctx.guild)
    reason.format(ctx.author)
    original_roles = [ctx.guild.get_role(role_id)
        for role_id in mute_data["roles"]]

    await target.add_roles(*original_roles, reason=str(reason))
    await target.remove_roles(mute_role, reason=str(reason))
    conyaml.remove_mute(ctx.guild.id, target.id)

    text = loclib.Loc.member("text_unmute_success", ctx.author)
    text.format(target_mention)

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.reply(embed=embed)

################################################################
