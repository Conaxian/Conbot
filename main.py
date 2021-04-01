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
    "pyexecute": "execute.py"
}

localization = {
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

# Function that works as a ternary operator

cond = lambda condition, true, false: true if condition else false

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
    data = cond(data == None, {}, data)
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

    loc = load_yaml(localization[lang])
    loc = loc[f"loc_{lang}"]
    return loc

# Gets the localization string for a key

def localize(lang, key):

    return load_localization(lang)[key]

################################################################

# Formats a localization string

def format_loc(string, values):

    for i in range(len(values)):
        string = string.replace(f"${i+1}", str(values[i]))
    return string

################################################################

# Logs a message to a text file

async def log(msg):

    with open(files["log"], "a") as f:
        msg_datetime = f"{date()} | {time()} UTC"
        f.write("\n--------------------------------")
        f.write(f"\n[{msg_datetime}]")
        f.write(f"\n[{msg.guild.name} | {msg.guild.id}]")
        f.write(f"\n[#{msg.channel.name} | {msg.channel.id}]")
        f.write(f"\n[{msg.author} | {msg.author.id}]")
        f.write(f"\n{msg.content}")
        f.write("\n--------------------------------\n")

################################################################

# Gets the amount of songs in queue

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

# Continues playing the song queue

async def play_continue(ctx, voice):

    shift_queue(ctx.guild)

    if queue_length(ctx.guild) > 0:
        path = get_song_path(ctx.guild, 1)

        song_name = path.split("$<|sep;|>")[1]
        song_name = song_name.replace(" _ ", " ").replace(".mp3", "")
        text = Loc("text_play_playing").server_loc(ctx.guild)
        text = format_loc(text, [song_name])
        embed = get_embed(text)
        await ctx.channel.send(embed=embed)

        voice.play(discord.FFmpegPCMAudio(path))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume = 0.25

################################################################

# Creates an embed

def get_embed(text, title=None, author_name=None, author_img=None, timestamp=None, fields={}, footer=None, color=None):

    color = cond(color != None, color, default_embed_color)
    embed = discord.Embed(description=text, colour=color)
    if title != None:
        embed.title = title
    if author_name != None and author_img != None:
        embed.set_author(name=author_name, icon_url=str(author_img))
    if timestamp != None:
        embed.timestamp = timestamp
    for field in fields.items():
        embed.add_field(name=field[0], value=field[1], inline=False)
    if footer != None:
        embed.set_footer(text=footer)
    return embed

# Creates an embed using information obtained from the message

def get_cembed(msg, text, title=None, author_name=None, author_img=None, timestamp=None, fields={}, footer=None):

    color = read_user_config(msg.author.id, "embed_color")
    return get_embed(text, title, author_name, author_img, timestamp, fields, footer, color)

################################################################

# Class for localization placeholders

class Loc:

    def __init__(self, name):

        self.name = name
    
    def __repr__(self):

        return self.name

    def loc(self, lang):

        return localize(lang, self.name)

    def server_loc(self, server):

        lang = read_server_config(server.id, "language")
        lang = cond(lang != None, lang, "en_US")
        return self.loc(lang)

    def user_loc(self, user):

        lang = read_user_config(user.id, "language")
        if lang == None:
            lang = read_server_config(user.guild.id, "language")
        lang = cond(lang != None, lang, "en_US")
        return self.loc(lang)

# Config class for user and server config

class Config:

    def __init__(self, name, default, ftype):

        self.name = name
        self.default = default
        self.ftype = ftype
    
    def format(self, value):

        value = cond(value != None, value, self.default)

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

        return cond(value, fvalue, None)

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

# Creates a Command

def cmd(name, calls, category, args, delimiters, perms, code, dev=False):

    desc_name = name.replace("-", "_")
    desc = f"cmd_desc_{desc_name}"
    return Command(name, calls, category, args, delimiters, perms, Loc(desc), code, dev)

################################################################

# Info

################################################################

async def help(ctx):

    command = ctx.args["command"]

    if command == None:

        cmd_list = {}
        for cmd in commands:
            if cmd.category not in cmd_list.keys():
                cmd_list[cmd.category] = []
            cmd_list[cmd.category].append(cmd.name)
        cmd_list.pop("dev", None)

        prefix_text = Loc("text_help_prefix").user_loc(ctx.author)
        prefix_text = format_loc(prefix_text, [ctx.prefix])
        title = Loc("label_help").user_loc(ctx.author)

        category_list = {}
        for category in cmd_list.items():
            category_name = Loc(f"cmd_category_{category[0]}")
            category_name = category_name.user_loc(ctx.author)
            cmd_str = "`, `".join(category[1])
            cmd_str = f"`{cmd_str}`"
            category_list[category_name] = cmd_str

        embed = get_cembed(ctx.msg, f"{prefix_text}\n", title, fields=category_list)

    else:

        cmd = None
        for command in commands:
            arg_cmd = ctx.args["command"].lower().replace("_", "-")
            if arg_cmd.lstrip(ctx.prefix) in command.calls:
                cmd = command
        
        if cmd == None or cmd.category == "dev":
            text = Loc("err_help_unknown_cmd").user_loc(ctx.author)
            embed = get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)
            return

        fields = {}
        none = Loc("label_none").user_loc(ctx.author)

        syntax = Loc("label_syntax").user_loc(ctx.author)
        cmd_call = f"{ctx.prefix}{cmd.name}"
        args = " ".join(cmd.args)
        cmd_syntax = f"{cmd_call} {args}"
        fields[syntax] = f"`{cmd_syntax.strip()}`"
        
        aliases = Loc("label_aliases").user_loc(ctx.author)
        alias_list = [f"`{call}`" for call in cmd.calls if call != cmd.name]
        cmd_aliases = ", ".join(alias_list)
        fields[aliases] = cond(cmd_aliases != "", cmd_aliases, none)

        req_perms = Loc("label_req_perms").user_loc(ctx.author)
        perms = []
        for perm in cmd.perms:
            perm_name = Loc(f"perm_{perm}").user_loc(ctx.author)
            perms.append(perm_name)
        perms_text = ", ".join(perms)
        fields[req_perms] = cond(perms != [], perms_text, none)

        desc = Loc("label_desc").user_loc(ctx.author)
        fields[desc] = cmd.desc.user_loc(ctx.author)

        embed = get_cembed(ctx.msg, "", cmd_call, fields=fields)

    await ctx.channel.send(embed=embed)

