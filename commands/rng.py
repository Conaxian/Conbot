################################################################

import sys
import random

sys.path.append("..")

import cembed
import cmdlib
import loclib

################################################################

async def rng(ctx):

    try:
        min_num, max_num = ctx.args["min"], ctx.args["max"]
        min_num, max_num = int(min_num.strip(", ")), int(max_num.strip(", "))

        if min_num > max_num:
            raise cmdlib.CmdError("err_rng_range_larger")
        if min_num == max_num:
            raise cmdlib.CmdError("err_rng_range_equal")

    except ValueError:
        raise cmdlib.CmdError("err_rng_no_floats")
    
    number = random.randint(min_num, max_num)
    embed = cembed.get_cembed(ctx.msg, f"`{str(number)}`")
    await ctx.channel.send(embed=embed)

################################################################
