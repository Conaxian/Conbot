################################################################

import discord
import sys

sys.path.append("..")

import utils
import cembed
import cmdlib
import loclib

################################################################

async def unban(ctx):

    target_id = utils.mention_id(ctx.args["target"])
    target = ctx.guild.get_member(target_id)
    bans = await ctx.guild.bans()
    banned_users = [ban.user for ban in bans]
    text = ""

    if not target:
        target = utils.get(banned_users, id=target_id)
        if not target:
            raise cmdlib.CmdError("err_unknown_user", ctx.client.user.id)

    reason = loclib.Loc.member("text_unban_reason", ctx.author)
    reason.format(ctx.author)
    try:
        await ctx.guild.unban(target, reason=str(reason))
        text = loclib.Loc.member("text_unban_success", ctx.author)
    except discord.errors.NotFound:
        text = loclib.Loc.member("text_unban_not_found", ctx.author)

    target_mention = f"<@!{target_id}>"
    text.format(target_mention)
    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.send(embed=embed)

################################################################
