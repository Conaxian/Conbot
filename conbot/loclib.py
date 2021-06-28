### Imports

# Standard Library
import os
from typing import Union

# Dependencies
from discord import Message, Guild, Member, User

# Conbot Modules
import const
import conyaml

### Class Definitions

# Localization string
class Loc:
    """
    Represents a template for a localized string.
    """

    def __init__(self, id_: str):
        self.id = id_
        self.fvalues = []

    def __repr__(self):
        fvalues = ", ".join(self.fvalues)
        result = f"Loc[ id: {self.id}; fvalues: ({fvalues}) ]"
        return result

    def format(self, *args):
        """
        Formats the template using the arguments.
        """
        self.fvalues = list(args)
        return self

    def string(self, lang: str) -> str:
        """
        Localizes the string represented by this template.
        """
        id_path = self.id.split("/")
        string = load_localization(lang)
        for node in id_path:
            string = string[node]
        for i in range(len(self.fvalues)):
            string = string.replace(f"${i}", str(self.fvalues[i]))
        return string

    def cstring(self, 
    ctx: Union[Message, Guild, Member, User],
    ) -> str:
        """
        Localizes the string represented by this template.
        The language is received automatically from ctx.
        """
        lang, user, guild = None, None, None
        is_context = not (
            isinstance(ctx, Message) or \
            isinstance(ctx, Guild) or \
            isinstance(ctx, Member) or \
            isinstance(ctx, User)
        )

        if is_context:
            lang = ctx.meta.user_lang or ctx.meta.guild_lang
        if isinstance(ctx, Message) or (is_context and not lang):
            guild = ctx.guild
            user = ctx.author
        if isinstance(ctx, User): user = ctx
        if isinstance(ctx, Guild): guild = ctx
        if isinstance(ctx, Member):
            user, guild = ctx, ctx.guild

        if user:
            config = conyaml.read_data(f"user_config/{user.id}")
            lang = config.language
        if guild and not lang:
            config = conyaml.read_data(f"guild_config/{guild.id}")
            lang = config.language

        return self.string(lang or const.default_lang)

### Function Definitions

# Load localization
def load_localization(lang: str) -> dict:
    """
    Loads a localization file.
    """
    loc_path = os.path.join(const.loc_dir, f"{lang}.yaml")
    return conyaml.load_yaml(loc_path)
