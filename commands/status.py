################################################################

import sys

sys.path.append("..")

import cembed
import loclib

################################################################

async def status(ctx):

    online_msg = loclib.Loc.member("text_status_online", ctx.author)
    embed = cembed.get_cembed(ctx.msg, online_msg)
    await ctx.channel.send(embed=embed)

################################################################
