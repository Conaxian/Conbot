################################################################

import sys
import datetime

sys.path.append("..")

import utils
import cembed
import cmdlib
import loclib

################################################################

async def avatar(ctx):

    if not ctx.args["member"]:
        member = ctx.guild.get_member(ctx.author.id)
    else:
        member_id = utils.mention_id(ctx.args["member"])
        member = ctx.guild.get_member(member_id)
        if not member:
            raise cmdlib.CmdError("err_unknown_member", ctx.client.user.mention)

    embed = cembed.get_cembed(ctx.msg, image=member.avatar_url, author_name=member.name, author_img=member.avatar_url)
    await ctx.channel.send(embed=embed)

################################################################