################################################################

async def status(ctx):

    online_msg = Loc("text_status_online").user_loc(ctx.author)
    embed = get_cembed(ctx.msg, online_msg)
    await ctx.channel.send(embed=embed)

################################################################

async def invite(ctx):

    invite = await ctx.channel.create_invite(max_age=0, max_uses=0, unique=False)
    invite_link = Loc("label_invite_link").user_loc(ctx.author)
    embed = get_cembed(ctx.msg, invite.url, invite_link, ctx.guild.name, ctx.guild.icon_url)
    await ctx.channel.send(embed=embed)

################################################################

async def perms(ctx):

    if ctx.args["member"] == None:
        member = ctx.guild.get_member(ctx.author.id)
    else:
        member_id = mention_id(ctx.args["member"])
        member = ctx.guild.get_member(member_id)
        if member == None:
            text = Loc("err_unknown_member").user_loc(ctx.author)
            text = format_loc(text, [client.user.mention])
            embed = get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)
            return

    perms = member.guild_permissions
    perm_dict = {}
    for perm in perms:
        perm_dict["WIP"] = "WIP" # TODO

    perms_text = Loc("text_perms_list").user_loc(ctx.author)
    perms_text = format_loc(perms_text, [member.mention])
    perms_title = Loc("text_perms_title").user_loc(ctx.author)
    perms_title = format_loc(perms_title, [ctx.guild.name])

    embed = get_cembed(ctx.msg, perms_text, perms_title, member.name, member.avatar_url, fields=perm_dict)
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
            text = Loc("err_rng_range_larger").user_loc(ctx.author)
        if min_num == max_num:
            text = Loc("err_rng_range_equal").user_loc(ctx.author)

    except ValueError:
        text = Loc("err_rng_no_floats").user_loc(ctx.author)

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
        text = Loc("err_choice_not_enough").user_loc(ctx.author)
        text = format_loc(text, [delimiter])
    else:
        text = random.choice(choices)
    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

