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
    too_large = False

    try:
        number = float(ctx.args["number"])
        try:
            numeral_str = num2words.num2words(number)
            numeral_str = numeral_str.title().replace("And", "and")
            too_large = len(numeral_str) > 2047
            embed = cembed.get_cembed(ctx.msg, numeral_str, title)
        except OverflowError:
            too_large = True
    except ValueError:
        text = loclib.Loc.member("err_invalid_number", ctx.author)
        embed = cembed.get_cembed(ctx.msg, text)

    if too_large:
        text = loclib.Loc.member("err_number_too_large", ctx.author)
        embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################
