################################################################

import sys
import random

sys.path.append("..")

import cembed
import loclib

################################################################

async def choice(ctx):

    delimiter = ","
    choices = ctx.args["choices"].split(delimiter)
    choices = list(filter(None, choices))
    if len(choices) < 2:
        text = loclib.Loc.member("err_choice_not_enough", ctx.author)
        text.format(delimiter)
    else:
        text = random.choice(choices)
    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################