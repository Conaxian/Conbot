################################################################

import sys

sys.path.append("..")

import conyaml
import cembed
import cmdlib
import loclib

################################################################

async def server_settings(ctx):

    option, value = ctx.args["option"], ctx.args["value"]
    if option and not ctx.author.guild_permissions.manage_guild:
        raise cmdlib.CmdError("err_server_settings_perms")

    if option:
        for config in ctx.server_config:
            loc_name = loclib.Loc.member(f"config_{config.name}", ctx.author)
            config_names = [config.name, str(loc_name).lower()]
            if option.strip().lower().replace("_", " ") in config_names:
                valid_value = config.validate(ctx, value)

                if valid_value:
                    conyaml.set_server_config(ctx.guild.id, config.name, valid_value)
                    text = loclib.Loc.member("text_server_settings_success", ctx.author)
                    text.format(loc_name, config.format(valid_value))
                elif value:
                    text = loclib.Loc.member(f"config_invalid_{config.name}", ctx.author)

                else:
                    conyaml.set_server_config(ctx.guild.id, config.name, None)
                    text = loclib.Loc.member("text_server_settings_success", ctx.author)
                    none = loclib.Loc.member("label_none", ctx.author)
                    default = loclib.Loc.member("label_default", ctx.author)
                    default = str(default).lower()
                    default_value = config.format(config.default)
                    default_value = f"{default_value or none} ({default})"
                    text.format(loc_name, default_value)

                embed = cembed.get_cembed(ctx.msg, text)
                break
        else:
            raise cmdlib.CmdError("err_settings_unknown_option")

    else:
        fields = {}
        for config in ctx.server_config:
            name = f"config_{config.name}"
            name = loclib.Loc.member(name, ctx.author)
            value = conyaml.read_server_config(ctx.guild.id, config.name)
            value = config.format(value)
            value = value or loclib.Loc.member("label_none", ctx.author)
            fields[name] = value

        title = loclib.Loc.member("label_server_config", ctx.author)
        embed = cembed.get_cembed(ctx.msg, "", title, author_name=ctx.guild.name, author_img=ctx.guild.icon_url, fields=fields)

    await ctx.send(embed=embed)

################################################################