async def gay(ctx):

    target = ctx.args["target"]
    target = cond(target != None, target, ctx.author.mention)
    gay_percent = random.randint(0, 100)
    gay_text = Loc("text_gay").user_loc(ctx.author)
    gay_text = format_loc(gay_text, [target, gay_percent])
    gay_meter = Loc("label_gay_meter").user_loc(ctx.author)
    embed = get_cembed(ctx.msg, gay_text, gay_meter)
    await ctx.channel.send(embed=embed)

################################################################

async def penis(ctx):

    target = ctx.args["target"]
    target = cond(target != None, target, ctx.author.mention)
    penis = f"8{'=' * random.randint(0, 10)}>"
    penis_text = Loc("text_penis").user_loc(ctx.author)
    penis_text = format_loc(penis_text, [target, penis])
    penis_length = Loc("label_penis_length").user_loc(ctx.author)
    embed = get_cembed(ctx.msg, penis_text, penis_length)
    await ctx.channel.send(embed=embed)

################################################################

# Tools

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
        exec_loc[loc_name] = Loc(loc_name).user_loc(ctx.author)

    execute = PyExecute(files["pyexecute"], exec_loc)
    output = execute.execute(code)
    output = cond(len(output) <= 2000, output, output[:2000])

    title = Loc("label_output").user_loc(ctx.author)
    embed = get_cembed(ctx.msg, f"```{output}```", title)
    await ctx.channel.send(embed=embed)

################################################################

# Music

################################################################

async def join(ctx):

    voice = ctx.author.voice

    if voice == None:
        text = Loc("err_join_no_voice").user_loc(ctx.author)
    
    else:
        bot_channel = None
        for bot_voice in client.voice_clients:
            if bot_voice.guild == ctx.guild:
                bot_channel = bot_voice

        if bot_channel == None:
            await voice.channel.connect()
            text = Loc("text_join").user_loc(ctx.author)
            text = format_loc(text, [voice.channel])
        else:
            text = Loc("err_join_voice_connected").user_loc(ctx.author)

    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

async def leave(ctx):

    voices = client.voice_clients
    text = Loc("err_leave_no_voice").user_loc(ctx.author)

    for voice in voices:
        if voice.guild == ctx.guild:
            path = f"{song_dir}/{voice.guild.id}"
            await voice.disconnect()
            os.system(f"rm -rf {path}")
            
            text = Loc("text_leave").user_loc(ctx.author)
            text = format_loc(text, [voice.channel])

    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

async def play(ctx):

    voice = ctx.author.voice

    if voice == None:
        text = Loc("err_join_no_voice").user_loc(ctx.author)
        embed = get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return
    
    else:
        bot_channel = None
        for bot_voice in client.voice_clients:
            if bot_voice.guild == ctx.guild:
                bot_channel = bot_voice

        if bot_channel == None:
            await voice.channel.connect()
            text = Loc("text_join").user_loc(ctx.author)
            text = format_loc(text, [voice.channel])
            embed = get_cembed(ctx.msg, text)
            await ctx.channel.send(embed=embed)

    voices = client.voice_clients

    for voice in voices:
        if voice.guild == ctx.guild:
            text = Loc("text_play_downloading").user_loc(ctx.author)
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

        text = Loc("text_play_playing").server_loc(ctx.guild)
        text = format_loc(text, [song_name])

    else:
        text = Loc("text_play_add_queue").server_loc(ctx.guild)
        text = format_loc(text, [song_name])

    embed = get_embed(text)
    await ctx.channel.send(embed=embed)

