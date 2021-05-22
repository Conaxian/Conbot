################################################################

import sys

sys.path.append("..")

import cembed
import loclib

################################################################

async def shutdown(ctx):

    text = loclib.Loc.member("text_exit", ctx.author)
    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

    def crash():
        try:
            crash()
        except:
            crash()
    crash()

################################################################
