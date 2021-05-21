################################################################

import sys

sys.path.append("..")

import const
import cembed
import loclib
import pyexecute

################################################################

async def python(ctx):

    code = ctx.args["code"]
    code = code.strip(" `\n")
    if code.startswith("python"):
        code = code[6:]
    elif code.startswith("py"):
        code = code[2:]

    exec_loc = {}
    exec_loc["timeout"] = loclib.Loc.member("err_exec_timeout", ctx.author)
    exec_loc["banned_module"] = loclib.Loc.member("err_exec_banned_module", ctx.author)
    exec_loc["banned_keyword"] = loclib.Loc.member("err_exec_banned_keyword", ctx.author)
    exec_loc["timeout"].format(const.exec_timeout)

    pyexec = pyexecute.PyExecute(const.files["pyexecute"], exec_loc)
    execute_code = lambda: pyexec.execute(code)
    output = await ctx.async_exec(execute_code)
    output = str(output)[:2000]

    title = loclib.Loc.member("label_output", ctx.author)
    embed = cembed.get_cembed(ctx.msg, f"```{output}```", title)
    await ctx.channel.send(embed=embed)

################################################################
