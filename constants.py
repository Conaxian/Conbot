################################################################

import os

################################################################

token = os.environ.get("DISCORD_BOT_TOKEN")

default_prefix = "?"
default_reply_chance = 0.3333
default_embed_color = 0x20a0e0

loop_timeout = 1
exec_timeout = 5

song_max_size = 5_242_880
song_max_length = 600

conax_discord_tag = "0001"
bot_invite_url = "https://www.conax.cz/conbot-link"
bot_github_url = "https://github.com/Conaxian/conbot"

files = {
    "log": "log.txt",
    "server_config": "server_config.yaml",
    "user_config": "user_config.yaml",
    "server_activity": "server_activity.yaml",
    "pyexecute": "exec_file.py",
    "pycalc": "calc_file.py"
}

loc_files = {
    "en_US": "localization/en_US.yaml",
    "en_GB": "localization/en_GB.yaml",
    "cs_CZ": "localization/cs_CZ.yaml"
}

song_dir = "songs"

devs = [
    209607873787985920 # Conax
]

################################################################