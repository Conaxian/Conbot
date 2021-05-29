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

    penis_str = f"8{'=' * random.randint(0, 10)}>"
    text = loclib.Loc.member("text_penis", ctx.author)
    text.format(target, penis_str)
    title = loclib.Loc.member("label_penis_length", ctx.author)

    embed = cembed.get_cembed(ctx.msg, text, title)
    await ctx.reply(embed=embed)

################################################################
