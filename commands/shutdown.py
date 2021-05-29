################################################################

import sys

sys.path.append("..")

import cembed
import loclib

################################################################

async def shutdown(ctx):

    text = loclib.Loc.member("text_exit", ctx.author)
    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.reply(embed=embed)
    await ctx.client.close()

################################################################
