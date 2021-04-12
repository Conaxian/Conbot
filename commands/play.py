################################################################

import discord
import sys

sys.path.append("..")

import cembed
import loclib
import songlib

################################################################

async def play(ctx):

    voice = ctx.author.voice

    if not voice:
        text = loclib.Loc.member("err_join_no_voice", ctx.author)
        embed = cembed.get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return
    
    else:
        for bot_voice in ctx.client.voice_clients:
            if bot_voice.guild == ctx.guild:
                break

        else:
            await voice.channel.connect()
            text = loclib.Loc.member("text_join", ctx.author)
            text.format(voice.channel)
            embed = cembed.get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)

    voices = ctx.client.voice_clients

    for voice in voices:
        if voice.guild == ctx.guild:
            text = loclib.Loc.member("text_play_downloading", ctx.author)
            embed = cembed.get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)
            position = songlib.queue_length(ctx.guild) + 1
            await songlib.download_song(ctx.guild, ctx.args["song"], position)

    songlib.play_text_output[ctx.guild.id] = ctx.channel
    path = songlib.get_song_path(ctx.guild, position)
    song_name = path.split("$<|sep;|>")[1].replace(".mp3", "")

    if songlib.queue_length(ctx.guild) == 1:
        voice.play(discord.FFmpegPCMAudio(path))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.25

        text = loclib.Loc.server("text_play_playing", ctx.guild)
        text.format(song_name)

    else:
        text = loclib.Loc.server("text_play_add_queue", ctx.guild)
        text.format(song_name)

    embed = cembed.get_embed(text)
    await ctx.channel.send(embed=embed)

################################################################