################################################################

async def skip(ctx):

    voices = client.voice_clients
    text = Loc("err_skip_not_playing").user_loc(ctx.author)
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

                    text = Loc("text_play_playing").server_loc(voice.guild)
                    text = format_loc(text, [song_name])
                    embed = get_embed(text)

    await ctx.channel.send(embed=embed)

################################################################

# Moderation

################################################################

async def kick(ctx):

    target_id = mention_id(ctx.args["target"])
    target = ctx.guild.get_member(target_id)
    text = ""

    if target == None:
        text = Loc("err_unknown_member").user_loc(ctx.author)
        text = format_loc(text, [client.user.mention])
    elif target.top_role >= ctx.author.top_role:
        text = Loc("err_kick_perms_author").user_loc(ctx.author)
    if text != "":
        embed = get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return

    reason = Loc("text_kick_reason").user_loc(ctx.author)
    reason = format_loc(reason, [ctx.author])
    await target.kick(reason=reason)
    text = Loc("text_kick_success").user_loc(ctx.author)
    target_mention = f"<@!{target_id}>"
    text = format_loc(text, [target_mention])

    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

async def ban(ctx):

    target_id = mention_id(ctx.args["target"])
    target = ctx.guild.get_member(target_id)
    text = ""

    if target == None:
        text = Loc("err_unknown_member").user_loc(ctx.author)
        text = format_loc(text, [client.user.mention])
    elif target.top_role >= ctx.author.top_role:
        text = Loc("err_ban_perms_author").user_loc(ctx.author)
    if text != "":
        embed = get_cembed(ctx.msg, text)
        await ctx.channel.send(embed=embed)
        return

    reason = Loc("text_ban_reason").user_loc(ctx.author)
    reason = format_loc(reason, [ctx.author])
    await target.ban(reason=reason)
    text = Loc("text_ban_success").user_loc(ctx.author)
    target_mention = f"<@!{target_id}>"
    text = format_loc(text, [target_mention])

    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

# Config

################################################################

async def user_settings(ctx):

    target_mention = ctx.args["member"]
    target = ctx.author
    if target_mention != None:
        target_id = mention_id(target_mention)
        if target_id != 0:
            target = ctx.guild.get_member(target_id)

    if target == None:
        text = Loc("err_unknown_member").user_loc(ctx.author)
        text = format_loc(text, [client.user.mention])
        embed = get_cembed(ctx.msg, text)
        ctx.channel.send(embed=embed)
        return

    fields = {}
    for config in user_config:
        name = f"config_{config.name}"
        name = Loc(name).user_loc(ctx.author)
        value = read_user_config(target.id, config.name)
        value = config.format(value)
        fields[name] = value

    title = Loc("label_user_config").user_loc(ctx.author)
    embed = get_cembed(ctx.msg, "", title, target.name, target.avatar_url, fields=fields)
    await ctx.channel.send(embed=embed)

################################################################

async def server_settings(ctx):

    fields = {}
    for config in server_config:
        name = f"config_{config.name}"
        name = Loc(name).user_loc(ctx.author)
        value = read_server_config(ctx.guild.id, config.name)
        value = config.format(value)
        fields[name] = value

    title = Loc("label_server_config").user_loc(ctx.author)
    embed = get_cembed(ctx.msg, "", title, ctx.guild.name, ctx.guild.icon_url, fields=fields)
    await ctx.channel.send(embed=embed)

################################################################

async def language(ctx):

    lang = ctx.args["language"]

    if lang == None:

        fields = {}
        for language in localization.keys():
            lang_name = Loc("language_name").loc(language)
            lang_code = f"`{language}`"
            fields[lang_name] = lang_code
        
        text = Loc("text_lang_list").user_loc(ctx.author)
        title = Loc("label_languages").user_loc(ctx.author)
        embed = get_cembed(ctx.msg, text, title, fields=fields)
    
    else:

        if lang in localization.keys():
            set_user_config(ctx.author.id, "language", lang)
            text = Loc("text_lang_changed").user_loc(ctx.author)

        else:
            text = Loc("err_unknown_lang").user_loc(ctx.author)
        
        embed = get_cembed(ctx.msg, text)

    await ctx.channel.send(embed=embed)

