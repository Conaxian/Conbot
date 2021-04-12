################################################################

import sys

sys.path.append("..")

import utils
import cembed
import loclib

################################################################

async def translate(ctx):

    translation, source, dest = await utils.translate_en(ctx.args["text"])

    text = loclib.Loc.member("text_translate", ctx.author)
    text.format(source, dest)
    text += f"\n\n```{translation.text}```"
    title = loclib.Loc.member("label_translate", ctx.author)

    embed = cembed.get_cembed(ctx.msg, text, title)
    await ctx.channel.send(embed=embed)

################################################################