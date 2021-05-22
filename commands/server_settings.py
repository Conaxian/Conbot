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

    if option and ctx.author.guild_permissions.manage_guild:

        for config in ctx.server_config:
            loc_name = loclib.Loc.member(f"config_{config.name}", ctx.author)
            if option.lower().strip().replace("_", " ") in [config.name, str(loc_name).lower()]:

                if value:
                    value = config.validate(ctx, value)

                    if value:
                        conyaml.set_server_config(ctx.guild.id, config.name, value)
                        text = loclib.Loc.member("text_server_settings_success", ctx.author)
                        text.format(loc_name, config.format(value))

                    else:
                        text = loclib.Loc.member(f"config_invalid_{config.name}", ctx.author)
                
                else:
                    conyaml.set_server_config(ctx.guild.id, config.name, None)
                    text = loclib.Loc.member("text_server_settings_success", ctx.author)
                    none = loclib.Loc.member("label_none", ctx.author)
                    default = loclib.Loc.member("label_default", ctx.author)
                    default_value = config.format(config.default)
                    default_value = f"{default_value if default_value else none} ({str(default).lower()})"
                    text.format(loc_name, default_value)

                break
            else:
                raise cmdlib.CmdError("err_settings_unknown_option")

        embed = cembed.get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)

    elif option:

        raise cmdlib.CmdError("err_server_settings_perms")

    else:

        fields = {}
        for config in ctx.server_config:
            name = f"config_{config.name}"
            name = loclib.Loc.member(name, ctx.author)
            value = conyaml.read_server_config(ctx.guild.id, config.name)
            value = config.format(value)
            value = value if value else loclib.Loc.member("label_none", ctx.author)
            fields[name] = value

        title = loclib.Loc.member("label_server_config", ctx.author)
        embed = cembed.get_cembed(ctx.msg, "", title, author_name=ctx.guild.name, author_img=ctx.guild.icon_url, fields=fields)
        await ctx.channel.send(embed=embed)

################################################################
