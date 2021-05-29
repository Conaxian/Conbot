################################################################

import sys

sys.path.append("..")

import utils
import conyaml
import cembed
import cmdlib
import loclib

################################################################

async def user_settings(ctx):

    target_mention = ctx.args["member"]
    target = ctx.author
    if target_mention:
        target_id = utils.mention_id(target_mention)
        if target_id != 0:
            target = ctx.guild.get_member(target_id)
        if not target:
            raise cmdlib.CmdError("err_unknown_member", ctx.client.user.mention)

    fields = {}
    for config in ctx.user_config:
        name = loclib.Loc.member(f"config_{config.name}", ctx.author)
        value = conyaml.read_user_config(target.id, config.name)
        value = config.format(value)
        value = value if value else loclib.Loc.member("label_none", ctx.author)
        fields[name] = value

    title = loclib.Loc.member("label_user_config", ctx.author)
    embed = cembed.get_cembed(ctx.msg, "", title, author_name=target.name, author_img=target.avatar_url, fields=fields)
    await ctx.send(embed=embed)

################################################################
