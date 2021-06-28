### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")

### Command

# Command Meta
meta = {
    "name": "invite",
    "category": "info",
    "index": 3,
}

# Command Call
async def call(ctx):
    invite = await ctx.channel.create_invite(unique=False)
    await ctx.reply(invite.url)
