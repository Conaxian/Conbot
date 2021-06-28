### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import const
from cmdtools import Arg
from cembed import cembed
from loclib import Loc

### Command

# Command Meta
meta = {
    "name": "help",
    "aliases": [
        "commands",
    ],
    "category": "info",
    "index": 0,
    "args": [
        Arg("[command]", "cmd"),
    ],
}

# Command Call
async def call(ctx):
    command = ctx.args["command"]

    if not command:
        cmd_dict = {category:[] for category in const.categories}
        for cmd in ctx.commands:
            if cmd.flags.dev: continue
            cmd_dict[cmd.category].append(cmd)
        text = Loc("misc/current_prefix").format(ctx.prefix)
        title = Loc("cmd/help/help")

        fields = {}
        for category, cmd_list in cmd_dict.items():
            if not cmd_list: continue
            cmd_list.sort(key=lambda cmd: cmd.index)
            name = Loc(f"cmd_category/{category}")
            cmd_str = "`, `".join(cmd.name for cmd in cmd_list)
            fields[name] = "`" + cmd_str + "`"

        embed = cembed(ctx, text, title=title, fields=fields)

    else:
        fields = {}
        none = Loc("misc/none")
        syntax = Loc("cmd/help/syntax")
        aliases = Loc("cmd/help/aliases")
        req_perms = Loc("cmd/help/req_perms")
        desc = Loc("cmd/help/desc_title")

        title = f"{ctx.prefix}{command.name}"
        args_list = [str(arg) for arg in command.args]
        args = " ".join(args_list)
        fields[syntax] = "`" + (title + " " + args).strip() + "`"

        alias_list = ["`" + alias + "`" for alias in command.aliases]
        fields[aliases] = ", ".join(alias_list) or none

        perms = [
            Loc(f"perm/{perm}").cstring(ctx)
            for perm in command.perms
        ]
        fields[req_perms] = ", ".join(perms) or none
        fields[desc] = Loc(f"cmd/{command.name.replace('-', '_')}/desc") \
            .format(*args_list)

        embed = cembed(ctx, title=title, fields=fields)

    await ctx.reply(embed=embed)
