################################################################

import discord
import datetime
import googletrans
import speedtest as speed_test

import const

################################################################

# Find the first element whose attributes match the specfied values

get = discord.utils.get

################################################################

# Convert a mention string (for example: <@!620175026972393472>) to user id

def mention_id(mention):

    try:
        if isinstance(mention, int) or mention.isdigit():
            return int(mention)

        base_mention = mention.startswith("<@") and mention[2:-1].isdigit()
        nickname_mention = mention.startswith("<@!") and mention[3:-1].isdigit()
        role_mention = mention.startswith("<@&") and mention[3:-1].isdigit()
        channel_mention = mention.startswith("<#") and mention[2:-1].isdigit()

        if any((base_mention, nickname_mention, role_mention, channel_mention)) and mention.endswith(">"):
            return int(mention.strip("<>@!&#"))

        else:
            return 0
    except:
        return 0

################################################################

# Get the current date in a DD/MM/YYYY format

def date(offset=datetime.timedelta()):

    datetime_now = datetime.datetime.now()
    datetime_now += offset
    day = f"{datetime_now.day:02d}"
    month = f"{datetime_now.month:02d}"
    date_str = f"{day}/{month}/{datetime_now.year}"
    return date_str

# Get the current time in a HH:MM format

def time(offset=datetime.timedelta()):

    datetime_now = datetime.datetime.now()
    datetime_now += offset
    hour = f"{datetime_now.hour:02d}"
    minute = f"{datetime_now.minute:02d}"
    time_str = f"{hour}:{minute}"
    return time_str

################################################################

# Check if the role is a normal role (neither @everyone 
# nor controled by Discord or an external app)

def is_role_normal(role):

    return not(
        role.is_bot_managed() or \
        role.is_default() or \
        role.is_integration() or \
        role.is_premium_subscriber()
    )

################################################################

# Translate a string (using Google Translate)

def translate(string, src=None, dest=None):

    translator = googletrans.Translator()
    kwargs = {}
    if src:
        kwargs["src"] = src
    if dest:
        kwargs["dest"] = dest
    translation = translator.translate(string, **kwargs)
    return translation

################################################################

# Test the internet speed of the bot's server

def speedtest():

    test = speed_test.Speedtest()
    test.get_best_server()
    test.download()
    test.upload()
    return test.results.ping, \
    test.results.download / 1000 / 1000, \
    test.results.upload / 1000 / 1000
    # Returns: Ping (ms), Download (Mbits), Upload (Mbits) 

################################################################

# Log a message to a text file

async def log(msg):

    with open(const.files["log"], "a", encoding="utf-8") as f:
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
