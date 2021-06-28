### Imports

# Standard Library
from typing import Union

# Conbot Modules
import const
import utils

### Class Definitions

# Config
class Config:
    """
    Represents a configurable value.
    """

    def __init__(self,
        name: str,
        default: str,
        ftype: str,
        dtype: str,
    ):
        self.name = name
        self.default = default
        self.ftype = ftype
        self.dtype = dtype

    def format(self, ctx, value):
        """
        Formats a value to fit the config
        format type.
        """
        if self.ftype == "any" or value == None: return value

        elif self.ftype == "lang_code":
            value = value.replace("-", "_")
            if value in const.languages: return value

        elif self.ftype == "text_channel":
            channel_id = utils.mention_id(value)
            if utils.get(ctx.guild.text_channels, id=channel_id):
                return channel_id

        elif self.ftype == "role":
            role_id = utils.mention_id(value)
            role = ctx.guild.get_role(role_id)
            if role and utils.is_role_normal(role):
                return role_id

    def display(self, value) -> Union[str, None]:
        """
        Converts a config value to its
        string representation.
        """
        value = value or self.default
        result = None
        if value == None: pass
        elif self.dtype == "default":
            result = str(value)

        elif self.dtype == "backticks":
            result = f"`{value}`"

        elif self.dtype == "lang_code":
            result = f"`{value.replace('_', '-')}`"

        elif self.dtype == "role_mention":
            result = f"<@&{value}>"

        elif self.dtype == "channel_mention":
            result = f"<#{value}>"

        elif self.dtype == "hex_str":
            value = hex(value)
            hex_number = value[2:].upper()
            zero_count = 8 - len(value)
            fvalue = f"`#{'0' * zero_count}{hex_number}`"

        return result

### Initialization

# User Config
user_config = [
    Config(
        "language",
        "en_US",
        "lang_code",
        "lang_code",
    ),
]

# Guild Config
guild_config = [
    Config(
        "language",
        "en_US",
        "lang_code",
        "lang_code",
    ),
    Config(
        "prefix",
        const.prefix,
        "any",
        "backticks",
    ),
    Config(
        "log_channel",
        None,
        "text_channel",
        "channel_mention",
    ),
    Config(
        "mute_role",
        None,
        "role",
        "role_mention",
    ),
]
