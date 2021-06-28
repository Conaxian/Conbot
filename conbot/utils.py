### Imports

# Standard Library
from datetime import datetime, timedelta

# Dependencies
import discord
from speedtest import Speedtest

# Conbot Modules
import const

### Function Definitions

# Utility functions from discord.py
get = discord.utils.get
find = discord.utils.find

# Fix Float
def fix_float(number: float) -> float:
    """
    Fixes a float by rounding it to 10 decimal places.
    """
    return round(number, 10)

# Mention ID
def mention_id(mention: str) -> int:
    """
    Converts a mention string to a snowflake (ID).
    """
    try:
        mention = mention.strip()
        if isinstance(mention, int) or mention.isdigit():
            return int(mention)
        is_mention = (
            mention.startswith("<@") and mention[2:-1].isdigit(),
            mention.startswith("<@!") and mention[3:-1].isdigit(),
            mention.startswith("<@&") and mention[3:-1].isdigit(),
            mention.startswith("<#") and mention[2:-1].isdigit(),
        )
        if any(is_mention) and mention.endswith(">"):
            return int(mention.strip("<>@!&#"))
        return 0
    except:
        return 0

# Date
def date(offset: timedelta=timedelta()) -> str:
    """
    Returns a string representation of the current date.
    """
    date_now = datetime.utcnow() + offset
    date_str = date_now.strftime(const.date_format)
    return date_str

# Time
def time(offset: timedelta=timedelta()) -> str:
    """
    Returns a string representation of the current time.
    """
    time_now = datetime.utcnow() + offset
    time_str = time_now.strftime(const.time_format)
    return time_str

# Escape Markdown
def escape_md(string: str) -> str:
    """
    Escapes all Markdown characters.
    """
    string = string.replace("\\", "\\\\")
    for char in const.md_chars:
        string = string.replace(char, "\\" + char)
    return string

# Strip Code
def strip_code(string: str) -> str:
    """
    Strips 1 to 3 backticks around the string.
    """
    for i in range(3):
        string = string.removeprefix("`").removesuffix("`")
    return string

# Escape Code
def escape_code(string: str) -> str:
    """
    Escapes all backticks with acute accents.
    """
    string = string.strip() or " "
    return string.replace("`", "´")

# Constrain Embed Description
def embed_desc_constrain(desc: str, pre: str="", post: str="") -> str:
    """
    Constrains the embed description to fit inside
    the character limit.
    """
    padding_len = len(pre) + len(post)
    max_desc_length = const.embed_desc_limit - padding_len - len(desc)
    desc = desc[:max_desc_length]
    return pre + desc + post

# Is a role normal?
def is_role_normal(role: discord.Role) -> bool:
    """
    Checks if the role is normal (neither controlled by
    integration, nor @everyone or the Server Booster role).
    """
    return not (
        role.is_bot_managed() or \
        role.is_default() or \
        role.is_integration() or \
        role.is_premium_subscriber()
    )

# Log
def log(msg: discord.Message):
    """
    Logs a message.
    """
    if msg.is_system(): return
    text = \
        f"\
----------------------------------------\
\n\
Timestamp: {date()} | {time()} UTC\
\n\
Guild:     {msg.guild.name} ({msg.guild.id})\
\n\
Channel:   #{msg.channel.name} ({msg.channel.id})\
\n\
Author:    {msg.author} ({msg.author.id})\
\n\
Content:\
\n\
{msg.content or '<empty>'}\
\n\
----------------------------------------\n\
########################################\n"
    with open(const.log_file, "a", encoding=const.encoding) as file:
        file.write(text)

# Speedtest
def speedtest() -> tuple[float, float, float]:
    """
    Tests the internet speed of the bot's server.
    Returned ping is in miliseconds (ms),
    download and upload are in megabits (Mbits).
    """
    test = Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    return test.results.ping, \
        test.results.download / 1_000_000, \
        test.results.upload / 1_000_000
