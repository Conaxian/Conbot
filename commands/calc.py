################################################################

import sys

sys.path.append("..")

import constants
import cembed
import loclib
from pyexecute import PyExecute

################################################################

async def calc(ctx):

    expr = ctx.args["expression"]
    expr = expr.strip(" `\n").replace("^", "**").replace("\n", " ")
    allowed_chars = " \t0123456789.+-*/%()"
    text = None

    for char in expr:
        if char not in allowed_chars:
            text = loclib.Loc.member("err_calc_bannned_char", ctx.author)
            break

    else:
        err_timeout = loclib.Loc.member("err_calc_timeout", ctx.author)
        exec_loc = {"err_exec_timeout": err_timeout, "err_exec_banned_module": "", "err_exec_banned_keyword": ""}
        pyexecute = PyExecute(constants.files["pycalc"], exec_loc)
        text = pyexecute.execute(f"print({expr})")
        
        err_syntax = loclib.Loc.member("err_calc_syntax_error", ctx.author)
        text = text if "Error" not in text else err_syntax
        text = text if len(text) <= 2000 else text[:2000]

    title = loclib.Loc.member("label_result", ctx.author)
    embed = cembed.get_cembed(ctx.msg, f"```{text}```", title)
    await ctx.channel.send(embed=embed)

################################################################