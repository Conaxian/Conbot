################################################################

import sys

sys.path.append("..")

import utils
import cembed
import cmdlib
import loclib

################################################################

async def ban(ctx):

    target_id = utils.mention_id(ctx.args["target"])
    target = ctx.guild.get_member(target_id)

    if not target:
        raise cmdlib.CmdError("err_unknown_member", ctx.client.user.mention)
    if target.top_role >= ctx.author.top_role:
        raise cmdlib.CmdError("err_ban_perms_author")

    reason = loclib.Loc.member("text_ban_reason", ctx.author)
    reason.format(ctx.author)
    await target.ban(reason=str(reason))

    target_mention = f"<@!{target_id}>"
    text = loclib.Loc.member("text_ban_success", ctx.author)
    text.format(target_mention)

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.send(embed=embed)

################################################################
