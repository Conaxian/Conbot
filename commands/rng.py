################################################################

import sys
import random

sys.path.append("..")

import cembed
import loclib

################################################################

async def rng(ctx):

    try:
        min_num, max_num = ctx.args["min"], ctx.args["max"]
        min_num, max_num = int(min_num.strip(", ")), int(max_num.strip(", "))
        text = ""
        if min_num > max_num:
            text = loclib.Loc.member("err_rng_range_larger", ctx.author)
        if min_num == max_num:
            text = loclib.Loc.member("err_rng_range_equal", ctx.author)

    except ValueError:
        text = loclib.Loc.member("err_rng_no_floats", ctx.author)

    if text != "":
        embed = cembed.get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return
    
    number = random.randint(min_num, max_num)
    embed = cembed.get_cembed(ctx.msg, str(number))
    await ctx.channel.send(embed=embed)

################################################################
