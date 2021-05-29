################################################################

import sys

sys.path.append("..")

import utils
import cembed
import cmdlib
import loclib

################################################################

async def join(ctx):

    voice = ctx.author.voice

    if not voice:
        raise cmdlib.CmdError("err_join_no_voice")

    if utils.get(ctx.client.voice_clients, guild=ctx.guild):
        raise cmdlib.CmdError("err_join_voice_connected")

    else:
        await voice.channel.connect()
        text = loclib.Loc.member("text_join", ctx.author)
        text.format(voice.channel)

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.reply(embed=embed)

################################################################
