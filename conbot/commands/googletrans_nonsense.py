### Imports

# Standard Library
import sys
from random import choice

# Dependencies
from googletrans import Translator, LANGUAGES

# Conbot Modules
sys.path.append("..")
import utils
from cmdtools import Arg
from cembed import cembed
from loclib import Loc

### Initialization

# Translator
translator = Translator()

### Command

# Command Meta
meta = {
    "name": "googletrans-nonsense",
    "category": "dev",
    "args": [
        Arg("<text>", "inf_str"),
    ],
    "flags": [
        "dev",
    ],
}

# Command Call
async def call(ctx):
    original = ctx.args["text"]
    codes = tuple(LANGUAGES.keys())
    text, src, dest = original, "auto", choice(codes)

    for i in range(20):
        translate = lambda: translator.translate(text, src=src, dest=dest)
        translation = await ctx.bot.async_exec(translate)
        text = translation.text
        src, dest = translation.dest, choice(codes)

    translate = lambda: translator.translate(
        translation.text, src=translation.dest, dest="en")
    translation = await ctx.bot.async_exec(translate)

    text = Loc("cmd/translate/text").format("English", "Nonsense")
    text = utils.embed_desc_constrain(
        translation.text,
        text.cstring(ctx) + "\n\n```",
        "```",
    )
    title = Loc("cmd/translate/title")
    embed = cembed(ctx, text, title=title)
    await ctx.reply(embed=embed)
