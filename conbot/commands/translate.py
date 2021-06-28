### Imports

# Standard Library
import sys

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
    "name": "translate",
    "category": "tools",
    "aliases": [
        "trans",
    ],
    "index": 1,
    "args": [
        Arg("[src]", "lang_opt"),
        Arg("[dest]", "lang_opt"),
        Arg("<text>", "inf_str"),
    ],
}

# Command Call
async def call(ctx):
    original = ctx.args["text"]
    kwargs = {}
    if ctx.args["src"]: kwargs["src"] = ctx.args["src"]
    if ctx.args["dest"]: kwargs["dest"] = ctx.args["dest"]
    translate = lambda: translator.translate(original, **kwargs)
    translation = await ctx.bot.async_exec(translate)

    src = LANGUAGES[translation.src].capitalize()
    dest = LANGUAGES[translation.dest].capitalize()
    text = Loc("cmd/translate/text").format(src, dest)
    text = utils.embed_desc_constrain(
        translation.text,
        text.cstring(ctx) + "\n\n```",
        "```",
    )
    title = Loc("cmd/translate/title")
    embed = cembed(ctx, text, title=title)
    await ctx.reply(embed=embed)
