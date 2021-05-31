################################################################

import os

################################################################

# APIs
token = os.environ.get("DISCORD_BOT_TOKEN")           # Discord Bot Token
reddit_secret = os.environ.get("REDDIT_SECRET")       # Reddit API Secret
reddit_client_id = "ujugHj6tvQp-Sw"                   # Reddit Client ID
reddit_user_agent = \
    "python:discord.conbot:v1.0.0 (by /u/ConbotUser)" # Reddit User Agent

# General
default_prefix = "?"
cmd_call_cooldown = 1          # Seconds
cmd_help_min_diff = 0.6        # Percentage from 0.0 to 1.0
default_embed_color = 0x20a0e0 # Hex Color Value

# Images
meme_subreddits = ["memes", "dankmemes"]

# Music
music_loop_time = 5       # Seconds
player_volume = 0.5       # Percentage from 0.0 to 1.0
song_max_length = 60 * 60 # Seconds
song_queue_limit = 10     # Seconds

# Python Execution
python_cmd = None         # Python command, None means automatically decide based on OS
exec_timeout = 5          # Seconds
checks_per_second = 40    # Frequency
allowed_modules = ["datetime", "math", "random", 
"hashlib", "time", "getpass", "socket", "urllib"]
banned_names = ["exec", "eval", "compile", 
"globals", "locals", "vars", "builtins", "dir", 
"open", "input", "breakpoint", "getattr", "delattr",
"__dict__", "__base__"]

# Misc
max_displayed_warns = 10 # Seconds

# Bot Info
conax_discord_tag = "0001"
bot_invite_url = "https://www.conax.cz/conbot-link"
bot_github_url = "https://github.com/Conaxian/conbot"

# Welcome Text
welcome_text = f"Thanks for adding me to your server!\n\n\
• The default command prefix is `{default_prefix}`\n\
• Use `{default_prefix}help` to get a list of available commands\n\
• Use `{default_prefix}lang` to change your language setting\n\
• The bot needs a role with administrator permissions to work correctly"

# Files
files = {
    "log": "log.txt",                      # Message Logs
    "server_config": "server_config.yaml", # Server Config
    "user_config": "user_config.yaml",     # User Config
    "warns": "server_warns.yaml",          # Server Warns
    "pyexecute": "exec_file.py",           # Python Execution File
    "pycalc": "calc_file.py"               # Python Calculation File
}

# Localization Files
loc_files = {
    "en_US": "localization/en_US.yaml",
    "en_GB": "localization/en_GB.yaml",
    "cs_CZ": "localization/cs_CZ.yaml"
}

# Developer IDs (developers have access to dev commands)
devs = [
    209607873787985920, # Conax
    474247464799436820  # Markeon
]

################################################################
