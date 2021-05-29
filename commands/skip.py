################################################################

import sys

sys.path.append("..")

import utils
import cembed
import cmdlib
import loclib
import songlib

################################################################

async def skip(ctx):

    voice = utils.get(ctx.client.voice_clients, guild=ctx.guild)

    if voice:
        queue = songlib.queues[ctx.guild.id]

        if len(queue) >= 1:
            voice.stop()
            text = loclib.Loc.member("text_skip", ctx.author)
            text.format(queue[0]["info"]["title"])
            embed = cembed.get_cembed(ctx.msg, text)
            await ctx.reply(embed=embed)
            await songlib.player_check(ctx.client.voice_clients)
            if len(queue) < 1:
                text = loclib.Loc.server("err_empty_queue", ctx.guild)
                embed = cembed.get_embed(text)
                await ctx.send(embed=embed)
            return

    raise cmdlib.CmdError("err_empty_queue")

################################################################
