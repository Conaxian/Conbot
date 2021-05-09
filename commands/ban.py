################################################################

import sys

sys.path.append("..")

import utils
import cembed
import loclib

################################################################

async def ban(ctx):

    target_id = utils.mention_id(ctx.args["target"])
    target = ctx.guild.get_member(target_id)
    text = ""

    if not target:
        text = loclib.Loc.member("err_unknown_member", ctx.author)
        text.format(ctx.client.user.mention)
    elif target.top_role >= ctx.author.top_role:
        text = loclib.Loc.member("err_ban_perms_author", ctx.author)
    if text != "":
        embed = cembed.get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return

    reason = loclib.Loc.member("text_ban_reason", ctx.author)
    reason.format(ctx.author)
    await target.ban(reason=str(reason))
    text = loclib.Loc.member("text_ban_success", ctx.author)
    target_mention = f"<@!{target_id}>"
    text.format(target_mention)

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################
