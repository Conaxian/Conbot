################################################################

import sys

sys.path.append("..")

import cembed
import loclib

################################################################

async def help(ctx):

    command = ctx.args["command"]

    if not command:

        cmd_list = {}
        for cmd in ctx.commands:
            if cmd.category not in cmd_list.keys():
                cmd_list[cmd.category] = []
            cmd_list[cmd.category].append(cmd.name)
        cmd_list.pop("dev", None)

        prefix_text = loclib.Loc.member("text_current_prefix", ctx.author)
        prefix_text.format(ctx.prefix)
        title = loclib.Loc.member("label_help", ctx.author)

        category_list = {}
        for category in cmd_list.items():
            category_name = loclib.Loc.member(f"cmd_category_{category[0]}", ctx.author)
            cmd_str = "`, `".join(category[1])
            category_list[category_name] = f"`{cmd_str}`"

        embed = cembed.get_cembed(ctx.msg, f"{prefix_text}\n", title, fields=category_list)

    else:

        cmd = None
        for command in ctx.commands:
            arg_cmd = ctx.args["command"].lower().replace("_", "-")
            if arg_cmd.lstrip(ctx.prefix) in command.calls:
                cmd = command
        
        if not cmd or cmd.category == "dev":
            text = loclib.Loc.member("err_help_unknown_cmd", ctx.author)
            embed = cembed.get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)
            return

        fields = {}
        none = loclib.Loc.member("label_none", ctx.author)

        syntax = loclib.Loc.member("label_syntax", ctx.author)
        cmd_call = f"{ctx.prefix}{cmd.name}"
        args = " ".join(cmd.args)
        cmd_syntax = f"{cmd_call} {args}"
        fields[syntax] = f"`{cmd_syntax.strip()}`"
        
        aliases = loclib.Loc.member("label_aliases", ctx.author)
        alias_list = [f"`{call}`" for call in cmd.calls if call != cmd.name]
        cmd_aliases = ", ".join(alias_list)
        fields[aliases] = cmd_aliases if cmd_aliases != "" else none

        req_perms = loclib.Loc.member("label_req_perms", ctx.author)
        perms = []
        for perm in cmd.perms:
            perm_name = loclib.Loc.member(f"perm_{perm}", ctx.author)
            perms.append(str(perm_name))
        perms_text = ", ".join(perms)
        fields[req_perms] = perms_text if perms != [] else none

        desc_title = loclib.Loc.member("label_desc", ctx.author)
        desc = loclib.Loc.member(f"cmd_desc_{cmd.desc}", ctx.author)
        fields[desc_title] = desc

        embed = cembed.get_cembed(ctx.msg, "", cmd_call, fields=fields)

    await ctx.channel.send(embed=embed)

################################################################
