################################################################

"""
Conbot - Made by Conax

If you find any bugs, or if you have any suggestions, please contact me. My Discord is Conax#1337.

By using this software, you agree to the license terms in the LICENSE.txt file.
"""

################################################################

# Note - Discord.py API Documentation: https://discordpy.readthedocs.io/en/latest/api.html

################################################################

from server import init
from pyexecute import PyExecute
from conexecute import ConExecute
import discord
import asyncio
import os
import sys
import yaml
import datetime
import random
import re
import urllib
import difflib
import traceback
import googletrans
import youtube_dl

################################################################

# General Constants

# TODO: Make separate config file(s) for most constants

token = os.environ.get("DISCORD_BOT_TOKEN")

loop_interval = 1

default_prefix = "?"
default_embed_color = 0x20a0e0
default_reply_chance = 0.3333

# This is an important workaround for the play function to send messages properly

play_text_output = {}

# Never use filenames directly, instead add any files used in the code to this dict and get the value

files = {
    "log": "log.txt",
    "server_config": "server_config.yaml",
    "user_config": "user_config.yaml",
    "server_activity": "server_activity.yaml",
    "pyexecute": "execute.py",
    "pycalc": "calc.py"
}

loc_files = {
    "en_US": "localization/en_US.yaml",
    "en_GB": "localization/en_GB.yaml",
    "cs_CZ": "localization/cs_CZ.yaml"
}

song_dir = "songs"

# Devs have access to all commands, this is a VERY DANGEROUS permission

devs = [
    209607873787985920 # Conax
]

# The bot has to get all intents to properly function

intents = discord.Intents.all()
client = discord.Client(intents=intents)

################################################################

# Converts a mention string (for example: <@!620175026972393472>) to user id

def mention_id(mention):

    str_id = mention.strip("<@!>")
    try:
        return int(str_id)
    except:
        return 0

################################################################

# Gets the current date in a DD/MM/YYYY format

def date(offset=datetime.timedelta()):

    datetime_now = datetime.datetime.now()
    datetime_now += offset
    day = f"{datetime_now.day:02d}"
    month = f"{datetime_now.month:02d}"
    date_str = f"{day}/{month}/{datetime_now.year}"
    return date_str

# Gets the current time in a HH:MM format

def time(offset=datetime.timedelta()):

    datetime_now = datetime.datetime.now()
    datetime_now += offset
    hour = f"{datetime_now.hour:02d}"
    minute = f"{datetime_now.minute:02d}"
    time_str = f"{hour}:{minute}"
    return time_str

################################################################

# Loads YAML data from a file

def load_yaml(file):

    with open(file, "r") as f:
        data = yaml.load(f, Loader=yaml.FullLoader)
    return data

# Saves YAML data to a file

def save_yaml(file, data):

    with open(file, "w") as f:
        f.write(yaml.dump(data, default_flow_style=False))

################################################################

# Reads YAML config option from a file

def read_config(file, id, option):

    data = load_yaml(file)
    try:
        return data[id][option]
    except Exception:
        return None

# Sets YAML config option to a file

def set_config(file, id, option, value):

    data = load_yaml(file)
    data = {} if not data else data
    if id not in data.keys():
        data[id] = {}
    data[id][option] = value
    save_yaml(file, data)

################################################################

# Reads user config

def read_user_config(user_id, option):

    return read_config(files["user_config"], user_id, option)

# Sets user config

def set_user_config(user_id, option, value):

    set_config(files["user_config"], user_id, option, value)

# Reads server config

def read_server_config(server_id, option):

    return read_config(files["server_config"], server_id, option)

# Sets server config

def set_server_config(server_id, option, value):

    set_config(files["server_config"], server_id, option, value)

################################################################

# Loads a localization file

def load_localization(lang):

    loc = load_yaml(loc_files[lang])
    loc = loc[f"loc_{lang}"]
    return loc

################################################################

# Logs a message to a text file

async def log(msg):

    with open(files["log"], "a") as f:
        space_length = max(len(date()), len(msg.guild.name), len(msg.channel.name), len(str(msg.author)))
        spacing = lambda string: " " * (space_length - len(string))
        msg_datetime = f"{date()}{spacing(date())} | {time()} UTC"
        f.write("\n--------------------------------")
        f.write(f"\n[{msg_datetime}]")
        f.write(f"\n[{msg.guild.name}{spacing(msg.guild.name)} | {msg.guild.id}]")
        f.write(f"\n[#{msg.channel.name}{spacing(msg.channel.name)}| {msg.channel.id}]")
        f.write(f"\n[{msg.author}{spacing(str(msg.author))} | {msg.author.id}]")
        f.write(f"\n{msg.content}")
        f.write("\n--------------------------------\n")

