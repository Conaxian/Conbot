################################################################

import sys
import num2words

sys.path.append("..")

import utils
import cembed
import loclib

################################################################

async def numeral(ctx):

    title = loclib.Loc.member("label_numeral", ctx.author)
    try:
        number = float(ctx.args["number"])
        numeral_str = num2words.num2words(number)
        numeral_str = numeral_str.title().replace("And", "and")
        embed = cembed.get_cembed(ctx.msg, f"```{numeral_str}```", title)
    except ValueError:
        text = loclib.Loc.member("err_invalid_number", ctx.author)
        embed = cembed.get_cembed(ctx.msg, text)

    await ctx.channel.send(embed=embed)

################################################################
