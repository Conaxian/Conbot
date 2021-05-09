################################################################

import sys

sys.path.append("..")

import constants
import cembed
import loclib

################################################################

async def about(ctx):

    text = loclib.Loc.member("text_about", ctx.author)
    text.format(constants.conax_discord_tag)
    title = loclib.Loc.member("label_about", ctx.author)
    title_bot_invite = loclib.Loc.member("label_bot_invite", ctx.author)
    title_github = loclib.Loc.member("label_github", ctx.author)
    fields = {title_bot_invite: constants.bot_invite_url, title_github: constants.bot_github_url}
    embed = cembed.get_cembed(ctx.msg, text, title, fields=fields, inline=True)
    await ctx.channel.send(embed=embed)

################################################################
