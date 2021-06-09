################################################################

import sys

sys.path.append("..")

import utils
import cembed
import conyaml
import cmdlib
import loclib

################################################################

async def mute(ctx):

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
        raise cmdlib.CmdError("err_mute_no_role")
    if mute_role >= ctx.guild.me.top_role:
        raise cmdlib.BotPermsError()
    if conyaml.is_muted(ctx.guild.id, target.id):
        raise cmdlib.CmdError("err_mute_member_muted", target_mention)

    reason = loclib.Loc.server("text_mute_reason", ctx.guild)
    reason.format(ctx.author)
    target_roles = list(filter(utils.is_role_normal, target.roles))

    await target.remove_roles(*target_roles, reason=str(reason))
    await target.add_roles(mute_role)
    role_ids = [role.id for role in target_roles]
    conyaml.add_mute(ctx.guild.id, target.id, role_ids)

    text = loclib.Loc.member("text_mute_success", ctx.author)
    text.format(target_mention)

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.reply(embed=embed)

################################################################
