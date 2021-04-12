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
    gay_percent = random.randint(0, 100)
    gay_text = loclib.Loc.member("text_gay", ctx.author)
    gay_text.format(target, gay_percent)
    gay_meter = loclib.Loc.member("label_gay_meter", ctx.author)
    embed = cembed.get_cembed(ctx.msg, gay_text, gay_meter)
    await ctx.channel.send(embed=embed)

################################################################