################################################################

# Gets the amount of songs in the queue

def queue_length(guild):

    try:
        path = f"{song_dir}/{guild.id}"
        return len(os.listdir(path))
    except FileNotFoundError:
        return 0

################################################################

# Gets the path of the song in the specified position

def get_song_path(guild, position):

    path = f"{song_dir}/{guild.id}"
    songs = os.listdir(path)
    for song in songs:
        song_position = song.split("$<|sep;|>")[0]
        if int(song_position) == position:
            return f"{path}/{song}"

################################################################

# Downloads a song from YouTube and saves it the specified path

async def download_song(guild, name, position):

    name = urllib.parse.quote(name, safe="")
    search_url = f"https://www.youtube.com/results?search_query={name}"
    html = urllib.request.urlopen(search_url)
    html = html.read().decode()
    videos = re.findall(r"watch\?v=(\S{11})", html)
    url = f"https://www.youtube.com/watch?v={videos[0]}"

    path = f"{song_dir}/{guild.id}/{position}$<|sep;|>%(title)s.%(ext)s"

    ydl_options = {
        "format": "bestaudio/best",
        "outtmpl": path,
        "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
        }]
    }

    with youtube_dl.YoutubeDL(ydl_options) as ydl:
        ydl.download([url])

################################################################

# Deletes the first song in the queue and shifts the queue

async def shift_queue(guild):

    path = f"{song_dir}/{guild.id}"
    song_amount = queue_length(guild)
    if song_amount <= 1:
        os.system(f"rm -rf {path}")
        os.mkdir(f"{path}")

    else:
        os.remove(get_song_path(guild, 1))
        for i in range(2, song_amount + 1):
            path = get_song_path(guild, i)
            song_name = path.split("$<|sep;|>")[1]
            song_name = f"$<|sep;|>{song_name}"
            path = f"{song_dir}/{guild.id}/"
            os.rename(f"{path}{i}{song_name}", f"{path}{i - 1}{song_name}")

################################################################

# Creates an embed

def get_embed(text, title=None, url=None, author_name=None, author_img=None, timestamp=None, fields={}, fields_inline=False, color=None):

    color = color if color else default_embed_color
    embed = discord.Embed(description=str(text), colour=color)

    if title:
        embed.title = str(title)

    if url:
        embed.url = url

    if author_name and author_img:
        embed.set_author(name=author_name, icon_url=str(author_img))

    if timestamp:
        embed.timestamp = timestamp

    for field in fields.items():
        field = list(field)
        field[0] = "\u200b" if str(field[0]).isspace() else str(field[0])
        field[1] = "\u200b" if str(field[1]).isspace() else str(field[1])
        embed.add_field(name=field[0], value=field[1], inline=fields_inline)

    embed.set_footer(text=f"{time()} UTC", icon_url="http://conax.cz/conbot/embed_clock.png")
    return embed

# Creates an embed using information obtained from the message

def get_cembed(msg, text, title=None, url=None, author_name=None, author_img=None, timestamp=None, fields={}, fields_inline=False):

    return get_embed(text, title, url, author_name, author_img, timestamp, fields, fields_inline, msg.author.color)

################################################################

# Class for localization strings

class Loc:

    def __init__(self, name, lang, values=[]):

        self.name = name
        self.lang = lang
        self.values = values

    def format(self, *args):

        self.values = list(args)

    def __repr__(self):

        string = loc_dict[self.lang][self.name]
        for i in range(len(self.values)):
            string = string.replace(f"${i+1}", str(self.values[i]))
        return string

    def __str__(self):

        return repr(self)

    def __add__(self, obj):

        return str(self) + str(obj)
    
    def __len__(self):

        return len(str(self))

    def replace(self, old, new, count=9999):

        return str(self).replace(old, new, count)

    @classmethod
    def server(cls, name, server):

        lang = read_server_config(server.id, "language")
        lang = lang if lang else "en_US"
        return cls(name, lang)

    @classmethod
    def member(cls, name, member):

        lang = read_user_config(member.id, "language")
        lang = lang if lang else read_server_config(member.guild.id, "language")
        lang = lang if lang else "en_US"
        return cls(name, lang)

# Config class for user and server config

class Config:

    def __init__(self, name, default, ftype):

        self.name = name
        self.default = default
        self.ftype = ftype
    
    def format(self, value):

        value = value if value else self.default
        fvalue = None

        if self.ftype == "hex_str":
            value = hex(value)
            hex_number = value[2:].upper()
            zero_count = 8 - len(value)
            fvalue = "#" + str(0) * zero_count + hex_number
            fvalue = f"`{fvalue}`"

        elif self.ftype == "channel_mention":
            fvalue = f"<#{value}>"

        elif self.ftype == "backticks":
            fvalue = f"`{value}`"

        elif self.ftype == "default":
            fvalue = value

        return fvalue if fvalue else None

