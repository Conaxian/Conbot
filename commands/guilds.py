################################################################

import sys

sys.path.append("..")

import cembed

################################################################

async def guilds(ctx):

    guild_names = [str(guild) for guild in ctx.client.guilds]
    text = "\n".join(guild_names)
    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.reply(embed=embed)

################################################################
