################################################################

import discord
import sys

sys.path.append("..")

import utils
import cembed
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
        for user in banned_users:
            if user.id == target_id:
                target = user
                break

    if not target:
        text = loclib.Loc.member("err_unknown_user", ctx.author)
        text.format(ctx.client.user.id)
    if text:
        embed = cembed.get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return

    reason = loclib.Loc.member("text_unban_reason", ctx.author)
    reason.format(ctx.author)
    try:
        await ctx.guild.unban(target, reason=str(reason))
    except discord.errors.NotFound:
        text = loclib.Loc.member("text_unban_not_found", ctx.author)
    if not text:
        text = loclib.Loc.member("text_unban_success", ctx.author)

    target_mention = f"<@!{target_id}>"
    text.format(target_mention)
    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################
