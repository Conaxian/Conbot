################################################################

"""
Conbot - Made by Conax

If you find any bugs, or if you have any suggestions, please contact me. My Discord is Conax#0001.

By using this software, you agree to the license terms in LICENSE.txt.
"""

################################################################

# Note - Discord.py API Documentation: https://discordpy.readthedocs.io/en/latest/api.html

################################################################

# All required modules

import discord
from discord.ext import tasks
import sys
import time
import datetime
import importlib
import difflib
import traceback

# Conbot modules

import const
import utils
import conyaml
import cembed
import cmdlib
import loclib
import songlib

# Search for modules in the "commands" directory

sys.path.append("commands")

################################################################

# Get all intents, create the client, define a dictionary of command call times

intents = discord.Intents.all()
client = discord.Client(intents=intents)

cmd_call_times = {}

################################################################

# Define all config options

user_config = [
    conyaml.Config("language", "en_US", "backticks", "lang_code"),
]

server_config = [
    conyaml.Config("language", "en_US", "backticks", "lang_code"),
    conyaml.Config("prefix", "?", "backticks", "any"),
    conyaml.Config("log", None, "channel_mention", "text_channel"),
    conyaml.Config("mute_role", None, "role_mention", "role"),
]

################################################################

# Define autoreplies

autoreplies = {
    "f": "F",
    "no u": "No u",
    "conax": "Conax is cool",
    "conbot": "Conbot is cool",
}

################################################################

# Define all commands

commands = [
    ################################

    # Info

    # Help
    cmdlib.Command.new(
        "help",
        ["commands"],
        "info",
        ["[command]"],
        [" "],
        []
    ),

    # Info
    cmdlib.Command.new(
        "about",
        ["info", "conbot"],
        "info",
        [],
        [" "],
        []
    ),

    # Status
    cmdlib.Command.new(
        "status",
        ["online", "test"],
        "info",
        [],
        [" "],
        []
    ),

    # Invite
    cmdlib.Command.new(
        "invite",
        [],
        "info",
        [],
        [" "],
        []
    ),

    # Perms
    cmdlib.Command.new(
        "perms",
        ["perm", "permissions", "permission"],
        "info",
        ["[member]"],
        [" "],
        []
    ),

    # Avatar
    cmdlib.Command.new(
        "avatar",
        ["profile-pic", "pfp"],
        "info",
        ["[member]"],
        [" "],
        []
    ),

    ################################

    # Chat

    # RNG
    cmdlib.Command.new(
        "rng",
        ["random", "randint"],
        "chat",
        ["<min>", "<max>"],
        [" "],
        []
    ),

    # Choice
    cmdlib.Command.new(
        "choice",
        ["choose"],
        "chat",
        ["<choices>"],
        [],
        []
    ),

    # Numeral
    cmdlib.Command.new(
        "numeral",
        ["num2word", "num2words"],
        "chat",
        ["<number>"],
        [" "],
        []
    ),

    # Gay
    cmdlib.Command.new(
        "gay",
        ["how-gay", "gay-level", "gay-meter"],
        "chat",
        ["[target]"],
        [],
        []
    ),

    # Penis
    cmdlib.Command.new(
        "penis",
        ["penis-length", "penis-size"],
        "chat",
        ["[target]"],
        [],
        []
    ),

    ################################

    # Tools

    # Emoji
    cmdlib.Command.new(
        "emoji",
        ["emote"],
        "tools",
        ["<name>"],
        [" "],
        []
    ),

    # Translate
    cmdlib.Command.new(
        "translate",
        ["trans"],
        "tools",
        ["<text>"],
        [],
        []
    ),

    # Calc
    cmdlib.Command.new(
        "calc",
        ["eval", "calculate", "evaluate"],
        "tools",
        ["<expression>"],
        [],
        []
    ),

    # Python
    cmdlib.Command.new(
        "python",
        ["py", "execute", "exec", "exe"],
        "tools",
        ["<code>"],
        [],
        []
    ),

    ################################

    # Images

    # Meme
    cmdlib.Command.new(
        "meme",
        ["memes"],
        "images",
        [],
        [" "],
        []
    ),

    ################################

    # Music

    # Join
    cmdlib.Command.new(
        "join",
        ["connect"],
        "music",
        [],
        [" "],
        []
    ),

    # Leave
    cmdlib.Command.new(
        "leave",
        ["quit", "disconnect", "dc"],
        "music",
        [],
        [" "],
        []
    ),

    # Play
    cmdlib.Command.new(
        "play",
        ["p", "song", "music"],
        "music",
        ["<song>"],
        [],
        []
    ),

    # Skip
    cmdlib.Command.new(
        "skip",
        [],
        "music",
        [],
        [" "],
        []
    ),

    # Queue
    cmdlib.Command.new(
        "queue",
        ["song-list"],
        "music",
        [],
        [" "],
        []
    ),

    ################################

    # Moderation

    # Kick
    cmdlib.Command.new(
        "kick",
        [],
        "mod",
        ["<target>"],
        [" "],
        ["kick_members"]
    ),

    # Ban
    cmdlib.Command.new(
        "ban",
        [],
        "mod",
        ["<target>"],
        [" "],
        ["ban_members"]
    ),

    # Unban
    cmdlib.Command.new(
        "unban",
        ["pardon"],
        "mod",
        ["<target>"],
        [" "],
        ["ban_members"]
    ),

    # Warn
    cmdlib.Command.new(
        "warn",
        [],
        "mod",
        ["<target, reason>"],
        [],
        ["manage_messages"]
    ),

    # Warns
    cmdlib.Command.new(
        "warns",
        ["warnings", "warn-list"],
        "mod",
        [],
        [" "],
        []
    ),

    ################################

    # Config

    # User Settings
    cmdlib.Command.new(
        "user-settings",
        ["user-config", "user-options", "settings", "config", "options"],
        "config",
        ["[member]"],
        [" "],
        []
    ),

    # Server Settings
    cmdlib.Command.new(
        "server-settings",
        ["server-config", "server-options", "guild-settings", "guild-config", "guild-options"],
        "config",
        ["[option]", "[value]"],
        [" "],
        []
    ),

    # Language
    cmdlib.Command.new(
        "language",
        ["languages", "lang"],
        "config",
        ["[language]"],
        [" "],
        []
    ),

    ################################

    # Developer

    # Shutdown
    cmdlib.Command.new(
        "shutdown",
        ["exit", "off"],
        "dev",
        [],
        [" "],
        []
    ),

    # Guilds
    cmdlib.Command.new(
        "guilds",
        ["servers", "guild-list", "server-list"],
        "dev",
        [],
        [" "],
        []
    ),

    # Announce
    cmdlib.Command.new(
        "announce",
        [],
        "dev",
        ["<channel, message>"],
        [],
        []
    ),

    # Conscript
    cmdlib.Command.new(
        "conscript",
        ["cscript", "botscript"],
        "dev",
        ["<code>"],
        [],
        []
    ),

    # Google Translate Nonsense
    cmdlib.Command.new(
        "googletrans-nonsense",
        ["googletrans-nonsense"],
        "dev",
        ["<text>"],
        [],
        []
    ),
    ################################
]

