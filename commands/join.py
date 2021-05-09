################################################################

import sys

sys.path.append("..")

import utils
import cembed
import loclib

################################################################

async def join(ctx):

    voice = ctx.author.voice

    if not voice:
        text = loclib.Loc.member("err_join_no_voice", ctx.author)

    if utils.get(ctx.client.voice_clients, guild=ctx.guild):
        text = loclib.Loc.member("err_join_voice_connected", ctx.author)

    else:
        await voice.channel.connect()
        text = loclib.Loc.member("text_join", ctx.author)
        text.format(voice.channel)

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################
