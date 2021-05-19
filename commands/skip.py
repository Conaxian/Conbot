################################################################

import sys

sys.path.append("..")

import utils
import cembed
import loclib
import songlib

################################################################

async def skip(ctx):

    voice = utils.get(ctx.client.voice_clients, guild=ctx.guild)
    text = loclib.Loc.member("err_empty_queue", ctx.author)
    embed = cembed.get_cembed(ctx.msg, text)

    if voice:
        queue = songlib.queues[ctx.guild.id]

        if len(queue) >= 1:
            voice.stop()
            text_skip = loclib.Loc.member("text_skip", ctx.author)
            text_skip.format(queue[0]["info"]["title"])
            embed_skip = cembed.get_cembed(ctx.msg, text_skip)
            await ctx.channel.send(embed=embed_skip)
            await songlib.player_check(ctx.client.voice_clients)
            if len(queue) >= 1:
                return

    await ctx.channel.send(embed=embed)

################################################################
