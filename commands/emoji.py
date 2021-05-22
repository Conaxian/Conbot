################################################################

import sys

sys.path.append("..")

import utils
import cembed
import cmdlib
import loclib

################################################################

async def emoji(ctx):

    name = ctx.args["name"].strip().lower()
    emoji = utils.get(ctx.client.emojis, name=name)
    if not emoji or not emoji.guild.get_member(ctx.author.id) or not emoji.available:
        raise cmdlib.CmdError("err_unknown_emoji")
    await ctx.channel.send(str(emoji))

################################################################
