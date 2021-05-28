################################################################

import sys

sys.path.append("..")

import const
import cembed
import cmdlib
import loclib
from pyexecute import PyExecute, ExecTimeoutError

################################################################

executor = PyExecute(const.files["pycalc"], 
const.exec_timeout, const.checks_per_second, const.python_cmd)

################################################################

async def calc(ctx):

    expr = ctx.args["expression"]
    expr = expr.strip(" `\n").replace("^", "**").replace("\n", " ").replace(",", ".")
    allowed_chars = " \t0123456789.+-*/%()_"

    if not all(char in allowed_chars for char in expr):
        raise cmdlib.CmdError("err_calc_banned_char")

    try:
        execute_code = lambda: executor.execute(f"print(round({expr}, 10))")
        result = await ctx.async_exec(execute_code)
        output, error = result.stdout, result.stderr

        if output:
            text = output[:2000].strip() + " "
        else:
            err_syntax = loclib.Loc.member("err_calc_syntax_error", ctx.author)
            err_zero_div = loclib.Loc.member("err_calc_zero_division", ctx.author)
            text = err_zero_div if "ZeroDivisionError" in error else err_syntax

    except ExecTimeoutError:
        text = loclib.Loc.member("err_exec_timeout", ctx.author)
        text.format(const.exec_timeout)

    title = loclib.Loc.member("label_result", ctx.author)
    embed = cembed.get_cembed(ctx.msg, f"```{text}```", title)
    await ctx.channel.send(embed=embed)

################################################################
