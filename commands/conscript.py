################################################################

import sys
import traceback

sys.path.append("..")

import constants
import cembed
import loclib
import conscript_lib
from pyexecute import PyExecute

################################################################

async def conscript(ctx):

    code = ctx.args["code"]
    code = code.strip(" `\n")
    if code.startswith("python"):
        code = code[6:]
    elif code.startswith("py"):
        code = code[2:]

    exec_loc = {}
    for loc_name in ["err_exec_timeout", "err_exec_banned_module", "err_exec_banned_keyword"]:
        exec_loc[loc_name] = loclib.Loc.member(loc_name, ctx.author)
    exec_loc["err_exec_timeout"].format(constants.exec_timeout)

    pyexecute = PyExecute(constants.files["pyexecute"], exec_loc)
    output = str(pyexecute.execute(code))
    title = loclib.Loc.member("label_output", ctx.author)

    if output in [str(text) for text in exec_loc.values()]:
        output = output if len(output) <= 2000 else output[:2000]
        title = loclib.Loc.member("label_output", ctx.author)

    else:
        cs_base = conscript_lib.Base(ctx)
        try:
            exec(code, {"cb": cs_base})
            output = None
        except:
            output = traceback.format_exc()

    if output:
        embed = cembed.get_cembed(ctx.msg, f"```{output}```", title)
        await ctx.channel.send(embed=embed)

################################################################