### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import const
from cmdtools import Arg, CmdError
from conyaml import read_data, write_data
from cfglib import guild_config
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "server-settings",
    "aliases": [
        "server-config",
        "server-options",
        "guild-settings",
        "guild-config",
        "guild-options",
    ],
    "category": "config",
    "index": 1,
    "args": [
        Arg("[option]", "guild_config"),
        Arg("[value]", "inf_str"),
    ],
}

# Command Call
async def call(ctx):
    config, value = ctx.args["option"], ctx.args["value"]
    if config and (not ctx.author.guild_permissions.manage_guild and \
        not ctx.author.id in const.devs):
        raise CmdError("cmd/server_settings/no_perms")

    if config:
        fvalue = config.format(ctx, value)
        name = Loc(f"config/name/{config.name}")

        if fvalue:
            write_data(f"guild_config/{ctx.guild.id}/{config.name}",
                fvalue)
            text = Loc("cmd/server_settings/success").format(
                name.cstring(ctx), config.display(fvalue))

        elif value:
            format = Loc(f"config/format/{config.name}")
            text = Loc("cmd_call/invalid_value").format(
                f"**{name.cstring(ctx)}**", value,
                format.cstring(ctx).lower(),
            )

        else:
            write_data(f"guild_config/{ctx.guild.id}/{config.name}",
                config.default)
            none = Loc("misc/none").cstring(ctx)
            default = Loc("misc/default").cstring(ctx).lower()
            default_value = config.display(config.default)
            default_text = f"{default_value or none} ({default})"
            text = Loc("cmd/server_settings/success").format(
                name.cstring(ctx), default_text)

        embed = cembed(ctx, text)

    else:
        title = Loc("cmd/server_settings/title")
        fields = {}
        for config in guild_config:
            name = Loc(f"config/name/{config.name}")
            value = read_data(f"guild_config/{ctx.guild.id}/{config.name}")
            value = config.display(value) or Loc("misc/none")
            fields[name] = value
        embed = cembed(ctx, title=title, author={
            "name": ctx.guild.name,
            "icon": ctx.guild.icon_url,
        }, fields=fields)

    await ctx.reply(embed=embed)