################################################################

# Import all commands

for command in commands:

    module_name = command.name.replace("-", "_")
    try:
        try:
            cmd_code = getattr(importlib.import_module(module_name), module_name)
        except:
            cmd_code = getattr(importlib.import_module(f"{module_name}_"), module_name)
    except ModuleNotFoundError:
        cmd_code = getattr(importlib.import_module("wip"), "wip")
    command.code = cmd_code

################################################################

# Periodically check the music player

@tasks.loop(seconds=const.music_loop_time)
async def player_loop():

    await songlib.player_check(client.voice_clients)

################################################################

# Print a message, and set the activity when ready

@client.event
async def on_ready():

    print(f"Bot initialized as {client.user}")
    player_loop.start()

################################################################

# Log all member joins

@client.event
async def on_member_join(member):

    channel_id = conyaml.read_server_config(member.guild.id, "log")
    if channel_id:
        channel = member.guild.get_channel(channel_id)
        text = loclib.Loc.server("text_join_msg", member.guild)
        text.format(member.mention)
        embed = cembed.get_embed(text, author_name=member.name, 
        author_img=member.avatar_url, timestamp=datetime.datetime.now(), footer=False)
        await channel.send(embed=embed)

################################################################

# Log all member leaves

@client.event
async def on_member_remove(member):

    channel_id = conyaml.read_server_config(member.guild.id, "log")
    if channel_id:
        channel = member.guild.get_channel(channel_id)
        text = loclib.Loc.server("text_leave_msg", member.guild)
        text.format(member.mention)
        embed = cembed.get_embed(text, author_name=member.name, 
        author_img=member.avatar_url, timestamp=datetime.datetime.now(), footer=False)
        await channel.send(embed=embed)

################################################################

# Send a first time guild message

@client.event
async def on_guild_join(guild):

    channel = guild.public_updates_channel or guild.system_channel or guild.text_channels[0]
    await channel.send(const.welcome_text)

################################################################

# Check and evaluate messages

