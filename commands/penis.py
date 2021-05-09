################################################################

import sys
import random

sys.path.append("..")

import cembed
import loclib

################################################################

async def penis(ctx):

    target = ctx.args["target"]
    target = target if target else ctx.author.mention
    penis = f"8{'=' * random.randint(0, 10)}>"
    penis_text = loclib.Loc.member("text_penis", ctx.author)
    penis_text.format(target, penis)
    penis_length = loclib.Loc.member("label_penis_length", ctx.author)
    embed = cembed.get_cembed(ctx.msg, penis_text, penis_length)
    await ctx.channel.send(embed=embed)

################################################################
