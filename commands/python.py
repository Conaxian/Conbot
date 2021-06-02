################################################################

import sys

sys.path.append("..")

import const
import cembed
import cmdlib
import loclib
from pyexecute import PyExecute, UnsafeCodeError, ExecTimeoutError

################################################################

executor = PyExecute(const.files["pyexecute"], 
const.exec_timeout, const.checks_per_second, const.python_cmd)

################################################################

async def python(ctx):

    code = ctx.args["code"]
    code = code.strip(" `\n")
    code = code.removeprefix("py").removeprefix("thon")
    code = code.strip(" `\n")
    admin = code.startswith("#dev") and ctx.author.id in const.devs

    try:
        execute_code = lambda: executor.execute(code, admin)
        result = await ctx.async_exec(execute_code)
        output = result.stdout or result.stderr
        output = output.strip().replace("`", "´") + " "
        finish_text = loclib.Loc.member("text_exec_success", ctx.author)
        exec_time = round(result.exec_time, 2)
        finish_text.format(exec_time)

    except UnsafeCodeError as error:
        error = error.args[0]
        if error in const.banned_names:
            output = loclib.Loc.member("err_exec_banned_name", ctx.author)
        else:
            output = loclib.Loc.member("err_exec_banned_module", ctx.author)
        output.format(error)
        finish_text = loclib.Loc.member("text_exec_failure", ctx.author)

    except ExecTimeoutError:
        output = loclib.Loc.member("err_exec_timeout", ctx.author)
        output.format(const.exec_timeout)
        finish_text = loclib.Loc.member("text_exec_failure", ctx.author)

    title = loclib.Loc.member("label_output", ctx.author)
    max_output_length = const.max_embed_desc_length - len(f"```\n{finish_text}```")
    output = output[:max_output_length]
    embed = cembed.get_cembed(ctx.msg, f"```{output}```\n{finish_text}", title)
    await ctx.reply(embed=embed)

################################################################