# Class for commands

class Command:

    def __init__(self, name, calls, category, args, delimiters, perms, desc, code, dev):

        self.name = name
        self.calls = calls
        self.category = category
        self.args = args
        self.delimiters = delimiters
        self.perms = perms
        self.desc = desc
        self.code = code
        self.dev = dev

    @classmethod
    def new(cls, name, aliases, category, args, delimiters, perms, code, dev=False):

        aliases.append(name)
        desc = name.replace("-", "_")
        return cls(name, aliases, category, args, delimiters, perms, desc, code, dev)

# Class for command context

class Context:

    def __init__(self, msg, prefix, args):

        self.msg = msg
        self.author = msg.author
        self.guild = msg.guild
        self.channel = msg.channel
        self.prefix = prefix
        self.args = args

################################################################

# Info

################################################################

async def help(ctx):

    command = ctx.args["command"]

    if not command:

        cmd_list = {}
        for cmd in commands:
            if cmd.category not in cmd_list.keys():
                cmd_list[cmd.category] = []
            cmd_list[cmd.category].append(cmd.name)
        cmd_list.pop("dev", None)

        prefix_text = Loc.member("text_help_prefix", ctx.author)
        prefix_text.format(ctx.prefix)
        title = Loc.member("label_help", ctx.author)

        category_list = {}
        for category in cmd_list.items():
            category_name = Loc.member(f"cmd_category_{category[0]}", ctx.author)
            cmd_str = "`, `".join(category[1])
            category_list[category_name] = f"`{cmd_str}`"

        embed = get_cembed(ctx.msg, f"{prefix_text}\n", title, fields=category_list)

    else:

        cmd = None
        for command in commands:
            arg_cmd = ctx.args["command"].lower().replace("_", "-")
            if arg_cmd.lstrip(ctx.prefix) in command.calls:
                cmd = command
        
        if not cmd or cmd.category == "dev":
            text = Loc.member("err_help_unknown_cmd", ctx.author)
            embed = get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)
            return

        fields = {}
        none = Loc.member("label_none", ctx.author)

        syntax = Loc.member("label_syntax", ctx.author)
        cmd_call = f"{ctx.prefix}{cmd.name}"
        args = " ".join(cmd.args)
        cmd_syntax = f"{cmd_call} {args}"
        fields[syntax] = f"`{cmd_syntax.strip()}`"
        
        aliases = Loc.member("label_aliases", ctx.author)
        alias_list = [f"`{call}`" for call in cmd.calls if call != cmd.name]
        cmd_aliases = ", ".join(alias_list)
        fields[aliases] = cmd_aliases if cmd_aliases != "" else none

        req_perms = Loc.member("label_req_perms", ctx.author)
        perms = []
        for perm in cmd.perms:
            perm_name = Loc.member(f"perm_{perm}", ctx.author)
            perms.append(str(perm_name))
        perms_text = ", ".join(perms)
        fields[req_perms] = perms_text if perms != [] else none

        desc_title = Loc.member("label_desc", ctx.author)
        desc = Loc.member(f"cmd_desc_{cmd.desc}", ctx.author)
        fields[desc_title] = desc

        embed = get_cembed(ctx.msg, "", cmd_call, fields=fields)

    await ctx.channel.send(embed=embed)

################################################################

async def status(ctx):

    online_msg = Loc.member("text_status_online", ctx.author)
    embed = get_cembed(ctx.msg, online_msg)
    await ctx.channel.send(embed=embed)

################################################################

async def invite(ctx):

    invite = await ctx.channel.create_invite(max_age=0, max_uses=0, unique=False)
    invite_link = Loc.member("label_invite_link", ctx.author)
    embed = get_cembed(ctx.msg, invite.url, invite_link, author_name=ctx.guild.name, author_img=ctx.guild.icon_url)
    await ctx.channel.send(embed=embed)

################################################################

