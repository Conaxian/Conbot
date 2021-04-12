################################################################

import datetime
import googletrans

import constants

################################################################

# Converts a mention string (for example: <@!620175026972393472>) to user id

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

# Translates a string into English

async def translate_en(string):

    translator = googletrans.Translator()
    translation = translator.translate(string)
    source, dest = translation.src, translation.dest
    return translation, source, dest

################################################################

# Logs a message to a text file

async def log(msg):

    with open(constants.files["log"], "a") as f:
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