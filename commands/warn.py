################################################################

import sys

sys.path.append("..")

import utils
import cembed
import conyaml
import loclib

################################################################

async def warn(ctx):

    arg_words = ctx.args["target, reason"].split(" ")
    reason = "Unspecified" if len(arg_words) < 2 else " ".join(arg_words[1:])
    target_id = utils.mention_id(arg_words[0])
    target = ctx.guild.get_member(target_id)
    text = ""

    if not target:
        text = loclib.Loc.member("err_unknown_member", ctx.author)
        text.format(ctx.client.user.mention)
    elif target.top_role >= ctx.author.top_role:
        text = loclib.Loc.member("err_warn_perms_author", ctx.author)
    if text:
        embed = cembed.get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return

    conyaml.add_warn(ctx.guild.id, target.id, reason)
    text = loclib.Loc.member("text_warn_success", ctx.author)
    target_mention = f"<@!{target_id}>"
    text.format(target_mention, f"`{reason}`")

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################
