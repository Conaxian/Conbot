################################################################

import sys

sys.path.append("..")

import utils
import cembed
import loclib

################################################################

async def emoji(ctx):

    name = ctx.args["name"].strip().lower()
    emoji = utils.get(ctx.client.emojis, name=name)
    if not emoji or not emoji.guild.get_member(ctx.author.id) or not emoji.available:
        text = loclib.Loc.member("err_unknown_emoji", ctx.author)
        embed = cembed.get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return
    await ctx.channel.send(str(emoji))

################################################################
