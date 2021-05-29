################################################################

import sys

sys.path.append("..")

import const
import cembed
import conyaml
import loclib

################################################################

async def warns(ctx):

    warns = conyaml.get_warns(ctx.guild.id)
    warns = warns[-const.max_displayed_warns:]
    fields = []
    title = loclib.Loc.member("text_warns_title", ctx.author)
    title.format(ctx.guild.name)

    if len(warns) > 0:
        text = loclib.Loc.member("text_warns_last", ctx.author)
        text.format(const.max_displayed_warns)
        for warn in warns:
            member = ctx.guild.get_member(warn["member"])
            warn_desc = loclib.Loc.member("text_warns_desc", ctx.author)
            warn_datetime = warn["time"].split("-")
            warn_desc.format(warn["reason"], warn_datetime[0], warn_datetime[1])
            fields.append((member.display_name, warn_desc))
        embed = cembed.get_cembed(ctx.msg, text, title, author_name=ctx.guild.name, author_img=ctx.guild.icon_url, fields=fields)

    else:
        text = loclib.Loc.member("text_warns_none", ctx.author)
        embed = cembed.get_cembed(ctx.msg, text, title, author_name=ctx.guild.name, author_img=ctx.guild.icon_url)

    await ctx.reply(embed=embed)

################################################################