async def perms(ctx):

    if not ctx.args["member"]:
        member = ctx.guild.get_member(ctx.author.id)
    else:
        member_id = mention_id(ctx.args["member"])
        member = ctx.guild.get_member(member_id)
        if not member:
            text = Loc.member("err_unknown_member", ctx.author)
            text.format(client.user.mention)
            embed = get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)
            return
    perms = member.guild_permissions

    perm_list = ["administrator", "view_channel", "manage_channels", "manage_roles", "manage_emojis", "view_audit_log", "manage_webhooks", "manage_guild"]
    perm_list += ["send_messages", "embed_links", "attach_files", "add_reactions", "external_emojis", "mention_everyone", "manage_messages", "read_message_history", "send_tts_messages", "use_slash_commands"]
    perm_list += ["create_instant_invite", "change_nickname", "manage_nicknames", "kick_members", "ban_members"]
    perm_list += ["connect", "speak", "stream", "use_voice_activation", "priority_speaker", "mute_members", "deafen_members", "move_members"]

    fields = {}
    for perm in perm_list:
        enabled = "**[Yes]" if getattr(perms, perm) else "**[No]"
        enabled += "(https://discord.com/developers/docs/topics/permissions)**"
        name = Loc.member(f"perm_{perm}", ctx.author)
        fields[name] = enabled

    perms_text = Loc.member("text_perms_list", ctx.author)
    perms_text.format(member.mention)
    perms_title = Loc.member("text_perms_title", ctx.author)
    perms_title.format(ctx.guild.name)

    embed = get_cembed(ctx.msg, perms_text, perms_title, author_name=member.name, author_img=member.avatar_url, fields=fields, fields_inline=True)
    await ctx.channel.send(embed=embed)

################################################################

# Chat

################################################################

async def rng(ctx):

    try:
        min_num, max_num = ctx.args["min"], ctx.args["max"]
        min_num, max_num = int(min_num.strip(", ")), int(max_num.strip(", "))
        text = ""
        if min_num > max_num:
            text = Loc.member("err_rng_range_larger", ctx.author)
        if min_num == max_num:
            text = Loc.member("err_rng_range_equal", ctx.author)

    except ValueError:
        text = Loc.member("err_rng_no_floats", ctx.author)

    if text != "":
        embed = get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return
    
    number = random.randint(min_num, max_num)
    embed = get_cembed(ctx.msg, str(number))
    await ctx.channel.send(embed=embed)

################################################################

async def choice(ctx):

    delimiter = ","
    choices = ctx.args["choices"].split(delimiter)
    if len(choices) < 2:
        text = Loc.member("err_choice_not_enough", ctx.author)
        text.format(delimiter)
    else:
        text = random.choice(choices)
    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

async def gay(ctx):

    target = ctx.args["target"]
    target = target if target else ctx.author.mention
    gay_percent = random.randint(0, 100)
    gay_text = Loc.member("text_gay", ctx.author)
    gay_text.format(target, gay_percent)
    gay_meter = Loc.member("label_gay_meter", ctx.author)
    embed = get_cembed(ctx.msg, gay_text, gay_meter)
    await ctx.channel.send(embed=embed)

################################################################

async def penis(ctx):

    target = ctx.args["target"]
    target = target if target else ctx.author.mention
    penis = f"8{'=' * random.randint(0, 10)}>"
    penis_text = Loc.member("text_penis", ctx.author)
    penis_text.format(target, penis)
    penis_length = Loc.member("label_penis_length", ctx.author)
    embed = get_cembed(ctx.msg, penis_text, penis_length)
    await ctx.channel.send(embed=embed)

################################################################

# Tools

################################################################

async def translate(ctx):

    translator = googletrans.Translator()
    translation = translator.translate(ctx.args["text"])
    source, dest = translation.src, translation.dest

    text = Loc.member("text_translate", ctx.author)
    text.format(source, dest)
    text += f"\n\n```{translation.text}```"
    title = Loc.member("label_translate", ctx.author)

    embed = get_cembed(ctx.msg, text, title)
    await ctx.channel.send(embed=embed)

################################################################

async def calc(ctx):

    expr = ctx.args["expression"]
    expr = expr.strip(" `\n").replace("^", "**").replace("\n", " ")
    allowed_chars = " \t0123456789.+-*/%"
    text = None

    for char in expr:
        if char not in allowed_chars:
            text = Loc.member("err_calc_bannned_char", ctx.author)

    if not text:
        err_timeout = Loc.member("err_calc_timeout", ctx.author)
        exec_loc = {"err_exec_timeout": err_timeout, "err_exec_banned_module": "", "err_exec_banned_keyword": ""}
        pyexecute = PyExecute(files["pycalc"], exec_loc)
        text = pyexecute.execute(f"print({expr})")
        
        err_syntax = Loc.member("err_calc_syntax_error", ctx.author)
        text = text if "Error" not in text else err_syntax
        text = text if len(text) <= 2000 else text[:2000]

    title = Loc.member("label_result", ctx.author)
    embed = get_cembed(ctx.msg, f"```{text}```", title)
    await ctx.channel.send(embed=embed)

################################################################

