################################################################

import sys
import num2words

sys.path.append("..")

import cembed
import cmdlib
import loclib

################################################################

async def numeral(ctx):

    try:
        number = float(ctx.args["number"])

        try:
            numeral_str = num2words.num2words(number)
            numeral_str = numeral_str.title().replace("And", "and")
            if len(numeral_str) > 2047:
                raise cmdlib.CmdError("err_number_too_large")
            title = loclib.Loc.member("label_numeral", ctx.author)
            embed = cembed.get_cembed(ctx.msg, numeral_str, title)

        except OverflowError:
            raise cmdlib.CmdError("err_number_too_large")
    except ValueError:
        raise cmdlib.CmdError("err_invalid_number")

    await ctx.channel.send(embed=embed)

################################################################
