### Imports

# Standard Library
import sys

# Conbot Modules
sys.path.append("..")
import const
import utils
from cmdtools import Arg
from cembed import cembed
from loclib import Loc
from pyexecute import PyExecutor, UnsafeCodeError, ExecTimeoutError

### Initialization

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
    "name": "python",
    "category": "tools",
    "aliases": [
        "py",
        "execute",
        "exec",
        "exe",
    ],
    "index": 4,
    "args": [
        Arg("<code>", "py_code"),
    ],
}

# Command Call
async def call(ctx):
    code = ctx.args["code"]
    admin = code.startswith("#dev") and ctx.author.id in const.devs

    try:
        exec_code = lambda: executor.execute(code, admin)
        result = await ctx.bot.async_exec(exec_code)
        output = utils.escape_code(result.stdout or result.stderr)
        exec_time = round(result.exec_time, 2)
        text = Loc("cmd/python/success").format(exec_time)

    except UnsafeCodeError as error:
        error = error.args[0]
        if error in const.banned_names:
            output = Loc("cmd/python/banned_name")
        else:
            output = Loc("cmd/python/banned_module")
        output.format(error)
        text = Loc("cmd/python/failure")

    except ExecTimeoutError:
        output = Loc("cmd/python/timeout").format(const.exec_timeout)
        text = Loc("cmd/python/failure")

    title = Loc("cmd/python/output")
    if isinstance(output, Loc): output = output.cstring(ctx)
    text = utils.embed_desc_constrain(output, "```", 
        "```\n" + text.cstring(ctx))
    embed = cembed(ctx, text, title=title)
    await ctx.reply(embed=embed)
