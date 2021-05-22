################################################################

import sys

sys.path.append("..")

import const
import utils
import cembed
import cmdlib
import loclib
import songlib

################################################################

async def play(ctx):

    voice = ctx.author.voice

    if not voice:
        raise cmdlib.CmdError("err_join_no_voice")

    else:
        if not utils.get(ctx.client.voice_clients, guild=ctx.guild):
            await voice.channel.connect()
            text = loclib.Loc.member("text_join", ctx.author)
            text.format(voice.channel)
            embed = cembed.get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)

    if len(songlib.queues.get(ctx.guild.id, [])) >= const.song_queue_limit:
        text = loclib.Loc.member("text_max_queue_length", ctx.author)
        text.format(const.song_queue_limit)
        embed = cembed.get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return

    voice = utils.get(ctx.client.voice_clients, guild=ctx.guild)
    text = None
    song_url = await songlib.yt_search(ctx.args["song"])

    if not song_url:
        raise cmdlib.CmdError("err_play_unknown_song")

    else:
        song, info = await songlib.get_song(song_url, ctx.client.loop)
        if not song:
            max_length = const.song_max_length / 60
            max_length = str(round(max_length, 2)).rstrip("0").rstrip(".")
            raise cmdlib.CmdError("err_play_too_long", max_length)

    if text:
        embed = cembed.get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return

    if ctx.guild.id in songlib.queues.keys() and songlib.queues[ctx.guild.id]:
        songlib.queues[ctx.guild.id].append({"song": song, "info": info, "context": ctx, "playing": False})
        text = loclib.Loc.server("text_play_add_queue", ctx.guild)
    else:
        song = {"song": song, "info": info, "context": ctx, "playing": False}
        songlib.queues[ctx.guild.id] = [song]
        await songlib.play_song(voice, song)
        text = loclib.Loc.server("text_play_playing", ctx.guild)

    text.format(info["title"])
    embed = cembed.get_embed(text)
    await ctx.channel.send(embed=embed)

################################################################
