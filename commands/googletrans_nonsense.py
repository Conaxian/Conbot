################################################################

import sys
import random
import googletrans

sys.path.append("..")

import utils
import cembed
import loclib

################################################################

async def googletrans_nonsense(ctx):

    codes = list(googletrans.LANGUAGES.keys())
    translation = utils.translate(ctx.args["text"], "en", random.choice(codes))
    for i in range(20):
        translation = utils.translate(translation.text, translation.dest, random.choice(codes))
    translation = utils.translate(translation.text, translation.dest, "en")

    text = loclib.Loc.member("text_translate", ctx.author)
    text.format("English", "Nonsense")
    text += f"\n\n```{translation.text}```"
    title = loclib.Loc.member("label_translate", ctx.author)

    embed = cembed.get_cembed(ctx.msg, text, title)
    await ctx.send(embed=embed)

################################################################