@client.event
async def on_message(msg):

    # If the message author is a bot or the message is empty, return
    if msg.author.bot or not msg.content:
        return

    # Get the server command prefix
    prefix = conyaml.read_server_config(msg.guild.id, "prefix")
    prefix = prefix or const.default_prefix

    # If the message is a mention of the bot, send the current prefix
    if utils.mention_id(msg.content.strip()) == client.user.id:
        text = loclib.Loc.member("text_current_prefix", msg.author)
        text.format(prefix)
        await msg.channel.send(text, reference=msg, mention_author=False)
        return

    # Log the message
    await utils.log(msg)

    # Reply if the message is an autoreply trigger
    autoreply = msg.content.strip(" \n\t*_~`>|").lower()
    if autoreply in autoreplies:
        await msg.channel.send(autoreplies[autoreply], reference=msg, mention_author=False)

    # Check for a command
    if msg.content.startswith(prefix) and set(msg.content) != {prefix}:

        # Check if the user isn't spamming commands
        call_time = cmd_call_times.get(msg.author.id, float("-inf"))
        if call_time > time.time() - const.cmd_call_cooldown:
            return

        # Register the call time
        cmd_call_times[msg.author.id] = time.time()

        # Get the command name
        command = msg.content.split(" ")[0]
        command = command[len(prefix):]
        command = command.lower().replace("_", "-")

        # Look for the command, ignore dev commands unless the message author is a dev
        for cmd in commands:

            if cmd.category == "dev" and msg.author.id not in const.devs:
                continue

            if command in cmd.calls:

                # Check if the user has sufficient permissions to use the command
                perms = msg.author.guild_permissions
                perms = dict(iter(perms))
                perms = [perms[perm] for perm in cmd.perms]
                if not all(perms):
                    text = loclib.Loc.member("err_missing_perms_user", msg.author)
                    embed = cembed.get_cembed(msg, text)
                    await msg.channel.send(embed=embed, reference=msg, mention_author=False)
                    return

                # Create a list of command parts, and get the amount of specified arguments
                try:
                    parts = msg.content.split(" ")
                    parts = " ".join(parts[1:])
                    for delimiter in cmd.delimiters:
                        parts = parts.replace(delimiter, "$<|sep;|>")
                    parts = parts.split("$<|sep;|>")
                except:
                    parts = []
                parts = parts if parts != [""] else []
                arg_count = len(parts)

                # Get the minimum amount of arguments
                min_args = 0
                for arg in cmd.args:
                    if arg.startswith("<"):
                        min_args += 1

                # Check if the amount of arguments isn't too large
                if arg_count > len(cmd.args):
                    text = loclib.Loc.member("err_arg_overflow", msg.author)
                    max_args = len(cmd.args)
                    none = loclib.Loc.member("label_none", msg.author)
                    max_args = max_args if max_args > 0 else str(none).lower()
                    text.format(str(arg_count), str(max_args))
                    embed = cembed.get_cembed(msg, text)
                    await msg.channel.send(embed=embed, reference=msg, mention_author=False)
                    return

                # Check if the amount of arguments isn't too small
                if arg_count < min_args:
                    text = loclib.Loc.member("err_arg_underflow", msg.author)
                    text.format(arg_count, min_args)
                    embed = cembed.get_cembed(msg, text)
                    await msg.channel.send(embed=embed, reference=msg, mention_author=False)
                    return

                # Create a dictionary of arguments
                args = {}
                for i in range(len(cmd.args)):
                    arg_name = cmd.args[i].strip("<>[]")
                    try:
                        args[arg_name] = parts[i]
                    except IndexError:
                        args[arg_name] = None

                # Call the command, handle all possible errors and send/print the respective error message
                ctx = cmdlib.Context(client, msg, prefix, args, commands, user_config, server_config)
                try:
                    await cmd.code(ctx)

                except cmdlib.CmdError as error:
                    format_args = error.args[1:]
                    text = loclib.Loc.member(error.args[0], msg.author)
                    text.format(*format_args)
                    embed = cembed.get_cembed(msg, text)
                    await msg.channel.send(embed=embed, reference=msg, mention_author=False)

                except discord.errors.Forbidden as error:
                    if str(error).endswith("Missing Permissions"):
                        text = loclib.Loc.member("err_missing_perms_bot", msg.author)
                        embed = cembed.get_cembed(msg, text)
                        await msg.channel.send(embed=embed, reference=msg, mention_author=False)

                except:
                    error = traceback.format_exc()
                    print(error)

                return

        # Find a close match between the entered command and the list of command calls, if there isn't any, display the default unknown command message
        calls = sum([cmd.calls for cmd in commands if cmd.category != "dev"], [])
        try:
            match = difflib.get_close_matches(command, calls, 1, const.cmd_help_min_diff)[0]
            text = loclib.Loc.member("err_unknown_cmd_alt", msg.author)
            text.format(prefix, match)
        except IndexError:
            text = loclib.Loc.member("err_unknown_cmd", msg.author)
            text.format(prefix)

        # Send the unknown command message
        embed = cembed.get_cembed(msg, text)
        await msg.channel.send(embed=embed, reference=msg, mention_author=False)
        return

################################################################

# Run the bot, catch HTTP Exceptions

try:
    client.run(const.token)
except discord.errors.HTTPException as error:
    print(error.response)

################################################################
