################################################################

import sys
import random

sys.path.append("..")

import cembed
import loclib

################################################################

async def gay(ctx):

    target = ctx.args["target"]
    target = target if target else ctx.author.mention

    gayness = random.randint(0, 100)
    text = loclib.Loc.member("text_gay", ctx.author)
    text.format(target, gayness)
    title = loclib.Loc.member("label_gay_meter", ctx.author)

    embed = cembed.get_cembed(ctx.msg, text, title)
    await ctx.send(embed=embed)

################################################################
