################################################################

import sys
import time

sys.path.append("..")

import cembed
import loclib
import songlib

################################################################

async def queue(ctx):

    queue = songlib.queues.get(ctx.guild.id, [])
    title = loclib.Loc.member("label_queue", ctx.author)

    if len(queue) <= 0:
        text = loclib.Loc.member("err_empty_queue", ctx.author)
        embed = cembed.get_cembed(ctx.msg, text, title, author_name=ctx.guild.name, author_img=ctx.guild.icon_url)

    else:
        fields = []
        for song in queue:
            song_name = song["info"]["title"]
            song_desc = loclib.Loc.member("text_queue_song", ctx.author)
            song_requestor = f"<@!{song['context'].author.id}>"
            song_duration = time.strftime("%H:%M:%S", time.gmtime(song["info"]["duration"]))
            song_desc.format(song_requestor, song_duration)
            fields.append((song_name, song_desc))

        embed = cembed.get_cembed(ctx.msg, title=title, author_name=ctx.guild.name, author_img=ctx.guild.icon_url, fields=fields)

    await ctx.send(embed=embed)

################################################################
