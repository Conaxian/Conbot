################################################################

"""
Conbot - Made by Conax

If you find any bugs, or if you have any suggestions, please contact me. My Discord is Conax#0001.

By using this software, you agree to the license terms in the LICENSE.txt file.
"""

################################################################

# Note - Discord.py API Documentation: https://discordpy.readthedocs.io/en/latest/api.html

################################################################

# Flask server

from server import init

# All required modules

import discord
import asyncio
import os
import sys
import datetime
import importlib
import difflib
import traceback

# Conbot modules

import constants
import utils
import conyaml
import cembed
import cmdlib
import loclib
import songlib

# Search for modules in the "commands" directory

sys.path.append("commands")

################################################################

# The bot has to get all intents to properly function

intents = discord.Intents.all()
client = discord.Client(intents=intents)

################################################################

# Define all config options

user_config = [
    conyaml.Config("language", "en_US", "backticks", "lang_code")
]

server_config = [
    conyaml.Config("language", "en_US", "backticks", "lang_code"),
    conyaml.Config("prefix", "?", "backticks", "any"),
    conyaml.Config("log", None, "channel_mention", "text_channel")
]

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
        ["song", "music"],
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
    
    # Exit
    cmdlib.Command.new(
        "shutdown",
        ["exit", "off"],
        "dev",
        [],
        [" "],
        [],
        True
    ),

    # Guilds
    cmdlib.Command.new(
        "guilds",
        ["servers", "guild-list", "server-list"],
        "dev",
        [],
        [" "],
        [],
        True
    ),

    # Announce
    cmdlib.Command.new(
        "announce",
        [],
        "dev",
        ["<channel, message>"],
        [],
        [],
        True
    )
    ################################
]

################################################################

# Import all commands

for command in commands:

    module_name = command.name.replace("-", "_")
    try:
        cmd_code = getattr(importlib.import_module(module_name), module_name)
    except ModuleNotFoundError:
        cmd_code = getattr(importlib.import_module("wip"), "wip")
    command.code = cmd_code

################################################################

# Loop that keeps checking for various things

async def loop():

    while True:

        # Disconnect from empty voice channels

        voices = client.voice_clients
        for voice in voices:
            if len(voice.channel.members) <= 1:
                path = f"{constants.song_dir}/{voice.guild.id}"
                await voice.disconnect()
                os.system(f"rm -rf {path}")
                os.mkdir(path)

            # Check if the current song has finished playing and starts a new song

            if not voice.is_playing() and not voice.is_paused():

                song_amount = songlib.queue_length(voice.guild)
                if song_amount >= 1:
                    await songlib.shift_queue(voice.guild)
                    if song_amount - 1 >= 1:

                        path = songlib.get_song_path(voice.guild, 1)
                        song_name = path.split("$<|sep;|>")[1].replace(".mp3", "")

                        voice.play(discord.FFmpegPCMAudio(path))
                        voice.source = discord.PCMVolumeTransformer(voice.source)
                        voice.source.volume = 0.25

                        text = loclib.Loc.server("text_play_playing", voice.guild)
                        text.format(song_name)
                        embed = cembed.get_embed(text)
                        text_channel = songlib.play_text_output[voice.guild.id]
                        await text_channel.send(embed=embed)

        # Updates the bot activity

        status = discord.Status.online
        activity_name = f"{len(client.guilds)} servers"
        activity_type = discord.ActivityType.watching
        activity = discord.Activity(name=activity_name, type=activity_type)
        await client.change_presence(status=status, activity=activity)

        # Wait between check turns

        await asyncio.sleep(constants.loop_interval)

################################################################

# Prints a message, clears the song directory, and sets the activity when ready

@client.event
async def on_ready():

    print(f"Bot initialized as {client.user}")
    os.system(f"rm -rf {constants.song_dir}")
    os.mkdir(constants.song_dir)
    status = discord.Status.online
    activity_name = f"{len(client.guilds)} servers"
    activity_type = discord.ActivityType.watching
    activity = discord.Activity(name=activity_name, type=activity_type)
    await client.change_presence(status=status, activity=activity)
    await client.loop.create_task(loop())

################################################################

# Logs all member joins

@client.event
async def on_member_join(member):

    channel_id = conyaml.read_server_config(member.guild.id, "log_channel")
    if channel_id:
        channel = member.guild.get_channel(channel_id)
        text = loclib.Loc.server("text_join_msg", member.guild)
        text.format(member.mention)
        embed = cembed.get_embed(text, "", author_name=member.name, author_img=member.avatar_url, timestamp=datetime.datetime.now(), footer=False)
        await channel.send(embed=embed)

################################################################

# Logs all member leaves

@client.event
async def on_member_remove(member):

    channel_id = conyaml.read_server_config(member.guild.id, "log_channel")
    if channel_id:
        channel = member.guild.get_channel(channel_id)
        text = loclib.Loc.server("text_leave_msg", member.guild)
        text.format(member.mention)
        embed = cembed.get_embed(text, "", author_name=member.name, author_img=member.avatar_url, timestamp=datetime.datetime.now(), footer=False)
        await channel.send(embed=embed)

