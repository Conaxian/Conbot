################################################################

import sys

sys.path.append("..")

import cembed
import loclib
import songlib

################################################################

async def skip(ctx):

    voices = ctx.client.voice_clients
    text = loclib.Loc.member("err_empty_queue", ctx.author)
    embed = cembed.get_cembed(ctx.msg, text)

    for voice in voices:
        if voice.guild == ctx.guild:
            queue = songlib.queues[ctx.guild.id]

            if len(queue) >= 1:
                voice.stop()

                text_skip = loclib.Loc.member("text_skip", ctx.author)
                text_skip.format(queue[0]["info"]["title"])
                embed_skip = cembed.get_cembed(ctx.msg, text_skip)
                await ctx.channel.send(embed=embed_skip)

            break

    await ctx.channel.send(embed=embed)

################################################################
