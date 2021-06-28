### Imports

# Standard Library
import os

# Dependencies
from dotenv import load_dotenv

### Constants

# General
name = "Conbot"
author = "Conax#0001" # Discord in Name#Tag format
bot_invite = "https://www.conax.cz/conbot-link" # URL
bot_github = "https://github.com/Conaxian/Conbot" # URL
encoding = "utf-8" # UTF-8 is recommended
date_format = "%d/%m/%Y" # DD/MM/YYYY
time_format = "%H:%M" # HH:MM
time_format_sec = "%H:%M:%S" # HH:MM:SS
md_chars = "*_~`>|" # Markdown Characters

# Version
version_file = "version.txt"
with open(version_file, "r", encoding=encoding) as file:
    version = file.read().strip()

# Embeds
embed_desc_limit = 2048 # Characters
embed_color = 0x20a0e0 # Hex Color, Default
footer_text = "$TIME UTC" # $TIME is replaced by current UTC time
footer_icon = "https://conax.cz/cbfiles/embed_clock.png" # URL

# Permissions
permissions = {
    "administrator": [
        "administrator",
        "view_channel",
        "manage_channels",
        "manage_roles",
        "manage_emojis",
        "view_audit_log",
        "manage_webhooks",
        "manage_guild",
    ],
    "membership": [
        "create_instant_invite",
        "change_nickname",
        "manage_nicknames",
        "kick_members",
        "ban_members",
    ],
    "text_channels": [
        "send_messages",
        "embed_links",
        "attach_files",
        "add_reactions",
        "external_emojis",
        "mention_everyone",
        "manage_messages",
        "read_message_history",
        "send_tts_messages",
        "use_slash_commands",
    ],
    "voice_channels": [
        "connect",
        "speak",
        "stream",
        "use_voice_activation",
        "priority_speaker",
        "mute_members",
        "deafen_members",
        "move_members",
    ],
} # Category-Permissions Pairs

# Commands
cmd_dir = "commands" # Commands Directory
prefix = "?" # Default
cmd_cooldown = 1 # Seconds
cmd_hint_threshold = 0.6 # Decimal Percentage
categories = [
    "info",
    "chat",
    "tools",
    "images",
    "music",
    "mod",
    "config",
    "dev",
] # Command Categories

# Environmental Variables
load_dotenv()
token = os.environ.get("DISCORD_BOT_TOKEN")
reddit_secret = os.environ.get("REDDIT_SECRET")

# Reddit API
reddit_client_id = "ujugHj6tvQp-Sw"
reddit_user_agent = \
    "python:discord.conbot:v1.0.0\
    (by /u/ConbotUser)"

# Files
log_file = "log.txt"
data_file = "cbdata.yaml"
pyexec_file = "execute.py"

# Localization
loc_dir = "locale" # Localization Directory
default_lang = "en_US"
languages = [
    "en_US", # American English
    "en_GB", # British English
    "cs_CZ", # Czech
] # Language Codes

# Developers (have access to dev commands and bypass permissions)
devs = [
    209607873787985920, # Conax
    474247464799436820, # Markeon
]

# Welcome Text
welcome_text = \
f"\
Thanks for adding me to your server!\
\n\n\t\
• The default command prefix is `{prefix}`\
\n\t\
• Use `{prefix}help` to get a list of available commands\
\n\t\
• Use `{prefix}lang` to change your language setting\
\n\t\
• The bot needs a role with administrator permissions \
to work correctly"

# Autoreplies
autoreplies = {
    "f": "F",
    "no u": "No u",
    "conax": "Conax is cool",
    "conbot": "Conbot is cool",
} # Trigger-Result Pairs (trigger must be lowercase)

# Images
meme_subreddits = ["memes", "dankmemes"]

# Music
music_loop_interval = 5 # Seconds
player_volume = 0.5 # Decimal Percentage
music_max_length = 60 * 60 # Seconds
music_queue_limit = 10

# Moderation
max_warns_shown = 10

# Python Executor
python_cmd = None # Python command, None means OS default
                  # (python on Windows and python3 
                  # on Unix-like systems)
exec_timeout = 5 # Seconds
checks_per_second = 40 # Frequency
allowed_modules = [
    "datetime",
    "math",
    "random",
    "hashlib",
    "time",
    "getpass",
    "socket",
    "urllib",
] # Modules
banned_names = [
    "exec",
    "eval",
    "compile",
    "globals",
    "locals",
    "vars",
    "builtins",
    "dir",
    "open",
    "input",
    "breakpoint",
    "getattr",
    "delattr",
    "__dict__",
    "__base__",
] # Functions, Attributes