async def python(ctx):

    code = ctx.args["code"]
    code = code.strip(" `\n")
    if code.startswith("python"):
        code = code[6:]
    elif code.startswith("py"):
        code = code[2:]

    exec_loc = {}
    for loc_name in ["err_exec_timeout", "err_exec_banned_module", "err_exec_banned_keyword"]:
        exec_loc[loc_name] = Loc.member(loc_name, ctx.author)

    pyexecute = PyExecute(files["pyexecute"], exec_loc)
    output = pyexecute.execute(code)
    output = output if len(output) <= 2000 else output[:2000]

    title = Loc.member("label_output", ctx.author)
    embed = get_cembed(ctx.msg, f"```{output}```", title)
    await ctx.channel.send(embed=embed)

################################################################

# Music

################################################################

async def join(ctx):

    voice = ctx.author.voice

    if not voice:
        text = Loc.member("err_join_no_voice", ctx.author)
    
    else:
        bot_channel = None
        for bot_voice in client.voice_clients:
            if bot_voice.guild == ctx.guild:
                bot_channel = bot_voice

        if not bot_channel:
            await voice.channel.connect()
            text = Loc.member("text_join", ctx.author)
            text.format(voice.channel)
        else:
            text = Loc.member("err_join_voice_connected", ctx.author)

    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

async def leave(ctx):

    voices = client.voice_clients
    text = Loc.member("err_leave_no_voice", ctx.author)

    for voice in voices:
        if voice.guild == ctx.guild:
            path = f"{song_dir}/{voice.guild.id}"
            await voice.disconnect()
            os.system(f"rm -rf {path}")
            
            text = Loc.member("text_leave", ctx.author)
            text.format(voice.channel)

    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

async def play(ctx):

    voice = ctx.author.voice

    if not voice:
        text = Loc.member("err_join_no_voice", ctx.author)
        embed = get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return
    
    else:
        bot_channel = None
        for bot_voice in client.voice_clients:
            if bot_voice.guild == ctx.guild:
                bot_channel = bot_voice

        if not bot_channel:
            await voice.channel.connect()
            text = Loc.member("text_join", ctx.author)
            text.format(voice.channel)
            embed = get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)

    voices = client.voice_clients

    for voice in voices:
        if voice.guild == ctx.guild:
            text = Loc.member("text_play_downloading", ctx.author)
            embed = get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)
            position = queue_length(ctx.guild) + 1
            await download_song(ctx.guild, ctx.args["song"], position)

    global play_text_output
    play_text_output[ctx.guild.id] = ctx.channel
    path = get_song_path(ctx.guild, position)
    song_name = path.split("$<|sep;|>")[1].replace(".mp3", "")

    if queue_length(ctx.guild) == 1:
        voice.play(discord.FFmpegPCMAudio(path))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.25

        text = Loc.server("text_play_playing", ctx.guild)
        text.format(song_name)

    else:
        text = Loc.server("text_play_add_queue", ctx.guild)
        text.format(song_name)

    embed = get_embed(text)
    await ctx.channel.send(embed=embed)

################################################################

async def skip(ctx):

    voices = client.voice_clients
    text = Loc.member("err_skip_not_playing", ctx.author)
    embed = get_cembed(ctx.msg, text)

    for voice in voices:
        if voice.guild == ctx.guild:
            song_amount = queue_length(ctx.guild)
            if song_amount >= 1:
                voice.stop()
                await shift_queue(ctx.guild)
                if song_amount - 1 >= 1:

                    path = get_song_path(voice.guild, 1)
                    song_name = path.split("$<|sep;|>")[1].replace(".mp3", "")

                    voice.play(discord.FFmpegPCMAudio(path))
                    voice.source = discord.PCMVolumeTransformer(voice.source)
                    voice.source.volume = 0.25

                    text = Loc.server("text_play_playing", voice.guild)
                    text.format(song_name)
                    embed = get_embed(text)

    await ctx.channel.send(embed=embed)

################################################################

# Moderation

################################################################

async def kick(ctx):

    target_id = mention_id(ctx.args["target"])
    target = ctx.guild.get_member(target_id)
    text = ""

    if not target:
        text = Loc.member("err_unknown_member", ctx.author)
        text.format(client.user.mention)
    elif target.top_role >= ctx.author.top_role:
        text = Loc.member("err_kick_perms_author", ctx.author)
    if text != "":
        embed = get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return

    reason = Loc.member("text_kick_reason", ctx.author)
    reason.format(ctx.author)
    await target.kick(reason=reason)
    text = Loc.member("text_kick_success", ctx.author)
    target_mention = f"<@!{target_id}>"
    text.format(target_mention)

    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

