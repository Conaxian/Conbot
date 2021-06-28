### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import const
import utils
from cmdtools import Arg, CmdError
from cembed import cembed
from loclib import Loc
from pyexecute import PyExecutor, ExecTimeoutError

### Initialization

# Allowed Characters
allowed_chars = " \t0123456789.+-*/%()_"

# Python Executor
executor = PyExecutor(
    const.pyexec_file,
    const.exec_timeout,
    const.checks_per_second,
    const.python_cmd,
)

### Command

# Command Meta
meta = {
    "name": "calc",
    "category": "tools",
    "aliases": [
        "calculate",
        "eval",
        "evaluate",
    ],
    "index": 3,
    "args": [
        Arg("<expression>", "calc_expr"),
    ],
}

# Command Call
async def call(ctx):
    expr = ctx.args["expression"]
    illegal_char = utils.find(lambda char: \
        char not in allowed_chars, expr)
    if illegal_char:
        raise CmdError("cmd/calc/illegal_char",
            utils.escape_code(illegal_char))

    try:
        code = f"print(round({expr}, 10))"
        exec_code = lambda: executor.execute(code)
        result = await ctx.bot.async_exec(exec_code)
        output, error = utils.escape_code(result.stdout), result.stderr
        if error:
            syntax_error = Loc("cmd/calc/syntax_error")
            zero_div = Loc("cmd/calc/zero_division")
            text = zero_div if "ZeroDivisionError" \
                in error else syntax_error
        else: text = output

    except ExecTimeoutError:
        text = Loc("cmd/calc/timeout").format(const.exec_timeout)

    title = Loc("cmd/calc/result")
    if isinstance(text, Loc): text = text.cstring(ctx)
    text = utils.embed_desc_constrain(text, "```", "```")
    embed = cembed(ctx, text, title=title)
    await ctx.reply(embed=embed)
