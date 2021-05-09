################################################################

import os

################################################################

token = os.environ.get("DISCORD_BOT_TOKEN")

default_prefix = "?"
default_reply_chance = 0.3333
default_embed_color = 0x20a0e0

music_loop_time = 5 # Seconds

cmd_call_cooldown = 1 # Seconds
exec_timeout = 5 # Seconds
max_displayed_warns = 10 # Seconds
song_max_length = 60 * 60 # Seconds
song_queue_limit = 10 # Seconds
player_volume = 0.5

conax_discord_tag = "0001"
bot_invite_url = "https://www.conax.cz/conbot-link"
bot_github_url = "https://github.com/Conaxian/conbot"

welcome_text = f"Thanks for adding me to your server!\n\n• The default command prefix is `{default_prefix}`\n• Use `{default_prefix}help` to get a list of available commands\n• Use `{default_prefix}lang` to change your language setting\n• The bot needs a role with administrator permissions to work correctly"

files = {
    "log": "log.txt",
    "server_config": "server_config.yaml",
    "user_config": "user_config.yaml",
    "warns": "server_warns.yaml",
    "pyexecute": "exec_file.py",
    "pycalc": "calc_file.py"
}

loc_files = {
    "en_US": "localization/en_US.yaml",
    "en_GB": "localization/en_GB.yaml",
    "cs_CZ": "localization/cs_CZ.yaml"
}

devs = [
    209607873787985920, # Conax
    474247464799436820  # Markeon
]

################################################################