async def ban(ctx):

    target_id = mention_id(ctx.args["target"])
    target = ctx.guild.get_member(target_id)
    text = ""

    if not target:
        text = Loc.member("err_unknown_member", ctx.author)
        text.format(client.user.mention)
    elif target.top_role >= ctx.author.top_role:
        text = Loc.member("err_ban_perms_author", ctx.author)
    if text != "":
        embed = get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return

    reason = Loc.member("text_ban_reason", ctx.author)
    reason.format(ctx.author)
    await target.ban(reason=reason)
    text = Loc.member("text_ban_success", ctx.author)
    target_mention = f"<@!{target_id}>"
    text.format(text, [target_mention])

    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

# Config

################################################################

async def user_settings(ctx):

    target_mention = ctx.args["member"]
    target = ctx.author
    if target_mention:
        target_id = mention_id(target_mention)
        if target_id != 0:
            target = ctx.guild.get_member(target_id)

    if not target:
        text = Loc.member("err_unknown_member", ctx.author)
        text.format(client.user.mention)
        embed = get_cembed(ctx.msg, text)
        ctx.channel.send(embed=embed)
        return

    fields = {}
    for config in user_config:
        name = Loc.member(f"config_{config.name}", ctx.author)
        value = read_user_config(target.id, config.name)
        value = config.format(value)
        fields[name] = value

    title = Loc.member("label_user_config", ctx.author)
    embed = get_cembed(ctx.msg, "", title, author_name=target.name, author_img=target.avatar_url, fields=fields, fields_inline=True)
    await ctx.channel.send(embed=embed)

################################################################

async def server_settings(ctx):

    fields = {}
    for config in server_config:
        name = f"config_{config.name}"
        name = Loc.member(name, ctx.author)
        value = read_server_config(ctx.guild.id, config.name)
        value = config.format(value)
        fields[name] = value

    title = Loc.member("label_server_config", ctx.author)
    embed = get_cembed(ctx.msg, "", title, author_name=ctx.guild.name, author_img=ctx.guild.icon_url, fields=fields, fields_inline=True)
    await ctx.channel.send(embed=embed)

################################################################

async def language(ctx):

    lang = ctx.args["language"]

    if not lang:

        fields = {}
        for language in loc_files.keys():
            lang_name = loc_dict[language]["language_name"]
            lang_code = f"`{language}`"
            fields[lang_name] = lang_code
        
        text = Loc.member("text_lang_list", ctx.author)
        title = Loc.member("label_languages", ctx.author)
        embed = get_cembed(ctx.msg, text, title, fields=fields)
    
    else:

        lang = lang.replace("-", "_")
        if lang in loc_files.keys():
            set_user_config(ctx.author.id, "language", lang)
            text = Loc.member("text_lang_changed", ctx.author)

        else:
            text = Loc.member("err_unknown_lang", ctx.author)
        
        embed = get_cembed(ctx.msg, text)

    await ctx.channel.send(embed=embed)

################################################################

# Dev

################################################################

async def shutdown(ctx):

    text = Loc.member("text_exit", ctx.author)
    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)
    def crash():
        try:
            crash()
        except:
            crash()
    crash()

################################################################

async def conscript(ctx):

    code = ctx.args["code"]
    code = code.strip(" `\n")

    conexecute = ConExecute(client, ctx)
    output = await conexecute.execute(code)
    output = output if len(output) <= 2000 else output[:2000]

    title = Loc.member("label_output", ctx.author)
    embed = get_cembed(ctx.msg, f"```{output}```", title)
    await ctx.channel.send(embed=embed)

################################################################

async def guilds(ctx):

    guild_names = [str(guild) for guild in client.guilds]
    text = "\n".join(guild_names)
    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

# Misc

################################################################

async def wip(ctx):

    text = Loc.member("text_wip", ctx.author)
    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

# Preloads the localization files

loc_dict = {lang:load_localization(lang) for lang in loc_files.keys()}

################################################################

# Config options

user_config = [
    Config("language", "en_US", "backticks")
]

server_config = [
    Config("language", "en_US", "backticks"),
    Config("log_channel", None, "channel_mention")
]

################################################################

# List of commands

