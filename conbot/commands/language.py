### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import const
from cmdtools import Arg
from conyaml import write_data
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "language",
    "aliases": [
        "languages",
        "lang",
    ],
    "category": "config",
    "index": 2,
    "args": [
        Arg("[language]", "loc_lang"),
    ],
}

# Command Call
async def call(ctx):
    lang = ctx.args["language"]

    if not lang:
        text = Loc("cmd/language/list")
        title = Loc("cmd/language/languages")
        fields = {}
        for language in const.languages:
            name = Loc("meta/name").string(language)
            fields[name] = f"`{language.replace('_', '-')}`"
        embed = cembed(ctx, text, title=title, fields=fields)

    else:
        write_data(f"user_config/{ctx.author.id}/language", lang)
        name = Loc("meta/name").string(lang)
        text = Loc("cmd/language/changed").format(name)
        embed = cembed(ctx, text.string(lang))

    await ctx.reply(embed=embed)
