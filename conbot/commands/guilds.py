### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
from cembed import cembed

### Command

# Command Meta
meta = {
    "name": "guilds",
    "aliases": [
        "servers",
    ],
    "category": "dev",
    "flags": [
        "dev",
    ],
}

# Command Call
async def call(ctx):
    guilds = [str(guild) for guild in ctx.bot.guilds]
    text = "\n".join(guilds)
    embed = cembed(ctx, text)
    await ctx.reply(embed=embed)