commands = [
    # Info

    # Help
    Command.new(
        "help",
        ["commands"],
        "info",
        ["[command]"],
        [" "],
        [],
        help
    ),

    # Status
    Command.new(
        "status",
        ["online", "test"],
        "info",
        [],
        [" "],
        [],
        status
    ),

    # Invite
    Command.new(
        "invite",
        [],
        "info",
        [],
        [" "],
        [],
        invite
    ),

    # Perms
    Command.new(
        "perms",
        ["perm", "permissions", "permission"],
        "info",
        ["[member]"],
        [" "],
        [],
        perms
    ),

    # Chat

    # RNG
    Command.new(
        "rng",
        ["random", "randint"],
        "chat",
        ["<min>", "<max>"],
        [" "],
        [],
        rng
    ),

    # Choice
    Command.new(
        "choice",
        ["choose"],
        "chat",
        ["<choices>"],
        ["$<|no_delimiter;|>"],
        [],
        choice
    ),

    # Gay
    Command.new(
        "gay",
        ["how-gay", "gay-level", "gay-meter"],
        "chat",
        ["[target]"],
        ["$<|no_delimiter;|>"],
        [],
        gay
    ),

    # Penis
    Command.new(
        "penis",
        ["penis-length", "penis-size"],
        "chat",
        ["[target]"],
        ["$<|no_delimiter;|>"],
        [],
        penis
    ),

    # Tools

    # translate
    Command.new(
        "translate",
        ["trans"],
        "tools",
        ["<text>"],
        ["$<|no_delimiter;|>"],
        [],
        translate
    ),

    # Calc
    Command.new(
        "calc",
        ["eval", "calculate", "evaluate"],
        "tools",
        ["<expression>"],
        ["$<|no_delimiter;|>"],
        [],
        calc
    ),

    # Python
    Command.new(
        "python",
        ["py", "execute", "exec", "exe"],
        "tools",
        ["<code>"],
        ["$<|no_delimiter;|>"],
        [],
        python
    ),

    # Music

    # Join
    Command.new(
        "join",
        ["connect"],
        "music",
        [],
        [" "],
        [],
        join
    ),

    # Leave
    Command.new(
        "leave",
        ["quit", "disconnect", "dc"],
        "music",
        [],
        [" "],
        [],
        leave
    ),

    # Play
    Command.new(
        "play",
        ["song", "music"],
        "music",
        ["<song>"],
        ["$<|no_delimiter;|>"],
        [],
        play
    ),

    # Skip
    Command.new(
        "skip",
        [],
        "music",
        [],
        [" "],
        [],
        skip
    ),

    # Moderation

    # Kick
    Command.new(
        "kick",
        [],
        "mod",
        ["<target>"],
        [" "],
        ["kick_members"],
        kick
    ),

    # Ban
    Command.new(
        "ban",
        [],
        "mod",
        ["<target>"],
        [" "],
        ["ban_members"],
        ban
    ),

    # Config

    # User Settings
    Command.new(
        "user-settings",
        ["user-config", "user-options", "settings", "config", "options"],
        "config",
        ["[member]"],
        [" "],
        [],
        user_settings
    ),

    # Server Settings
    Command.new(
        "server-settings",
        ["server-config", "server-options"],
        "config",
        [],
        [" "],
        [],
        server_settings
    ),

    # Language
    Command.new(
        "language",
        ["languages", "lang"],
        "config",
        ["[language]"],
        [" "],
        [],
        language
    ),

    # Developer
    
    # Exit
    Command.new(
        "exit",
        ["shutdown", "off"],
        "dev",
        [],
        [" "],
        [],
        shutdown,
        True
    ),

    # ConScript
    Command.new(
        "conscript",
        ["cscript", "conbot-script"],
        "dev",
        ["<code>"],
        ["$<|no_delimiter;|>"],
        [],
        conscript,
        True
    ),

    # Guilds
    Command.new(
        "guilds",
        ["servers", "guild-list", "server-list"],
        "dev",
        [],
        [" "],
        [],
        guilds,
        True
    )

]

################################################################

# Loop that keeps checking various things

async def loop():

    while True:

        # Disconnect from empty voice channels

        voices = client.voice_clients
        for voice in voices:
            if len(voice.channel.members) <= 1:
                path = f"{song_dir}/{voice.guild.id}"
                await voice.disconnect()
                os.system(f"rm -rf {path}")
                os.mkdir(path)

            # Check if the song finished playing and starts a new song

            if not voice.is_playing() and not voice.is_paused():

                song_amount = queue_length(voice.guild)
                if song_amount >= 1:
                    await shift_queue(voice.guild)
                    if song_amount - 1 >= 1:

                        path = get_song_path(voice.guild, 1)
                        song_name = path.split("$<|sep;|>")[1].replace(".mp3", "")

                        voice.play(discord.FFmpegPCMAudio(path))
                        voice.source = discord.PCMVolumeTransformer(voice.source)
                        voice.source.volume = 0.25

                        text = Loc.server("text_play_playing", voice.guild)
                        text.format(song_name)
                        embed = get_embed(text)
                        text_channel = play_text_output[voice.guild.id]
                        await text_channel.send(embed=embed)

        # Updates the bot activity

        status = discord.Status.online
        activity_name = f"{len(client.guilds)} servers"
        activity_type = discord.ActivityType.watching
        activity = discord.Activity(name=activity_name, type=activity_type)
        await client.change_presence(status=status, activity=activity)

        # Wait between check turns

        await asyncio.sleep(loop_interval)

