################################################################

import sys

sys.path.append("..")

import utils
import cembed
import conyaml
import cmdlib
import loclib

################################################################

async def warn(ctx):

    arg_words = ctx.args["target, reason"].split(" ")
    reason = "Unspecified" if len(arg_words) < 2 else " ".join(arg_words[1:])
    target_id = utils.mention_id(arg_words[0])
    target = ctx.guild.get_member(target_id)

    if not target:
        raise cmdlib.CmdError("err_unknown_member", ctx.client.user.mention)
    if target.top_role >= ctx.author.top_role:
        raise cmdlib.CmdError("err_warn_perms_author")

    conyaml.add_warn(ctx.guild.id, target.id, reason)
    text = loclib.Loc.member("text_warn_success", ctx.author)
    target_mention = f"<@!{target_id}>"
    text.format(target_mention, f"`{reason}`")

    embed = cembed.get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################