################################################################

# Sends a first time guild message

@client.event
async def on_guild_join(guild):

    channel = guild.public_updates_channel
    if not channel:
        channel = guild.system_channel
    if not channel:
        channel = guild.text_channels[0]
    text = f"Thanks for adding me to your server!\n\n• The default command prefix is `{constants.default_prefix}`\n• Use `{constants.default_prefix}help` to get a list of available commands\n• Use `{constants.default_prefix}lang` to change your language setting\n• The bot needs a role with administrator permissions to work correctly"
    await channel.send(text)

################################################################

# Checks and evaluates messages

@client.event
async def on_message(msg):

    # If the message author is a bot or the message is empty, return

    if msg.author.bot or msg.content == "":
        return

    # Logs the message

    await utils.log(msg)

    # Gets the server command prefix

    prefix = conyaml.read_server_config(msg.guild.id, "prefix")
    prefix = prefix if prefix else constants.default_prefix

    # Checks for a command

    if msg.content.startswith(prefix) and set(msg.content) != {prefix}:

        # Gets the command name

        command = msg.content.split(" ")[0]
        command = command[len(prefix):]
        command = command.lower().replace("_", "-")

        # Looks for the command, ignores dev commands unless the message author is a dev

        for cmd in commands:

            if cmd.category == "dev" and msg.author.id not in constants.devs:
                continue

            if command in cmd.calls:

                # Checks if the user has sufficient permissions to use the command
                
                perms = msg.author.guild_permissions
                perms = dict(iter(perms))
                perms = [perms[perm] for perm in cmd.perms]
                if not all(perms):
                    text = loclib.Loc.member("err_missing_perms", msg.author)
                    embed = cembed.get_cembed(msg, text)
                    await msg.channel.send(embed=embed)
                    return

                # Creates a list of command parts and gets the amount of specified arguments

                try:
                    parts = msg.content.split(" ")
                    parts = " ".join(parts[1:])
                    for delimiter in cmd.delimiters:
                        parts = parts.replace(delimiter, "$<|sep;|>")
                    parts = parts.split("$<|sep;|>")
                except Exception:
                    parts = []
                parts = parts if parts != [""] else []
                arg_count = len(parts)

                # Gets the minimum amount of arguments

                min_args = 0
                for arg in cmd.args:
                    if arg.startswith("<"):
                        min_args += 1

                # Checks if the amount of arguments isn't too large

                if arg_count > len(cmd.args):
                    text = loclib.Loc.member("err_arg_overflow", msg.author)
                    max_args = len(cmd.args)
                    none = loclib.Loc.member("label_none", msg.author)
                    max_args = max_args if max_args > 0 else str(none).lower()
                    text.format(str(arg_count), str(max_args))
                    embed = cembed.get_cembed(msg, text)
                    await msg.channel.send(embed=embed)
                    return

                # Checks if the amount of arguments isn't too small

                if arg_count < min_args:
                    text = loclib.Loc.member("err_arg_underflow", msg.author)
                    text.format(arg_count, min_args)
                    embed = cembed.get_cembed(msg, text)
                    await msg.channel.send(embed=embed)
                    return
                
                # Creates a dictionary of arguments

                args = {}
                for i in range(len(cmd.args)):
                    arg_name = cmd.args[i].strip("<>[]")
                    try:
                        args[arg_name] = parts[i]
                    except IndexError:
                        args[arg_name] = None

                # Calls the command, prints an error message if the bot has insufficient permissions

                ctx = cmdlib.Context(client, msg, prefix, args, commands, user_config, server_config)
                try:
                    await cmd.code(ctx)
                except discord.errors.Forbidden as error:
                    if str(error).endswith("Missing Permissions"):
                        text = loclib.Loc.member("err_missing_perms", msg.author)
                        embed = cembed.get_cembed(msg, text)
                        await msg.channel.send(embed=embed)
                except Exception:
                    error = f"```{traceback.format_exc()}```"
                    await msg.channel.send(error)

                return

        # Get the list of command calls (except dev commands)

        calls = []
        for cmd in commands:
            if cmd.category != "dev":
                calls += cmd.calls

        # Find a close match between the entered command and the list of command calls, if there isn't any, display the default unknown command message

        try:
            match = difflib.get_close_matches(command, calls, 1, 0.6)[0]
            text = loclib.Loc.member("err_unknown_cmd_alt", msg.author)
            text.format(prefix, match)
        except IndexError:
            text = loclib.Loc.member("err_unknown_cmd", msg.author)
            text.format(prefix)

        # Send the unknown command message

        embed = cembed.get_cembed(msg, text)
        await msg.channel.send(embed=embed)
        return

################################################################

# Starts the server and runs the bot

init()
client.run(constants.token)

################################################################