################################################################

# Prints a message, clears the song directory, and sets the activity when ready

@client.event
async def on_ready():

    print(f"Bot initialized as {client.user}")
    os.system(f"rm -rf {song_dir}")
    os.mkdir(song_dir)
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

    channel_id = read_server_config(member.guild.id, "log_channel")
    if channel_id:
        channel = member.guild.get_channel(channel_id)
        text = Loc.server("text_join_msg", member.guild)
        text.format(member.mention)
        embed = get_embed(text, "", author_name=member.name, author_img=member.avatar_url, timestamp=datetime.datetime.now())
        await channel.send(embed=embed)

################################################################

# Logs all member leaves

@client.event
async def on_member_remove(member):

    channel_id = read_server_config(member.guild.id, "log_channel")
    if channel_id:
        channel = member.guild.get_channel(channel_id)
        text = Loc.server("text_leave_msg", member.guild)
        text.format(member.mention)
        embed = get_embed(text, "", author_name=member.name, author_img=member.avatar_url, timestamp=datetime.datetime.now())
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
    text = f"Thanks for adding me to your server!\n\n• The default command prefix is `{default_prefix}`\n• Use `{default_prefix}help` to get a list of available commands\n• Use `{default_prefix}lang` to change your language setting\n• The bot needs a role with administrator permissions to work correctly"
    await channel.send(text)

################################################################

# Checks and evaluates messages

@client.event
async def on_message(msg):

    # If the message author is a bot or the message is empty, return

    if msg.author.bot or msg.content == "":
        return

    # Logs the message

    await log(msg)

    # Gets the server command prefix

    prefix = read_server_config(msg.guild.id, "Prefix")
    prefix = prefix if prefix else default_prefix

    # Checks for a command

    if msg.content.startswith(prefix) and set(msg.content) != {prefix}:

        # Gets the command name

        command = msg.content.split(" ")[0]
        command = command[len(prefix):]
        command = command.lower().replace("_", "-")

        # Looks for the command, ignores dev commands unless the message author is a dev

        for cmd in commands:

            if cmd.category == "dev" and msg.author.id not in devs:
                continue

            if command in cmd.calls:

                # Checks if the user has sufficient permissions to use the command
                
                perms = msg.author.guild_permissions
                perms = dict(iter(perms))
                perms = [perms[perm] for perm in cmd.perms]
                if not all(perms):
                    text = Loc.member("err_missing_perms", msg.author)
                    embed = get_cembed(msg, text)
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
                    text = Loc.member("err_arg_overflow", msg.author)
                    max_args = len(cmd.args)
                    none = Loc.member("label_none", msg.author)
                    max_args = max_args if max_args > 0 else str(none).lower()
                    text.format(str(arg_count), str(max_args))
                    embed = get_cembed(msg, text)
                    await msg.channel.send(embed=embed)
                    return

                # Checks if the amount of arguments isn't too small

                if arg_count < min_args:
                    text = Loc.member("err_arg_underflow", msg.author)
                    text.format(arg_count, min_args)
                    embed = get_cembed(msg, text)
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

                ctx = Context(msg, prefix, args)
                try:
                    await cmd.code(ctx)
                except discord.errors.Forbidden as error:
                    if str(error).endswith("Missing Permissions"):
                        text = Loc.member("err_missing_perms", msg.author)
                        embed = get_cembed(msg, text)
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
            text = Loc.member("err_unknown_cmd_alt", msg.author)
            text.format(prefix, match)
        except IndexError:
            text = Loc.member("err_unknown_cmd", msg.author)
            text.format(prefix)

        # Send the unknown command message

        embed = get_cembed(msg, text)
        await msg.channel.send(embed=embed)
        return

    # TOP SECRET

    if msg.content.startswith("<i-want-to-cum-inside-twilight-sparkle>"):
        server = client.get_guild(486956287293128715)
        channel = server.get_channel(486956287742181421)
        text = msg.content.replace("<i-want-to-cum-inside-twilight-sparkle>", "").strip()
        await channel.send(text)

    # Autoreplies
    # TODO: Change

    """
    if clean(msg.content).lower() in autoreplies.keys() and random.random() < (default_reply_chance if not read_server_config(msg.guild.id, "Reply Chance") else read_server_config(msg.guild.id, "Reply Chance") / 100):
        await msg.channel.send(autoreplies[clean(msg.content).lower()])
    """

################################################################

init()
client.run(token)

################################################################