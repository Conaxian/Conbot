################################################################

import sys

sys.path.append("..")

import utils
import cembed
import loclib
import songlib

################################################################

async def leave(ctx):

    voice = utils.get(ctx.client.voice_clients, guild=ctx.guild)
    text = loclib.Loc.member("err_leave_no_voice", ctx.author)

    if voice:
        await voice.disconnect()
        songlib.queues.get(voice.guild.id, []).clear()
        text = loclib.Loc.member("text_leave", ctx.author)
        text.format(voice.channel)

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################
