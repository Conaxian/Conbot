################################################################

import sys

sys.path.append("..")

import const
import conyaml
import cembed
import cmdlib
import loclib

################################################################

async def language(ctx):

    lang = ctx.args["language"]

    if not lang:

        fields = {}
        for language in const.loc_files.keys():
            lang_name = loclib.loc_dict[language]["language_name"]
            fields[lang_name] = f"`{language}`"

        text = loclib.Loc.member("text_lang_list", ctx.author)
        title = loclib.Loc.member("label_languages", ctx.author)
        embed = cembed.get_cembed(ctx.msg, text, title, fields=fields)

    else:

        lang = lang.replace("-", "_")
        if lang in const.loc_files.keys():
            conyaml.set_user_config(ctx.author.id, "language", lang)
            text = loclib.Loc.member("text_lang_changed", ctx.author)
        else:
            raise cmdlib.CmdError("err_unknown_lang")

        embed = cembed.get_cembed(ctx.msg, text)

    await ctx.channel.send(embed=embed)

################################################################
