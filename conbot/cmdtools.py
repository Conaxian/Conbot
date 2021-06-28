### Imports

# Standard Library
from typing import Any
from math import isnan

# Dependencies
from discord import Message, ChannelType
from googletrans import LANGUAGES, LANGCODES

# Conbot Modules
import const
import utils
from bot import Bot
from cbcollections import AttrDict
from cfglib import guild_config
from loclib import Loc

### Class Definitions

# Command Context
class Context:
    """
    Represents the context of a command call.
    """

    def __init__(self,
        bot: Bot,
        msg: Message,
        commands: list,
        prefix: str,
        args: list,
        **meta,
    ):
        self.bot = bot
        self.msg = msg
        self.author = msg.author
        self.channel = msg.channel
        self.guild = msg.guild
        self.commands = commands
        self.prefix = prefix
        self.args = args
        self.meta = AttrDict(**meta)

    async def send(self, content: str=None, *args, **kwargs):
        """
        Sends a message to the channel of the Context.
        """
        await self.channel.send(content, *args, **kwargs)

    async def reply(self, content: str=None, *args, **kwargs):
        """
        Replies to the message of the Context.
        """
        mention_author = kwargs.get("mention_author", False)
        await self.channel.send(content, *args, **kwargs, 
        reference=self.msg, mention_author=mention_author)

