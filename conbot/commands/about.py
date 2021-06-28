### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import const
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "about",
    "aliases": [
        "conbot",
        "github",
        "version",
    ],
    "category": "info",
    "index": 1,
}

# Command Call
async def call(ctx):
    name, tag = const.author.split("#")
    text = Loc("cmd/about/text").format(name, tag)
    about = Loc("cmd/about/about")
    bot_invite = Loc("cmd/about/bot_invite")
    github = Loc("cmd/about/github")
    version = Loc("cmd/about/version")

    fields = {
        bot_invite: const.bot_invite,
        github: const.bot_github,
        version: f"**`v{const.version}`**",
    }
    embed = cembed(ctx, text, title=about, fields=fields, inline=True)
    await ctx.reply(embed=embed)
