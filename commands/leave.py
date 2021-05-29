################################################################

import sys

sys.path.append("..")

import utils
import cembed
import loclib
import cmdlib
import songlib

################################################################

async def leave(ctx):

    voice = utils.get(ctx.client.voice_clients, guild=ctx.guild)

    if voice:
        await voice.disconnect()
        songlib.queues.get(voice.guild.id, []).clear()
        text = loclib.Loc.member("text_leave", ctx.author)
        text.format(voice.channel)
    else:
        raise cmdlib.CmdError("err_leave_no_voice")

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.send(embed=embed)

################################################################
