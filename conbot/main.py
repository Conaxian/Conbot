### Imports

# Standard Library
from datetime import datetime

# Dependencies
import discord
from discord.ext import tasks

# Conbot Modules
import const
from utils import log
from bot import Bot
from msg_handler import MsgHandler
from conyaml import read_data
from cembed import embed
from loclib import Loc
from musiclib import player_check

### Initialization

# Create a bot and a message handler
bot = Bot()
msg_handler = MsgHandler(bot)

### Bot Tasks

# Music Player Loop
@tasks.loop(seconds=const.music_loop_interval)
async def player_loop():
    """
    Periodically checks the music player.
    """
    await player_check(bot.voice_clients)

### Bot Events

# Execute when the bot is ready
@bot.event
async def on_ready():
    """
    Prints a successful init message.
    """
    print(f"Bot initialized as {bot.user}")
    player_loop.start()

# Execute when a message is sent
@bot.event
async def on_message(msg: discord.Message):
    """
    Logs and evaluates messages.
    """
    log(msg)
    await msg_handler.handle(msg)

# Execute when a member joins a guild
@bot.event
async def on_member_join(member: discord.Member):
    """
    Sends a log message when a member joins a guild.
    """
    log_channel_id = read_data("guild_config/" + \
        f"{member.guild.id}/log_channel")
    if not log_channel_id: return
    log_channel = member.guild.get_channel(log_channel_id)

    text = Loc("log/member_join").format(member.mention)
    embed_ = embed(text.cstring(member.guild), author={
        "name": member.name,
        "icon": member.avatar_url,
    }, timestamp=datetime.utcnow())
    await log_channel.send(embed=embed_)

# Execute when a member leaves a guild
@bot.event
async def on_member_remove(member: discord.Member):
    """
    Sends a log message when a member leaves a guild.
    """
    log_channel_id = read_data("guild_config/" + \
        f"{member.guild.id}/log_channel")
    if not log_channel_id: return
    log_channel = member.guild.get_channel(log_channel_id)

    text = Loc("log/member_leave").format(member.mention)
    embed_ = embed(text.cstring(member.guild), author={
        "name": member.name,
        "icon": member.avatar_url,
    }, timestamp=datetime.utcnow())
    await log_channel.send(embed=embed_)

# Execute when the bot joins a guild
@bot.event
async def on_guild_join(guild: discord.Guild):
    """
    Sends the guild welcome message.
    """
    channel = \
        guild.public_updates_channel or \
        guild.system_channel or \
        guild.text_channels[0]
    await channel.send(const.welcome_text)

# Start the bot
bot.run(const.token)
