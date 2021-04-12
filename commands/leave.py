################################################################

import os
import sys

sys.path.append("..")

import constants
import cembed
import loclib

################################################################

async def leave(ctx):

    voices = ctx.client.voice_clients
    text = loclib.Loc.member("err_leave_no_voice", ctx.author)

    for voice in voices:
        if voice.guild == ctx.guild:
            path = f"{constants.song_dir}/{voice.guild.id}"
            await voice.disconnect()
            os.system(f"rm -rf {path}")
            
            text = loclib.Loc.member("text_leave", ctx.author)
            text.format(voice.channel)

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################