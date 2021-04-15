################################################################

import yaml

import constants
import utils

################################################################

# Loads YAML data from a file

def load_yaml(file):

    with open(file, "r") as f:
        data = yaml.safe_load(f)
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
    if value:
        data[id][option] = value
    else:
        data[id].pop(option, None)
    save_yaml(file, data)

################################################################

# Reads user config

def read_user_config(user_id, option):

    return read_config(constants.files["user_config"], user_id, option)

# Sets user config

def set_user_config(user_id, option, value):

    set_config(constants.files["user_config"], user_id, option, value)

# Reads server config

def read_server_config(server_id, option):

    return read_config(constants.files["server_config"], server_id, option)

# Sets server config

def set_server_config(server_id, option, value):

    set_config(constants.files["server_config"], server_id, option, value)

################################################################

# Config class for user and server config

class Config:

    def __init__(self, name, default, ftype, vtype):

        self.name = name
        self.default = default
        self.ftype = ftype
        self.vtype = vtype
    
    def format(self, value):

        value = value if value else self.default
        fvalue = None

        if not value:
            pass

        elif self.ftype == "hex_str":
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

    def validate(self, ctx, value):

        if self.vtype == "any":
            return value

        elif self.vtype == "lang_code":
            return value if value in constants.loc_files.keys() else None

        elif self.vtype == "text_channel":
            channel_id = utils.mention_id(value)
            for channel in ctx.guild.text_channels:
                if channel_id == channel.id:
                    return channel_id
            return None

################################################################