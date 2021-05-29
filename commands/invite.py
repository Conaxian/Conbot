################################################################

import sys

sys.path.append("..")

import cembed
import loclib

################################################################

async def invite(ctx):

    invite = await ctx.channel.create_invite(max_age=0, max_uses=0, unique=False)
    invite_link = loclib.Loc.member("label_invite_link", ctx.author)
    embed = cembed.get_cembed(ctx.msg, invite.url, invite_link, author_name=ctx.guild.name, author_img=ctx.guild.icon_url)
    await ctx.send(embed=embed)

################################################################
