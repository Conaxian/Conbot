################################################################

import sys

sys.path.append("..")

import const
import cembed
import loclib

################################################################

async def about(ctx):

    text = loclib.Loc.member("text_about", ctx.author)
    text.format(const.conax_discord_tag)
    title = loclib.Loc.member("label_about", ctx.author)
    title_bot_invite = loclib.Loc.member("label_bot_invite", ctx.author)
    title_github = loclib.Loc.member("label_github", ctx.author)
    title_version = loclib.Loc.member("label_version", ctx.author)

    fields = {
        title_bot_invite: const.bot_invite_url,
        title_github: const.bot_github_url,
        title_version: f"**`v{const.version}`**",
    }
    embed = cembed.get_cembed(ctx.msg, text, title, fields=fields, inline=True)
    await ctx.reply(embed=embed)

################################################################