# Command Argument
class Arg:
    """
    Represents a single command argument.

    ### Valid formats:

    word -> `str`:
        A single word separated by whitespace.
    inf_str -> `str`:
        A string of an arbitrary amount of words.
    word_comma -> `str`:
        A single word separated by a comma.
    inf_words_comma -> `list[str]`:
        A list of an arbitrary amount of words
        separated by commas.
    py_code -> `str`:
        A Python code, possibly formatted with Markdown.
    calc_expr -> `str`:
        A calculator expression, possibly formatted
        with Markdown.
    loc_lang -> `str`:
        A valid language code of a localization.
    lang_opt -> `str`:
        A language code or a name of a language
        supported by Google Translate.
        If the code/name isn't valid, the argument
        is ignored.
    int -> `int`:
        An integer parsed from the first word.
        Any trailing commas are stripped.
    cmd -> `commands.Command`:
        A command obtained by a call name.
        Commands with `flags.dev` are ignored.
    guild_config -> `cfglib.Config`:
        A single guild configuration obtained by its name.
    member -> `discord.Member`:
        A member of the message guild
        obtained by an ID or a mention.
    banned_user -> `discord.User`:
        A user who is banned from the message guild,
        obtained by an ID or a mention.
    text_channel_any -> `discord.TextChannel`:
        A text channel of any guild which
        the bot is a part of, obtained
        by an ID or a mention.
    custom_emoji_any -> `discord.Emoji`:
        A custom emoji of any guild which both
        the message author and the bot are
        members of, obtained by a name.
    """

    def __init__(self, name: str, format: str="word"):
        self.name = name.strip("<>[]")
        self.optional = \
            name.startswith("[") and name.endswith("]")
        self.format = format

    def __repr__(self):
        brackets = "[]" if self.optional else "<>"
        return brackets[0] + self.name + brackets[1]

    async def parse(self,
        bot: Bot,
        msg: Message,
        commands: list,
        prefix: str,
        string: str,
    ) -> tuple[Any, str]:
        """
        Parses a string into an argument.
        """
        if self.format == "word":
            result = string.split()[0]
            remainder = string.removeprefix(result)

        elif self.format == "inf_str":
            result, remainder = string, ""

        elif self.format == "word_comma":
            result = string.split(",")[0]
            remainder = string.removeprefix(result) \
                .removeprefix(",")

        elif self.format == "inf_words_comma":
            result = string.split(",")
            result = list(map(str.strip, result))
            remainder = ""

        elif self.format == "py_code":
            result = utils.strip_code(string) \
                .removeprefix("py").removeprefix("thon") \
                .strip(" \t\n")
            remainder = ""

        elif self.format == "calc_expr":
            result = utils.strip_code(string) \
                .strip(" \t\n").replace("\n", " ") \
                .replace("^", "**").replace(",", ".")
            remainder = ""

        elif self.format == "loc_lang":
            first_word = string.split()[0]
            result = first_word.replace("-", "_")
            if not result in const.languages:
                raise InvalidArgError(self, first_word)
            remainder = string.removeprefix(first_word)

        elif self.format == "lang_opt":
            first_word = string.split()[0]
            lang = first_word.lower()
            valid = lang in LANGUAGES or lang in LANGCODES
            result = lang if valid else None
            remainder = string.removeprefix(first_word) \
                if valid else string

        elif self.format == "int":
            num_str = string.split()[0]
            try:
                result = int(num_str.removesuffix(","))
            except ValueError:
                raise InvalidArgError(self, num_str.removesuffix(","))
            remainder = string.removeprefix(num_str)

        elif self.format == "num":
            num_str = string.split()[0]
            try:
                fixed_str = num_str.removesuffix(",").replace(",", ".")
                result = utils.fix_float(float(fixed_str))
                if isnan(result): raise ValueError
            except ValueError:
                raise InvalidArgError(self, num_str.removesuffix(","))
            remainder = string.removeprefix(num_str)

        elif self.format == "cmd":
            first_word = string.split()[0]
            cmd_call = first_word.lower().removeprefix(prefix) \
                .replace("_", "-")
            result = utils.find(lambda cmd: cmd_call in cmd.calls(),
            commands)
            if not result or result.flags.dev:
                raise InvalidArgError(self, first_word)
            remainder = string.removeprefix(first_word)

        elif self.format == "guild_config":
            result = None
            for config in guild_config:
                name = Loc(f"config/name/{config.name}") \
                    .cstring(msg).lower()
                string_parts = string.split()
                name_parts = name.split()
                cut_string = ""
                for i in range(len(name_parts)):
                    cut_string += string_parts[i] + " "
                    if name_parts[i].lower() != \
                        string_parts[i].lower():
                        break
                else:
                    result = config
                    remainder = string.removeprefix(cut_string.strip())
                    break
            if not result:
                raise InvalidArgError(self, cut_string.strip())

        elif self.format == "member":
            first_word = string.split()[0]
            mention_id = utils.mention_id(first_word)
            result = msg.guild.get_member(mention_id)
            if not result:
                raise InvalidArgError(self, first_word)
            remainder = string.removeprefix(first_word)

        elif self.format == "banned_user":
            first_word = string.split()[0]
            mention_id = utils.mention_id(first_word)
            bans = await msg.guild.bans()
            banned_users = (ban.user for ban in bans)
            result = utils.get(banned_users, id=mention_id)
            if not result:
                raise InvalidArgError(self, first_word)
            remainder = string.removeprefix(first_word)

        elif self.format == "text_channel_any":
            first_word = string.split()[0]
            mention_id = utils.mention_id(first_word)
            result = bot.get_channel(mention_id)
            if not result or result.type != ChannelType.text:
                raise InvalidArgError(self, first_word)
            remainder = string.removeprefix(first_word)

        elif self.format == "custom_emoji_any":
            emoji_name = string.split()[0]
            result = utils.get(bot.emojis, name=emoji_name)
            if not result or not result.available or not \
                result.guild.get_member(msg.author.id):
                raise InvalidArgError(self, emoji_name)
            remainder = string.removeprefix(emoji_name)

        return result, remainder.strip()

### Command Errors

# Base Command Error
class CmdError(Exception):
    """
    Base class for all command errors.
    """

# Bot Permissions Error
class BotPermsError(CmdError):
    """
    Raised when the bot has insufficient permissions.
    """

# Invalid Argument Error
class InvalidArgError(CmdError):
    """
    Raised when an invalid argument is passed to a command.
    """
