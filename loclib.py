################################################################

import const
import conyaml

################################################################

# Class for localization strings

class Loc:

    def __init__(self, name, lang, values=[]):

        self.name = name
        self.lang = lang
        self.values = values

    def format(self, *args):

        self.values = list(args)

    def __repr__(self):

        string = loc_dict[self.lang][self.name]
        for i in range(len(self.values)):
            string = string.replace(f"${i+1}", str(self.values[i]))
        return string

    def __str__(self):

        return repr(self)

    def __add__(self, obj):

        return str(self) + str(obj)
    
    def __len__(self):

        return len(str(self))

    def replace(self, old, new, count=9999):

        return str(self).replace(old, new, count)

    @classmethod
    def server(cls, name, server):

        lang = conyaml.read_server_config(server.id, "language") or "en_US"
        lang = lang or "en_US"
        return cls(name, lang)

    @classmethod
    def member(cls, name, member):

        lang = conyaml.read_user_config(member.id, "language") or \
        conyaml.read_server_config(member.guild.id, "language") or "en_US"
        return cls(name, lang)

################################################################

# Loads a localization file

def load_localization(lang):

    loc = conyaml.load_yaml(const.loc_files[lang])
    loc = loc[f"loc_{lang}"]
    return loc

################################################################

# Preloads the localization files

loc_dict = {lang:load_localization(lang) for lang in const.loc_files.keys()}

################################################################
