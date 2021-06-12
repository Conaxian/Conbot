################################################################

import yaml

import const
import utils

################################################################

# Load YAML data from a file

def load_yaml(file):

    with open(file, "a+", encoding="utf-8") as f:
        f.seek(0)
        data = yaml.safe_load(f)
    data = {} if not data else data
    return data

# Save YAML data to a file

def save_yaml(file, data):

    yaml_string = yaml.dump(data, default_flow_style=False)
    with open(file, "w", encoding="utf-8") as f:
        f.write(yaml_string)

################################################################

# Read YAML config option from a file

def read_config(file, id, option):

    data = load_yaml(file)
    try:
        return data[id][option]
    except:
        return

# Set YAML config option to a file

def set_config(file, id, option, value):

    data = load_yaml(file)
    if id not in data.keys():
        data[id] = {}
    if value:
        data[id][option] = value
    else:
        data[id].pop(option, None)
    save_yaml(file, data)

################################################################

# Read or set user config

def read_user_config(user_id, option):

    return read_config(const.files["user_config"], user_id, option)

def set_user_config(user_id, option, value):

    set_config(const.files["user_config"], user_id, option, value)

# Read or set server config

def read_server_config(server_id, option):

    return read_config(const.files["server_config"], server_id, option)

def set_server_config(server_id, option, value):

    set_config(const.files["server_config"], server_id, option, value)

################################################################

# Get the list of warns

def get_warns(server_id):

    data = load_yaml(const.files["warns"])
    try:
        return list(data[server_id].values())
    except:
        return []

# Add a warn

def add_warn(server_id, member_id, reason):

    data = load_yaml(const.files["warns"])
    if server_id not in data.keys():
        data[server_id] = {}
    warn_indices = data[server_id].keys()
    warn_index = max(warn_indices) + 1 if warn_indices else 1
    data[server_id][warn_index] = {
        "member": member_id,
        "reason": reason,
        "time": f"{utils.date()}-{utils.time()}",
    }
    save_yaml(const.files["warns"], data)

################################################################

# Get a mute

def get_mute(server_id, member_id):

    data = load_yaml(const.files["mutes"])
    try:
        return data[server_id][member_id]
    except KeyError:
        return None

# Add a mute

def add_mute(server_id, member_id, role_ids):

    data = load_yaml(const.files["mutes"])
    if server_id not in data.keys():
        data[server_id] = {}
    data[server_id][member_id] = {
        "roles": role_ids,
    }
    save_yaml(const.files["mutes"], data)

# Remove a mute

def remove_mute(server_id, member_id):

    data = load_yaml(const.files["mutes"])
    data[server_id].pop(member_id, None)
    if data[server_id] == {}: data.pop(server_id, None)
    save_yaml(const.files["mutes"], data)

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

        elif self.ftype == "role_mention":
            fvalue = f"<@&{value}>"

        elif self.ftype == "backticks":
            fvalue = f"`{value}`"

        elif self.ftype == "default":
            fvalue = value

        return fvalue

    def validate(self, ctx, value):

        if self.vtype == "any": return value

        elif self.vtype == "lang_code":
            value = value.replace("-", "_")
            return value if value in const.loc_files else None

        elif self.vtype == "text_channel":
            channel_id = utils.mention_id(value)
            if utils.get(ctx.guild.text_channels, id=channel_id):
                return channel_id

        elif self.vtype == "role":
            role_id = utils.mention_id(value)
            role = ctx.guild.get_role(role_id)
            if role and utils.is_role_normal(role):
                return role_id

################################################################
