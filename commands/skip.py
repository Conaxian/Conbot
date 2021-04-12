################################################################

import discord
import sys

sys.path.append("..")

import cembed
import loclib
import songlib

################################################################

async def skip(ctx):

    voices = ctx.client.voice_clients
    text = loclib.Loc.member("err_skip_not_playing", ctx.author)
    embed = cembed.get_cembed(ctx.msg, text)

    for voice in voices:
        if voice.guild == ctx.guild:
            song_amount = songlib.queue_length(ctx.guild)
            if song_amount >= 1:
                voice.stop()
                await songlib.shift_queue(ctx.guild)
                if song_amount - 1 >= 1:

                    path = songlib.get_song_path(voice.guild, 1)
                    song_name = path.split("$<|sep;|>")[1].replace(".mp3", "")

                    voice.play(discord.FFmpegPCMAudio(path))
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.25

                    text = loclib.Loc.server("text_play_playing", voice.guild)
                    text.format(song_name)
                    embed = cembed.get_embed(text)

    await ctx.channel.send(embed=embed)

################################################################