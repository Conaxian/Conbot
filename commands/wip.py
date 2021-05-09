################################################################

import sys

sys.path.append("..")

import cembed
import loclib

################################################################

async def wip(ctx):

    text = loclib.Loc.member("text_wip", ctx.author)
    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################
