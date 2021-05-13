################################################################

import sys

sys.path.append("..")

import utils
import cembed
import loclib

################################################################

async def translate(ctx):

    src_lang = None
    words = ctx.args["text"].split()[0]
    first_word = ctx.args["text"].split()[0].strip("`")
    if len(first_word) == 2 and len(words) > 1:
        src_lang = first_word

    try:
        translation = utils.translate(ctx.args["text"][3:], src_lang if src_lang else ctx.args["text"])
    except ValueError:
        translation = utils.translate(ctx.args["text"])

    text = loclib.Loc.member("text_translate", ctx.author)
    text.format(translation.src, translation.dest)
    text += f"\n\n```{translation.text}```"
    title = loclib.Loc.member("label_translate", ctx.author)

    embed = cembed.get_cembed(ctx.msg, text, title)
    await ctx.channel.send(embed=embed)

################################################################
