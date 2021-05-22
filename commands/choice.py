################################################################

import sys
import random

sys.path.append("..")

import cembed
import cmdlib
import loclib

################################################################

async def choice(ctx):

    delimiter = ","
    choices = ctx.args["choices"].split(delimiter)
    choices = map(str.strip, choices)
    choices = list(filter(None, choices))

    if len(choices) < 2:
        raise cmdlib.CmdError("err_choice_not_enough", delimiter)
    else:
        text = random.choice(choices)

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################