################################################################

# Dev

################################################################

async def shutdown(ctx):

    text = Loc("text_exit").user_loc(ctx.author)
    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)
    def crash():
        try:
            crash()
        except:
            crash()
    crash()

################################################################

# Misc

################################################################

async def wip(ctx):

    text = Loc("text_wip").user_loc(ctx.author)
    embed = get_cembed(ctx.msg, text)
    await ctx.channel.send(embed=embed)

################################################################

# Config options

user_config = [
    Config("language", "en_US", "backticks"),
    Config("embed_color", int(default_embed_color), "hex_str")
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
    cmd(
        "help",
        ["help", "commands"],
        "info",
        ["[command]"],
        [" "],
        [],
        help
    ),

    # Status
    cmd(
        "status",
        ["status", "online", "test"],
        "info",
        [],
        [" "],
        [],
        status
    ),

    # Invite
    cmd(
        "invite",
        ["invite"],
        "info",
        [],
        [" "],
        [],
        invite
    ),

    # Perms
    cmd(
        "perms",
        ["perms", "perm", "permissions", "permission"],
        "info",
        ["[member]"],
        [" "],
        [],
        perms
    ),

    # Chat

    # RNG
    cmd(
        "rng",
        ["rng", "random", "randint"],
        "chat",
        ["<min>", "<max>"],
        [" "],
        [],
        rng
    ),

    # Choice
    cmd(
        "choice",
        ["choice", "choose"],
        "chat",
        ["<choices>"],
        ["$<|no_delimiter;|>"],
        [],
        choice
    ),

    # Gay
    cmd(
        "gay",
        ["gay", "how-gay", "gay-level", "gay-meter"],
        "chat",
        ["[target]"],
        ["$<|no_delimiter;|>"],
        [],
        gay
    ),

    # Penis
    cmd(
        "penis",
        ["penis", "penis-length", "penis-size"],
        "chat",
        ["[target]"],
        ["$<|no_delimiter;|>"],
        [],
        penis
    ),

    # Tools

    # Python
    cmd(
        "python",
        ["python", "py", "execute", "exec", "exe"],
        "tools",
        ["<code>"],
        ["$<|no_delimiter;|>"],
        [],
        python
    ),

    # Music

    # Join
    cmd(
        "join",
        ["join", "connect"],
        "music",
        [],
        [" "],
        [],
        join
    ),

    # Leave
    cmd(
        "leave",
        ["leave", "quit", "disconnect", "dc"],
        "music",
        [],
        [" "],
        [],
        leave
    ),

    # Play
    cmd(
        "play",
        ["play", "song", "music"],
        "music",
        ["<song>"],
        ["$<|no_delimiter;|>"],
        [],
        play
    ),

    # Skip
    cmd(
        "skip",
        ["skip"],
        "music",
        [],
        [" "],
        [],
        skip
    ),

    # Moderation

    # Kick
    cmd(
        "kick",
        ["kick"],
        "mod",
        ["<target>"],
        [" "],
        ["kick_members"],
        kick
    ),

    # Ban
    cmd(
        "ban",
        ["ban"],
        "mod",
        ["<target>"],
        [" "],
        ["ban_members"],
        ban
    ),

    # Config

    # User Settings
    cmd(
        "user-settings",
        ["user-settings", "user-config", "user-options"],
        "config",
        ["[member]"],
        [" "],
        [],
        user_settings
    ),

    # Server Settings
    cmd(
        "server-settings",
        ["server-settings", "server-config", "server-options"],
        "config",
        [],
        [" "],
        [],
        server_settings
    ),

    # Language
    cmd(
        "language",
        ["language", "languages", "lang"],
        "config",
        ["[language]"],
        [" "],
        [],
        language
    ),

    # Developer
    
    # Exit
    cmd(
        "exit",
        ["exit", "shutdown", "off"],
        "dev",
        [],
        [" "],
        [],
        shutdown,
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

                        text = Loc("text_play_playing").server_loc(voice.guild)
                        text = format_loc(text, [song_name])
                        embed = get_embed(text)
                        text_channel = play_text_output[voice.guild.id]
                        await text_channel.send(embed=embed)

        # Wait between check turns

        await asyncio.sleep(loop_interval)

################################################################

# Prints a message and sets the activity when ready

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
    if channel_id != None:
        channel = member.guild.get_channel(channel_id)
        text = Loc("text_join_msg").server_loc(member.guild)
        text = format_loc(text, [member.mention])
        embed = get_embed(text, "", member.name, member.avatar_url, datetime.datetime.now())
        await channel.send(embed=embed)

################################################################

# Logs all member leaves

@client.event

async def on_member_remove(member):

    channel_id = read_server_config(member.guild.id, "log_channel")
    if channel_id != None:
        channel = member.guild.get_channel(channel_id)
        text = Loc("text_leave_msg").server_loc(member.guild)
        text = format_loc(text, [member.mention])
        embed = get_embed(text, "", member.name, member.avatar_url, datetime.datetime.now())
        await channel.send(embed=embed)

################################################################

# Checks and evaluates messages

@client.event

async def on_message(msg):

    # Logs the message

    await log(msg)

    # If the message author is a bot or the message is empty, return

    if msg.author.bot or msg.content == "":
        return

    # Gets the server command prefix

    prefix = read_server_config(msg.guild.id, "Prefix")
    prefix = cond(prefix != None, prefix, default_prefix)

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
                    text = Loc("err_missing_perms").user_loc(msg.author)
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
                parts = cond(parts != [""], parts, [])
                arg_count = len(parts)

                # Gets the minimum amount of arguments

                min_args = 0
                for arg in cmd.args:
                    if arg.startswith("<"):
                        min_args += 1

                # Checks if the amount of arguments isn't too large

                if arg_count > len(cmd.args):
                    text = Loc("err_arg_overflow").user_loc(msg.author)
                    max_args = len(cmd.args)
                    none = Loc("label_none").user_loc(msg.author).lower()
                    max_args = cond(max_args > 0, max_args, none)
                    text = format_loc(text, [str(arg_count), str(max_args)])
                    embed = get_cembed(msg, text)
                    await msg.channel.send(embed=embed)
                    return

                # Checks if the amount of arguments isn't too small

                if arg_count < min_args:
                    text = Loc("err_arg_underflow").user_loc(msg.author)
                    text = format_loc(text, [arg_count, min_args])
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
                        text = Loc("err_missing_perms").user_loc(msg.author)
                        embed = get_cembed(msg, text)
                        await msg.channel.send(embed=embed)

                return

        # Get the list of command calls (except dev commands)

        calls = []
        for cmd in commands:
            if cmd.category != "dev":
                calls += cmd.calls

        # Find a close match between the entered command and the list of command calls, if there isn't any, display the default unknown command message

        try:
            match = difflib.get_close_matches(command, calls, 1, 0.6)[0]
            text = Loc("err_unknown_cmd_alt").user_loc(msg.author)
            text = format_loc(text, [prefix, match])
        except IndexError:
            text = Loc("err_unknown_cmd").user_loc(msg.author)
            text = format_loc(text, [prefix])

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
    if clean(msg.content).lower() in autoreplies.keys() and random.random() < (default_reply_chance if read_server_config(msg.guild.id, "Reply Chance") == None else read_server_config(msg.guild.id, "Reply Chance") / 100):
        await msg.channel.send(autoreplies[clean(msg.content).lower()])
    """

################################################################

init()
client.run(token)

################################################################