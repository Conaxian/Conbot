### Imports

# Standard Library
from time import time
from itertools import chain
from difflib import get_close_matches
from traceback import format_exc

# Dependencies
from discord import Message, errors

# Conbot Modules
import const
import utils
from bot import Bot
import conyaml
import cmdtools
from cembed import cembed
from loclib import Loc
from commands import commands, Command

### Class Definitions

# Message Handler
class MsgHandler:
    """
    Handles received messages.
    """

    def __init__(self, bot: Bot):
        self.bot = bot

    async def handle(self, msg: Message):
        """
        Handles a received message.
        """
        if msg.author.bot or msg.is_system() or not msg.content: return
        guild_config = conyaml.read_data(f"guild_config/{msg.guild.id}")
        prefix = guild_config.prefix or const.prefix

        if utils.mention_id(msg.content) == self.bot.user.id:
            text = Loc("misc/current_prefix").format(prefix)
            await msg.channel.send(text.cstring(msg),
                reference=msg, mention_author=False)
            return

        autoreply = msg.content.strip(" \n\t" + const.md_chars).lower()
        if autoreply in const.autoreplies:
            await msg.channel.send(const.autoreplies[autoreply],
                reference=msg, mention_author=False)
            return

        if msg.content.lower().startswith(prefix) and \
            set(msg.content) != {prefix}:
            call_times = self.bot.global_vars.get("call_times", {})
            call_time = call_times.get(msg.author.id, float("-inf"))
            if call_time > time() - const.cmd_cooldown: return
            if not call_times:
                self.bot.global_vars["call_times"] = {}
            self.bot.global_vars["call_times"][msg.author.id] = time()

            await self.cmd_parse(msg, prefix)

    async def cmd_parse(self, msg: Message, prefix: str):
        """
        Parses a message into a command call.
        """
        original_call = msg.content.split()[0][len(prefix):]
        call = original_call.lower().replace("_", "-")
        cmd = utils.find(lambda cmd: call in cmd.calls(),
        commands)

        if not cmd or \
            (cmd.flags.dev and msg.author.id not in const.devs):
            calls = [cmd.calls() for cmd in commands \
                if not cmd.flags.dev]
            calls = list(chain(*calls))
            matches = get_close_matches(call, calls, 1,
            const.cmd_hint_threshold)   

            if not matches:
                text = Loc("cmd_call/unknown_cmd")
                text.format(prefix)
            else:
                text = Loc("cmd_call/unknown_cmd_hint")
                text.format(prefix, matches[0])

            embed = cembed(msg, text)
            await msg.channel.send(embed=embed,
            reference=msg, mention_author=False)
            return

        perms = dict(iter(msg.author.guild_permissions))
        has_perms = all([perms[perm] for perm in cmd.perms])
        if not has_perms:
            text = Loc("cmd_call/no_perms_user")
            embed = cembed(msg, text)
            await msg.channel.send(embed=embed,
            reference=msg, mention_author=False)
            return

        arg_string = msg.content \
            .removeprefix(prefix + original_call).strip()
        args = None

        try:
            args = await self.arg_parse(msg, prefix, cmd, arg_string)

        except cmdtools.InvalidArgError as error:
            invalid_arg = Loc("cmd_call/invalid_value")
            arg_format = Loc(f"arg_format/{error.args[0].format}")
            text = invalid_arg.format(
                f"`{error.args[0]}`",
                utils.escape_code(error.args[1]),
                arg_format.cstring(msg).lower(),
            )
            embed = cembed(msg, text)
            await msg.channel.send(embed=embed,
            reference=msg, mention_author=False)

        if args == None: return
        ctx = self.get_ctx(self.bot, msg, prefix, args)

        try:
            await cmd.call(ctx)
            return

        except cmdtools.CmdError as error:
            text = Loc(error.args[0]).format(*error.args[1:])

        except (errors.Forbidden, cmdtools.BotPermsError) as error:
            if isinstance(error, cmdtools.BotPermsError) or \
                str(error).endswith("Missing Permissions"):
                text = Loc("cmd_call/no_perms_bot")

        except:
            text = "```" + utils.escape_code(format_exc()) + "```"

        if text:
            embed = cembed(ctx, text)
            await msg.channel.send(embed=embed,
            reference=msg, mention_author=False)

    async def arg_parse(self,
        msg: Message,
        prefix: str,
        cmd: Command,
        string: str,
    ) -> dict:
        """
        Parses a string into a dictionary of arguments.
        """
        args = cmd.args.copy()
        arg_dict = {}
        text = None

        while string and args:
            result, remainder = \
                await args[0].parse(self.bot, msg,
                    commands, prefix, string)
            arg_dict[args[0].name] = result
            string = remainder
            args.pop(0)

        missing_arg = utils.find(lambda arg: not arg.optional, args)
        if args and missing_arg:
            text = Loc("cmd_call/min_args").format(missing_arg)
        elif string:
            overflowing = utils.escape_code(string)
            text = Loc("cmd_call/max_args").format(overflowing)

        if text:
            embed = cembed(msg, text)
            await msg.channel.send(embed=embed,
            reference=msg, mention_author=False)
            return

        for arg in args:
            arg_dict[arg.name] = None
        return arg_dict

    @staticmethod
    def get_ctx(
        bot: Bot,
        msg: Message,
        prefix: str,
        args: dict[str],
    ) -> cmdtools.Context:
        """
        Creates a command context.
        """
        user_config = conyaml.read_data(f"user_config/{msg.author.id}")
        guild_config = conyaml.read_data(f"guild_config/{msg.guild.id}")
        meta = {
            "user_lang": user_config.language,
            "guild_lang": guild_config.language,
        }
        ctx = cmdtools.Context(bot, msg, commands, prefix, args, **meta)
        return ctx
